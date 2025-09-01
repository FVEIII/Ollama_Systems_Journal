import argparse
from pathlib import Path
from sync_utils import sync_csv_to_yaml
import csv

parser = argparse.ArgumentParser(description="Sync YAML frontmatter with CSV dashboard.")
parser.add_argument("--csv", type=Path, default=Path("frontmatter_dashboard.csv"))
args = parser.parse_args()

updated = sync_csv_to_yaml(args.csv)

if updated:
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = updated[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated)

    print(f"✅ Synced {len(updated)} files to and from {args.csv.name}")
else:
    print("No changes detected.")
