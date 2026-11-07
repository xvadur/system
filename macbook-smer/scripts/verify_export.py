"""Check the original handoff bytes; run before making local edits."""

from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "context/EXPORT_MANIFEST.json").read_text())
failures = []
for entry in manifest["files"]:
    relative = Path(entry["path"])
    if relative.is_absolute() or ".." in relative.parts:
        failures.append(f"Invalid path: {relative}")
        continue
    path = root / relative
    if not path.is_file():
        failures.append(f"Missing: {relative}")
        continue
    if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
        failures.append(f"Changed: {relative}")

if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"Verified {len(manifest['files'])} original handoff files.")
