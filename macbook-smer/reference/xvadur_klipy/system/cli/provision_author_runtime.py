#!/usr/bin/env python3
"""Provision the versioned authoring dependency graph without touching shared npm.

Existing valid runtimes are verified, never reinstalled or replaced. An absent
runtime is built in a sibling temporary directory and published only after checks.
"""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from author_runtime import validate_runtime

def provision(project_root: Path, run=subprocess.run, npm_binary: str = "npm") -> dict:
    project_root = project_root.resolve()
    source = project_root / "system/runtime/authoring-4.0.529"
    target = project_root / "system/.cache/authored-runtime/4.0.529"
    for name in ("package.json", "package-lock.json"):
        if not (source / name).is_file():
            raise RuntimeError(f"Missing versioned authoring runtime descriptor: {source / name}")
    if target.exists():
        identity = validate_runtime(target, source)
        return {"status": "verified_existing", "runtimeRoot": str(target), **identity}
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".provision-4.0.529-", dir=target.parent))
    try:
        for name in ("package.json", "package-lock.json"):
            shutil.copyfile(source / name, staging / name)
        run([npm_binary, "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
            cwd=staging, check=True)
        identity = validate_runtime(staging, source)
        # A concurrently provisioned or active runtime is never replaced.
        if target.exists():
            identity = validate_runtime(target, source)
            return {"status": "verified_existing", "runtimeRoot": str(target), **identity}
        try:
            staging.rename(target)
        except OSError:
            if not target.exists():
                raise
            identity = validate_runtime(target, source)
            return {"status": "verified_existing", "runtimeRoot": str(target), **identity}
        return {"status": "provisioned", "runtimeRoot": str(target), **identity}
    finally:
        if staging.exists():
            shutil.rmtree(staging)

if __name__ == "__main__":
    try:
        print(json.dumps(provision(Path(__file__).resolve().parents[2]), indent=2))
    except (RuntimeError, OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
