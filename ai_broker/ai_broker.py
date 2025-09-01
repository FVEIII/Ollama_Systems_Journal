# Minimal AI Safety Broker
# - Enforces directory scopes, autonomy budgets, network allowlist, and tripwires
# - Provides append-only, hash-chained logs for tamper-evident auditing
#
# Usage (CLI):
#   python -m ai_broker read --path "./content/notes.md"
#   python -m ai_broker write --path "./exports/out.txt" --text "hello"
#   python -m ai_broker http_get --url "https://example.com"
#
# Python API:
#   from ai_broker import Broker
#   b = Broker("policy.json", log_path="broker.log")
#   data = b.read_file("./content/notes.md")

import os, sys, json, re, hashlib, datetime, urllib.parse, urllib.request

__all__ = ["Broker", "PolicyError", "TripwireError", "BudgetError"]

class PolicyError(Exception): pass
class TripwireError(Exception): pass
class BudgetError(Exception): pass

def _now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def _norm(p):
    return os.path.realpath(os.path.normpath(p))

def _is_under(path, base):
    path = _norm(path)
    base = _norm(base)
    try:
        return os.path.commonpath([path, base]) == base
    except ValueError:
        return False

class Broker:
    def __init__(self, policy_path="policy.json", log_path="broker.log"):
        with open(policy_path, "r", encoding="utf-8") as f:
            self.policy = json.load(f)
        self.log_path = log_path
        self.calls_used = 0
        self.prev_hash = self._last_hash()

    # ------------ Logging (hash-chained) ------------
    def _last_hash(self):
        if not os.path.exists(self.log_path):
            return "0"*64
        last = None
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if line:
                    last = json.loads(line)
        return last["hash"] if last else "0"*64

    def _log(self, action, details):
        record = {
            "ts": _now_iso(),
            "action": action,
            "details": details,
            "prev_hash": self.prev_hash
        }
        h = hashlib.sha256(json.dumps(record, sort_keys=True).encode("utf-8")).hexdigest()
        record["hash"] = h
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.prev_hash = h

    # ------------ Policy helpers ------------
    def _require_budget(self):
        self.calls_used += 1
        max_calls = int(self.policy.get("budgets", {}).get("max_tool_calls_per_task", 5))
        if self.calls_used > max_calls:
            self._log("budget_exceeded", {"calls_used": self.calls_used, "max": max_calls})
            raise BudgetError(f"Autonomy budget exceeded: {self.calls_used}/{max_calls}")

    def _check_tripwires(self, text):
        if not text:
            return
        for pattern in self.policy.get("tripwires", []):
            try:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    self._log("tripwire_triggered", {"pattern": pattern, "text_excerpt": text[:200]})
                    raise TripwireError(f"Tripwire matched: {pattern}")
            except re.error:
                # Treat invalid regex as literal substring
                if pattern.lower() in text.lower():
                    self._log("tripwire_triggered", {"pattern": pattern, "text_excerpt": text[:200]})
                    raise TripwireError(f"Tripwire matched (literal): {pattern}")

    def _confirm(self, prompt):
        if not sys.stdin.isatty():
            raise PolicyError("Confirmation required but no TTY available")
        print(f"[CONFIRM] {prompt} (y/N): ", end="", flush=True)
        resp = sys.stdin.readline().strip().lower()
        return resp in ("y", "yes")

    # ------------ File operations ------------
    def _allowed_base(self, path, allow_list):
        path = _norm(path)
        for base in allow_list:
            if _is_under(path, base):
                return base
        return None

    def read_file(self, path):
        self._require_budget()
        base = self._allowed_base(path, self.policy.get("directories", {}).get("allow_read", []))
        if not base:
            raise PolicyError(f"Read path not allowed: {path}")
        if not os.path.exists(path):
            raise PolicyError(f"File not found: {path}")
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = f.read()
        self._check_tripwires(data)
        self._log("read_file", {"path": _norm(path)})
        return data

    def write_file(self, path, text):
        self._require_budget()
        base = self._allowed_base(path, self.policy.get("directories", {}).get("allow_write", []))
        if not base:
            raise PolicyError(f"Write path not allowed: {path}")
        max_bytes = int(self.policy.get("budgets", {}).get("max_bytes_write", 5_000_000))
        enc = text.encode("utf-8")
        if len(enc) > max_bytes:
            raise PolicyError(f"Write exceeds max_bytes_write ({len(enc)} > {max_bytes})")
        os.makedirs(os.path.dirname(_norm(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        self._log("write_file", {"path": _norm(path), "bytes": len(enc)})
        return True

    # ------------ Network (GET only) ------------
    def http_get(self, url, timeout=10):
        self._require_budget()
        net = self.policy.get("network", {})
        if not net.get("enabled", False):
            raise PolicyError("Network is disabled by policy")
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        allow_domains = [d.lower() for d in net.get("allow_domains", [])]
        if domain not in allow_domains:
            if not self._confirm(f"Domain {domain} not in allowlist. Proceed?"):
                self._log("http_blocked", {"url": url, "reason": "not_allowlisted"})
                raise PolicyError("Network request denied")
        req = urllib.request.Request(url, headers={"User-Agent": "ai-broker/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        self._log("http_get", {"url": url, "bytes": len(data), "status": 200})
        # Do not pass raw bytes to models; caller should parse to safe formats.
        return data

# ---------------- CLI ----------------

def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print("Usage: python -m ai_broker <read|write|http_get> [args]\n"
              "  read --path PATH\n"
              "  write --path PATH --text TEXT\n"
              "  http_get --url URL\n")
        return 0

    cmd = argv[0]
    # discover policy/log next to module by default
    module_dir = os.path.dirname(__file__)
    policy_path = os.path.join(module_dir, "policy.json")
    log_path = os.path.join(module_dir, "broker.log")
    broker = Broker(policy_path=policy_path, log_path=log_path)

    def argval(flag):
        if flag in argv:
            i = argv.index(flag)
            if i+1 < len(argv):
                return argv[i+1]
        return None

    try:
        if cmd == "read":
            path = argval("--path")
            if not path: raise PolicyError("Missing --path")
            data = broker.read_file(path)
            # print to stdout for piping
            sys.stdout.write(data)
        elif cmd == "write":
            path = argval("--path")
            text = argval("--text")
            if not path or text is None: raise PolicyError("Missing --path or --text")
            broker.write_file(path, text)
            print("OK")
        elif cmd == "http_get":
            url = argval("--url")
            if not url: raise PolicyError("Missing --url")
            content = broker.http_get(url)
            # For CLI safety, print byte length only
            print(f"[fetched {len(content)} bytes]")
        else:
            raise PolicyError(f"Unknown command: {cmd}")
    except (PolicyError, TripwireError, BudgetError) as e:
        print(f"[BLOCKED] {e}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
