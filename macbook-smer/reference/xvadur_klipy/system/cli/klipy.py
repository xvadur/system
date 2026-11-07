#!/usr/bin/env python3
"""One entry point; canonical logic and schemas live in the TypeScript pipeline."""
from pathlib import Path
import os
import shutil
import sys

root = Path(__file__).resolve().parents[2]
node = shutil.which("node")
if len(sys.argv) > 1 and sys.argv[1] == "autor":
    from author_runtime import prepare_launch
    if not node:
        sys.exit("Node is missing")
    try:
        launch = prepare_launch(root)
    except (RuntimeError, OSError, ValueError) as error:
        sys.exit(str(error))
    os.chdir(root)
    os.execve(node, [node, "--import", launch["loader"], launch["entry"], *sys.argv[1:]],
              {**os.environ, **launch["env"]})
tsx = root / "system/node_modules/tsx/dist/loader.mjs"
if not node or not tsx.is_file():
    sys.exit("Runtime is missing. Run: python3 system/bootstrap.py")
os.chdir(root)
os.execv(node, [node, "--import", str(tsx), str(root / "system/cli/main.ts"), *sys.argv[1:]])
