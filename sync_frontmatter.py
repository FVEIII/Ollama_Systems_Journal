import os
import yaml
import csv

TARGET_DIR = 'prompts/coffee_sim/data'
OUTPUT_CSV = 'frontmatter_dashboard.csv'

def extract_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines[0].strip() != '---':
            return {}
        yaml_lines = []
        for line in lines[1:]:
            if line.strip() == '---':
                break
            yaml_lines.append(line)
        try:
            return yaml.safe_load(''.join(yaml_lines)) or {}
        except yaml.YAMLError:
            return {}

def collect_frontmatter():
    records = []
    for root, _, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.md'):
                rel_path = os.path.join(root, file)
                data = extract_frontmatter(rel_path)
                data['file_path'] = rel_path.replace('\\', '/')
                records.append(data)
    return records

def write_csv(records):
    if not records:
        return
    keys = sorted({k for r in records for k in r})
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)

if __name__ == '__main__':
    fm_records = collect_frontmatter()
    write_csv(fm_records)
    print(f"✓ Synced {len(fm_records)} files into {OUTPUT_CSV}")
