import csv
import yaml
import logging
from pathlib import Path
from datetime import datetime

# Constants
CSV_PATH = Path("frontmatter_dashboard.csv")
YAML_DELIMITER = "---"
KEY_FILE_PATH = "file_path"
KEY_LAST_UPDATED = "last_updated"
KEY_RELATED_LOOPS = "related_loops"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def load_yaml_frontmatter(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != YAML_DELIMITER:
        return {}, lines

    try:
        end_index = lines[1:].index(f"{YAML_DELIMITER}\n") + 1
        yaml_block = "".join(lines[1:end_index])
        rest_of_file = lines[end_index + 1:]
        return yaml.safe_load(yaml_block) or {}, rest_of_file
    except ValueError:
        logger.warning(f"No closing frontmatter in: {md_file}")
        return {}, lines

def write_yaml_frontmatter(md_file, frontmatter, content_lines):
    yaml_block = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True)
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"{YAML_DELIMITER}\n")
        f.write(yaml_block)
        f.write(f"{YAML_DELIMITER}\n")
        f.writelines(content_lines)

def sync():
    updated_rows = []

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for row in rows:
        md_file = Path(row[KEY_FILE_PATH])

        if not md_file.exists():
            logger.warning(f"File not found: {md_file}")
            continue

        frontmatter, body = load_yaml_frontmatter(md_file)

        # Detect changes
        changes = {}
        for key, value in row.items():
            if key == KEY_FILE_PATH:
                continue

            old_value = frontmatter.get(key, "")
            new_value = eval(value) if key == KEY_RELATED_LOOPS and value else value

            if isinstance(old_value, list):
                old_value = sorted(old_value)
            if isinstance(new_value, list):
                new_value = sorted(new_value)

            if old_value != new_value:
                changes[key] = (old_value, new_value)

        if changes:
            logger.info(f"Changes detected in {md_file}:")
            for field, (old, new) in changes.items():
                logger.info(f"  • {field}: {old} → {new}")

            # Update frontmatter
            for key, value in row.items():
                if key == KEY_FILE_PATH:
                    continue
                if key == KEY_RELATED_LOOPS:
                    try:
                        frontmatter[key] = eval(value) if value else []
                    except Exception:
                        frontmatter[key] = []
                else:
                    frontmatter[key] = value if value else None

            frontmatter[KEY_LAST_UPDATED] = datetime.now().strftime("%Y-%m-%d")
            write_yaml_frontmatter(md_file, frontmatter, body)

            # Build row
            synced_row = {KEY_FILE_PATH: str(md_file)}
            for key in row:
                if key == KEY_FILE_PATH:
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
    if updated_rows:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = updated_rows[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

    logger.info(f"✅ Synced {len(updated_rows)} files to and from {CSV_PATH.name}")

if __name__ == "__main__":
    sync()

