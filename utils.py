# utils.py
import hashlib
import json
from pathlib import Path

LOG_PATH = Path("logs/detections.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def generate_hash(record: dict) -> str:
    # Deterministic JSON -> SHA256
    record_str = json.dumps(record, sort_keys=True, default=str)
    return hashlib.sha256(record_str.encode()).hexdigest()

def append_detection_log(record: dict):
    # append JSON line
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str, sort_keys=True) + "\n")
