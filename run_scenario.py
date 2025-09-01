#!/usr/bin/env python3
import os, sys, argparse, subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def ap(*parts): return os.path.join(BASE_DIR, *parts)

LAST_PROMPT_FILE = ap(".last_prompt")

def load_last_prompt():
    try:
        with open(LAST_PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_prompt(relpath: str):
    with open(LAST_PROMPT_FILE, "w", encoding="utf-8") as f:
        f.write(relpath)

def list_prompts():
    pdir = ap("prompts")
    print("Available prompts:")
    for root, _, files in os.walk(pdir):
        for fn in sorted(files):
            if fn.lower().endswith(".md"):
                rel = os.path.relpath(os.path.join(root, fn), BASE_DIR)
                print(rel.replace("\\", "/"))

def read_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    t = text.lstrip()
    if t.startswith("---"):
        parts = t.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return text.strip()

def ask_ollama(prompt: str, model: str) -> str:
    print("\n▶ Sending to Ollama…")
    try:
        r = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True, text=True, encoding="utf-8", check=True
        )
        stdout = (r.stdout or "").strip()
        stderr = (r.stderr or "").strip()
        if stderr:
            print("ℹ️ ollama stderr:", stderr[:4000], "\n")
        print("◀ Raw response (first 600 chars):\n", stdout[:600], "\n")
        return stdout
    except subprocess.CalledProcessError as e:
        # Show *everything* we can to debug quickly
        print("\n❌ Ollama run failed.")
        if e.stderr:
            print("stderr:\n", e.stderr[:4000])
        if e.stdout:
            print("stdout:\n", e.stdout[:4000])
        print("Args:", e.args)
        raise

def append_report(prompt: str, response: str, outfile_abs: str, title: str):
    ts = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    block = f"""
## {ts} — {title}

**Prompt**
{prompt}

**Analysis & Recommendations**
{response}

---
"""
    os.makedirs(os.path.dirname(outfile_abs), exist_ok=True)
    with open(outfile_abs, "a", encoding="utf-8") as f:
        f.write(block)

def main():
    apg = argparse.ArgumentParser(description="Run a simulation prompt with Ollama and append a report.")
    apg.add_argument("-p", "--prompt",
        help="Path to prompt .md (relative to project root), e.g. prompts/global_price_drop_aromas.md")
    apg.add_argument("-m", "--model", default="llama3",
        help="Ollama model name (default: llama3)")
    apg.add_argument("-o", "--out", default="coffee_sim/market_analysis.md",
        help="Output markdown file (relative to project root)")
    apg.add_argument("--list", action="store_true", help="List available prompts and exit")
    apg.add_argument("--no-remember", dest="no_remember", action="store_true",
        help="Do not save this prompt as last-used")
    args = apg.parse_args()

    if args.list:
        list_prompts()
        return

    # Resolve prompt
    rel_prompt = args.prompt or load_last_prompt()
    if not rel_prompt:
        print("No prompt specified and no last-used prompt found. Use --prompt or --list.")
        sys.exit(1)

    rel_prompt = rel_prompt.replace("\\", "/")
    prompt_abs = ap(*rel_prompt.split("/"))
    out_abs    = ap(*args.out.replace("\\", "/").split("/"))

    if not os.path.exists(prompt_abs):
        print(f"❌ Prompt not found: {prompt_abs}")
        sys.exit(1)

    title = os.path.splitext(os.path.basename(prompt_abs))[0].replace("_", " ").title()

    print(f"Using prompt : {prompt_abs}")
    print(f"Writing to   : {out_abs}")
    print(f"Model        : {args.model}")

    if not args.no_remember:
        save_last_prompt(rel_prompt)

    prompt_text = read_prompt(prompt_abs)
    if not prompt_text:
        print("❌ Prompt file is empty after stripping frontmatter.")
        sys.exit(1)

    response = ask_ollama(prompt_text, args.model).strip()

    if not response:
        print("⚠️ Empty response from model — nothing appended.")
        sys.exit(2)

    append_report(prompt_text, response, out_abs, title)
    print(f"✅ Done — appended to: {out_abs}")

if __name__ == "__main__":
    main()
