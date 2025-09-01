#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime

# Optional color support
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    C = True
except Exception:
    class _N:  # no-colors fallback
        RESET = ""
    class _F:
        RED = GREEN = YELLOW = CYAN = MAGENTA = BLUE = WHITE = ""
    C = False
    Fore = _F()
    Style = _N()

# YAML loader
try:
    import yaml
except ImportError:
    print("❌ Missing dependency: PyYAML\n   Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
STATUS_ORDER   = {"Active": 0, "In Development": 1, "Concept Phase": 2, "On Hold": 3, "Completed": 4}

STATUS_COLOR = {
    "Active": Fore.GREEN if C else "",
    "In Development": Fore.CYAN if C else "",
    "Concept Phase": Fore.YELLOW if C else "",
    "On Hold": Fore.MAGENTA if C else "",
    "Completed": Fore.BLUE if C else "",
}

def find_yaml(default_name="project_status.yaml"):
    """
    Look for YAML in:
      1) --file arg if provided
      2) CWD
      3) ./Master_Project_Tracker/
    """
    # This gets overridden if --file is used
    here = os.getcwd()
    candidates = [
        os.path.join(here, default_name),
        os.path.join(here, "Master_Project_Tracker", default_name),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def load_projects(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    projects = data.get("projects", [])
    # Normalize fields
    norm = []
    for p in projects:
        norm.append({
            "id": p.get("id", ""),
            "name": p.get("name", ""),
            "description": p.get("description", ""),
            "status": p.get("status", ""),
            "priority": p.get("priority", ""),
            "tags": p.get("tags", []),
            "last_updated": p.get("last_updated", ""),
        })
    return norm

def filter_projects(items, tags=None, status=None):
    res = items
    if tags:
        tagset = set(t.lower() for t in tags)
        res = [p for p in res if tagset.issubset(set(t.lower() for t in p.get("tags", [])))]
    if status:
        status = {s.lower() for s in status}
        res = [p for p in res if p.get("status", "").lower() in status]
    return res

def sort_projects(items, key):
    if key == "priority":
        return sorted(items, key=lambda p: (PRIORITY_ORDER.get(p["priority"], 99), p["name"].lower()))
    if key == "status":
        return sorted(items, key=lambda p: (STATUS_ORDER.get(p["status"], 99), p["name"].lower()))
    return sorted(items, key=lambda p: p["name"].lower())

def pad(text, width):
    s = str(text)
    return s if len(s) >= width else s + " " * (width - len(s))

def color_status(s):
    return f"{STATUS_COLOR.get(s,'')}{s}{Style.RESET_ALL if C else ''}"

def print_table(items):
    if not items:
        print("No projects to display.")
        return
    # compute widths
    name_w  = max(20, max(len(p["name"]) for p in items))
    stat_w  = max(12, max(len(p["status"]) for p in items))
    prio_w  = max(6,  max(len(p["priority"]) for p in items))
    upd_w   = max(10, max(len(p["last_updated"]) for p in items))
    tags_w  = max(10, max(len(", ".join(p.get("tags", []))) for p in items))

    hdr = [
        pad("Project", name_w),
        pad("Status",  stat_w),
        pad("Priority", prio_w),
        pad("Last Updated", upd_w),
        pad("Tags", tags_w),
    ]
    sep = "-".ljust(sum(len(h)+3 for h in hdr), "-")

    print(sep)
    print(" | ".join(hdr))
    print(sep)
    for p in items:
        row = [
            pad(p["name"], name_w),
            pad(color_status(p["status"]), stat_w),
            pad(p["priority"], prio_w),
            pad(p["last_updated"], upd_w),
            pad(", ".join(p.get("tags", [])), tags_w),
        ]
        print(" | ".join(row))
    print(sep)

def main():
    ap = argparse.ArgumentParser(description="Show project statuses from project_status.yaml")
    ap.add_argument("--file", "-f", help="Path to YAML (default: project_status.yaml or Master_Project_Tracker/project_status.yaml)")
    ap.add_argument("--sort", "-s", choices=["name", "priority", "status"], default="priority",
                    help="Sort column (default: priority)")
    ap.add_argument("--tag", "-t", action="append", help="Filter by tag (can repeat)")
    ap.add_argument("--status", "-S", action="append", help="Filter by status (can repeat)")
    args = ap.parse_args()

    yaml_path = args.file or find_yaml()
    if not yaml_path:
        print("❌ Could not find project_status.yaml.\n   Use --file or place it in CWD or ./Master_Project_Tracker/", file=sys.stderr)
        sys.exit(1)

    projects = load_projects(yaml_path)
    projects = filter_projects(projects, tags=args.tag, status=args.status)
    projects = sort_projects(projects, args.sort)

    print(f"\n📄 Source: {yaml_path}")
    print_table(projects)

if __name__ == "__main__":
    main()
