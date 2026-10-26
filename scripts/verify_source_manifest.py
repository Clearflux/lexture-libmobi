#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Verify the library source inventory against the published snapshot hashes."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "SOURCE_MANIFEST.json").read_text())
expected = {item["path"] for item in manifest["files"]}
actual = {"Package.swift", "LICENSE.md"}
for directory in ("Sources", "Tests"):
    actual.update(str(path.relative_to(root)) for path in (root / directory).rglob("*") if path.is_file())
if expected != actual:
    raise SystemExit(f"Inventory mismatch: missing={expected - actual}, added={actual - expected}")
for item in manifest["files"]:
    path = root / item["path"]
    if path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
        raise SystemExit(f"Source mismatch: {item['path']}")
print(f"Verified {len(expected)} files for {manifest['snapshot']}")
