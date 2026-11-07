"""Freeze authoring code and resolve only its separately installed dependencies.

No npm install, global package changes, media copy or account changes happen here.
The package owner provisions system/.cache/authored-runtime/4.0.529 independently.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

VERSION = "authored-cli-runtime.v1"
REQUIRED = {"remotion": "4.0.529", "@remotion/renderer": "4.0.529",
            "@remotion/bundler": "4.0.529", "@remotion/cli": "4.0.529",
            "@remotion/media": "4.0.529", "@remotion/lottie": "4.0.529",
            "react": "19.3.0", "react-dom": "19.3.0", "zod": "3.25.76",
            "tsx": "4.20.6", "typescript": "5.9.3"}
SOURCE_DIRS = ("pipeline", "schemas", "scenes", "providers", "renderer", "runtime")
SOURCE_EXTENSIONS = {".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".json", ".py"}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def validate_runtime(runtime: Path, descriptors: Path | None = None) -> dict:
    package_path, lock_path = runtime / "package.json", runtime / "package-lock.json"
    if not package_path.is_file() or not lock_path.is_file():
        raise RuntimeError(f"Pinned authoring runtime is not provisioned: {runtime}.\nRun: python3 system/cli/provision_author_runtime.py\nNo shared-runtime fallback.")
    if descriptors is not None:
        for name in ("package.json", "package-lock.json"):
            expected = descriptors / name
            if not expected.is_file() or expected.read_bytes() != (runtime / name).read_bytes():
                raise RuntimeError(f"Isolated authoring descriptor differs from versioned source: {name}; existing dependencies were not changed.")
    package = json.loads(package_path.read_text())
    declared = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
    lock = json.loads(lock_path.read_text())
    for name, expected in REQUIRED.items():
        installed_path = runtime / "node_modules" / name / "package.json"
        installed = json.loads(installed_path.read_text()) if installed_path.is_file() else {}
        locked = lock.get("packages", {}).get("node_modules/" + name, {})
        if declared.get(name) != expected or installed.get("version") != expected or locked.get("version") != expected:
            raise RuntimeError(f"Isolated authoring dependency mismatch: {name}; expected {expected}. Shared dependencies will not be used.")
    loader = runtime / "node_modules/tsx/dist/loader.mjs"
    if not loader.is_file():
        raise RuntimeError("Isolated tsx loader is missing")
    return {"packageHash": sha(package_path.read_bytes()), "lockHash": sha(lock_path.read_bytes()), "dependencies": REQUIRED}

def collect_sources(project_root: Path, runtime: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for directory in SOURCE_DIRS:
        base = project_root / "system" / directory
        for folder, dirs, names in os.walk(base):
            dirs[:] = sorted(d for d in dirs if d not in {"node_modules", ".cache", "__pycache__", "public"})
            for name in sorted(names):
                source = Path(folder) / name
                if source.suffix not in SOURCE_EXTENSIONS:
                    continue
                if source.is_symlink():
                    raise RuntimeError(f"Source snapshot refuses symlink: {source}")
                files[source.relative_to(project_root).as_posix()] = source.read_bytes()
    for name in ("author.ts", "author_runtime.py", "klipy.py", "provision_author_runtime.py"):
        source = project_root / "system/cli" / name
        files[source.relative_to(project_root).as_posix()] = source.read_bytes()
    # Never copy the shared package/lock: another task may have upgraded it.
    files["system/package.json"] = (runtime / "package.json").read_bytes()
    files["system/package-lock.json"] = (runtime / "package-lock.json").read_bytes()
    return files

def prepare_launch(project_root: Path, runtime: Path | None = None) -> dict:
    project_root = project_root.resolve()
    runtime = (runtime or project_root / "system/.cache/authored-runtime/4.0.529").resolve()
    identity = validate_runtime(runtime, project_root / "system/runtime/authoring-4.0.529")
    files = collect_sources(project_root, runtime)
    file_hashes = [{"path": key, "hash": sha(value)} for key, value in sorted(files.items())]
    snapshot_hash = sha(json.dumps({"version": VERSION, "files": file_hashes}, sort_keys=True, separators=(",", ":")).encode())
    snapshots = runtime / "snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)
    snapshot = snapshots / snapshot_hash
    manifest = {"version": VERSION, "snapshotHash": snapshot_hash, **identity, "files": file_hashes}
    if not snapshot.exists():
        pending = Path(tempfile.mkdtemp(prefix=".pending-", dir=snapshots))
        try:
            for relative, data in files.items():
                target = pending / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                target.chmod(0o444)
            (pending / "runtime-source.json").write_text(json.dumps(manifest, indent=2) + "\n")
            (pending / "runtime-source.json").chmod(0o444)
            try:
                pending.rename(snapshot)
            except OSError:
                if not snapshot.exists():
                    raise
        finally:
            if pending.exists():
                shutil.rmtree(pending)
    # Reject drift in cached snapshots before executing a single JS import.
    for item in file_hashes:
        if sha((snapshot / item["path"]).read_bytes()) != item["hash"]:
            raise RuntimeError(f"Immutable authoring runtime source changed: {item['path']}")
    if json.loads((snapshot / "runtime-source.json").read_text()) != manifest:
        raise RuntimeError("Immutable authoring runtime manifest changed")
    return {"loader": str(runtime / "node_modules/tsx/dist/loader.mjs"),
            "entry": str(snapshot / "system/cli/author.ts"),
            "env": {"XVADUR_PROJECT_ROOT": str(project_root),
                    "XVADUR_AUTHORED_RUNTIME_ROOT": str(runtime),
                    "XVADUR_AUTHORED_SOURCE_ROOT": str(snapshot / "system"),
                    "XVADUR_AUTHORED_RUNTIME_MANIFEST": str(snapshot / "runtime-source.json")},
            "identity": manifest}
