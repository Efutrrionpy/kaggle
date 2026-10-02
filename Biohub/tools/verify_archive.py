"""Verify the small public archive without network, GPU or competition data."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifest.json").read_text())
    expected = {item["path"]: item for item in manifest["files"]}
    generated = {".repro-venv", "__pycache__", ".pytest_cache"}
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*")
              if p.is_file() and not generated.intersection(p.relative_to(root).parts)}
    actual.discard("manifest.json")
    if actual != set(expected):
        raise SystemExit(f"File-set mismatch: missing={set(expected)-actual}, extra={actual-set(expected)}")
    for relative, item in expected.items():
        p = root / relative
        if p.is_symlink() or root not in p.resolve().parents:
            raise SystemExit(f"Unsafe archive path: {relative}")
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        if p.stat().st_size != item["bytes"] or digest != item["sha256"]:
            raise SystemExit(f"Integrity mismatch: {relative}")
    print(json.dumps({"status": "PASS", "verified_files": len(expected)}, sort_keys=True))


if __name__ == "__main__":
    main()
