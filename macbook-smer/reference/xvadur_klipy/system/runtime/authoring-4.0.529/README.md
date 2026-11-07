# Reproducible Remotion authoring runtime

This directory owns the exact dependency declarations and npm lockfile for the Remotion Reel authoring route. Its Remotion packages remain **4.0.529**, Zod **3.25.76**, React **19.3.0**, tsx **4.20.6** and TypeScript **5.9.3**. The separate `system/package.json` and its installation can evolve independently.

From the project root:

```sh
python3 system/cli/provision_author_runtime.py
python3 system/cli/klipy.py autor --help
```

Provisioning an absent runtime copies these two descriptors into a temporary sibling of `system/.cache/authored-runtime/4.0.529`, executes `npm ci --ignore-scripts --no-audit --no-fund`, verifies the installed versions and descriptor bytes, then atomically publishes the directory. It requires Node, npm and access to the packages or a populated npm cache. An existing valid runtime is only verified; it is not reinstalled. An existing inconsistent runtime is rejected and never silently replaced, including while another render might use it. No shared project dependencies are changed.

The normal Python CLI dispatches `autor` before loading the shared TypeScript entry. It uses the isolated tsx/Zod/Remotion installation and a content-hashed, immutable source snapshot. The snapshot holds authoring pipeline/schema/scene/renderer/runtime sources and copies of these dependency descriptors. Canonical media and episode artifacts stay in the real project; they are not copied into the runtime. Render receipts record the runtime source, package and lock hashes. Updating application source creates a new snapshot for the next invocation without mutating a running one.

If the disposable runtime cache is absent, the provision command above reconstructs it from this directory. Bootstrap never falls back to an incompatible shared installation. Native browser/FFmpeg prerequisites remain the same as the existing renderer.

Bootstrap and provisioning regression tests:

```sh
python3 -m unittest system/tests/test_author_runtime.py
```

The tests cover a concurrent shared Remotion/Zod upgrade, source snapshot preservation, refusal of altered dependencies/snapshots, an existing-runtime no-op, staged provisioning and cleanup of an interrupted installation. The fake-installer tests check orchestration; they are not a claim of a fresh network installation.
