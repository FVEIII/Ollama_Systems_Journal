import csv
import yaml
from pathlib import Path
from datetime import datetime

csv_path = Path("frontmatter_dashboard.csv")

def load_yaml_frontmatter(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != '---':
        return {}, lines

    try:
        end_index = lines[1:].index('---\n') + 1
        yaml_block = ''.join(lines[1:end_index])
        rest_of_file = lines[end_index + 1:]
        return yaml.safe_load(yaml_block) or {}, rest_of_file
    except ValueError:
        # End of frontmatter not found
        return {}, lines

def write_yaml_frontmatter(md_file, frontmatter, content_lines):
    yaml_block = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(yaml_block)
        f.write('---\n')
        f.writelines(content_lines)

def sync():
    updated_rows = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for row in rows:
        md_file = Path(row["file_path"])

        if not md_file.exists():
            print(f"⚠️ File not found: {md_file}")
            continue

        frontmatter, body = load_yaml_frontmatter(md_file)

        # Update YAML from CSV row
        for key, value in row.items():
            if key == "file_path":
                continue
            if key == "related_loops":
                try:
                    frontmatter[key] = eval(value) if value else []
                except Exception:
                    frontmatter[key] = []
            else:
                frontmatter[key] = value if value else None

        # Update last_updated timestamp
        frontmatter["last_updated"] = datetime.now().strftime("%Y-%m-%d")

        write_yaml_frontmatter(md_file, frontmatter, body)

        # Build CSV row from updated frontmatter
        synced_row = {"file_path": str(md_file)}
        for key in row:
            if key == "file_path":
                continue
            value = frontmatter.get(key, "")
            if isinstance(value, list):
                synced_row[key] = str(value)
            elif isinstance(value, datetime):
                synced_row[key] = value.strftime("%Y-%m-%d")
            else:
                synced_row[key] = str(value) if value is not None else ""

        updated_rows.append(synced_row)

    # Save back to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = updated_rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"✅ Synced {len(updated_rows)} files to and from frontmatter_dashboard.csv")

if __name__ == "__main__":
    sync()
