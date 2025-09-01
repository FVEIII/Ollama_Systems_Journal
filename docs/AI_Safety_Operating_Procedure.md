# AI Safety Operating Procedure (SOP)

> Scope: Local and small‑team use of LLMs/agents (e.g., Ollama + VS Code) for coding, content, data work, and maker/CNC tasks.
> Goal: Harvest benefits of AI while reducing tail‑risks via capability firewalls (what the model can touch), behavioral guardrails (how it behaves), and procedural brakes (how humans approve and reverse).

---

## 0) Roles and Surfaces
- **Model**: Stateless tool‑using assistant. No long‑horizon goals. No self‑modification.
- **Broker**: A small guard process that enforces policy before any tool/action.
- **Human Operator**: Approves sensitive actions, reviews logs daily, controls the kill switch.
- **Tools**: File I/O, web fetch (allowlisted), CNC/laser exporters, email drafts. Tools are **brokered**, never called raw.

---

## 1) Default Operating Mode
1. **Offline by default**: No network tool unless explicitly enabled per‑task.
2. **Least privilege**: Grant the smallest directory scopes and tool scopes needed.
3. **Autonomy budget**: Each task gets a max N tool calls (default: 5). On cap, the model must summarize and stop.
4. **Two‑stage outreach**: AI may draft emails/posts; **you** send them. No autonomous external messaging.
5. **Append‑only logs**: Every action is logged with a tamper‑evident hash chain.
6. **Tripwires**: Pattern checks (deception, prompt-injection, impersonation, secret exfil) pause execution and alert the operator.

---

## 2) Sensitive Operations (Require Confirmation)
- Network requests to non‑allowlisted domains.
- Writing outside approved directories.
- Launching external processes or shell (generally **disallowed**).
- Any action referencing personal secrets, credentials, or private keys.
- CNC/laser **export** that would overwrite prior g‑code/artifacts.

> Confirmation is **out‑of‑band** (human prompt in the broker), not via the model itself.

---

## 3) Logging and Audit
- **Immutable journal**: Each event is recorded with timestamp, actor (model/operator), action, parameters, and `prev_hash` → `hash` chain.
- **Daily skim** (5–10 min): Check for loops, repeated denials, or unusual network/file patterns.
- **Incident handling**:
  - Stop the session.
  - Snapshot the working directory and log file.
  - Write a short postmortem (what, why, mitigation).
  - Update policy and tripwires if needed.

---

## 4) Policy Structure (Enforced by the Broker)
- **Directories**:
  - `allow_read`: Whitelisted base paths for reading.
  - `allow_write`: Whitelisted base paths for writing/creating files.
- **Networking**:
  - `allow_domains`: e.g., `["example.com"]`; all others require explicit approval.
  - Global on/off switch.
- **Budgets**:
  - `max_tool_calls_per_task` (default 5).
  - `max_bytes_write` per file (default 5 MB).
- **Tripwires** (regex or substrings):
  - Prompt‑injection (e.g., “ignore previous instructions”).
  - Impersonation (e.g., “pretend to be the user”).
  - Secret exfiltration (e.g., “AWS_SECRET”, “PRIVATE KEY”).
  - Deceptive phrasing (“do not log”, “bypass policy”, “act silently”).

---

## 5) Prohibited Capabilities
- Self‑modification: The runtime model cannot update its weights, policies, or tools.
- Raw shell access.
- Direct email send or social posting.
- Training on your operational logs without review/consent.

---

## 6) Review Cadence
- **Daily**: Log skim, revoke anomalies.
- **Weekly**: Update `policy.json` scopes (only if needed), rotate logs.
- **Quarterly**: Run red‑team scenarios (prompt‑injection, deception, untrusted inputs) and tune tripwires.

---

## 7) Quickstart (with the included broker)
1. Place `ai_broker/` in your Systems Journal repo.
2. Edit `policy.json` to reflect your project paths, domains, and budgets.
3. Wrap dangerous operations by calling the broker’s CLI or Python API:
   ```bash
   # example: read a file (within allowed paths)
   python -m ai_broker read --path "./content/notes.md"

   # example: safe write (enforced size + directory scope)
   python -m ai_broker write --path "./exports/output.txt" --text "hello"

   # example: allowlisted GET (or require confirm if not allowlisted)
   python -m ai_broker http_get --url "https://example.com/data.json"
   ```
4. Review `broker.log` after sessions. If a tripwire triggers, the broker halts and prints a message.

---

## 8) Extending Safely
- Add a **CNC export tool** through the broker that validates file extension (e.g., `.nc`, `.gcode`) and writes only to `./exports/cnc/`.
- Add a **summarize‑then‑act** pattern: require the model to output a one‑paragraph plan, which the broker stores, before granting tools.
- Consider a **second‑AI reviewer** (offline) to critique risky plans—but broker remains the final guard.

---

## 9) Philosophy in a sentence
Treat the model as a brilliant intern in a glass room: lots of visibility, limited levers, and a big friendly stop button.
