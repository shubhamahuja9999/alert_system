# utils.py
import hashlib
import json

def generate_hash(record: dict) -> str:
    """Generate SHA256 hash for tamper-proof logging."""
    record_str = json.dumps(record, sort_keys=True, default=str)
    return hashlib.sha256(record_str.encode()).hexdigest()
