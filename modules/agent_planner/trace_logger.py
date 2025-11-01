from pathlib import Path
import json, time

class TraceLogger:
    def __init__(self, log_dir: str):
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        self.fp = Path(log_dir) / f"trace_{int(time.time())}.jsonl"

    def write(self, record: dict):
        with self.fp.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
