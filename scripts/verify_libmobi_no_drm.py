#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Reject DRM/password algorithms accidentally linked into Lexture's libmobi."""
import argparse
from pathlib import Path
import re
import subprocess


def verify(binary):
    binary = Path(binary)
    if not binary.is_file():
        raise ValueError(f"Missing libmobi binary: {binary}")
    symbols = subprocess.run(["/usr/bin/nm", str(binary)], check=True,
                             capture_output=True, text=True).stdout
    for required in ("_mobi_load_file", "_mobi_parse_rawml"):
        if not re.search(r"\b[Tt] " + re.escape(required) + r"$", symbols, re.M):
            raise ValueError(f"Not a complete libmobi parser: {required} missing")
    forbidden = re.compile(
        r"\b_?(?:mobi_(?:pk1\w*|drmkey_\w*|drm_(?:encrypt|decrypt)\w*|"
        r"randombytes\w*)|SHA1\w*|sha1\w*)$", re.M)
    found = sorted(set(forbidden.findall(symbols)))
    if found:
        raise ValueError(f"DRM/crypto implementation leaked into libmobi: {found}")
    return {"binary": str(binary), "drm_implementations": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True, type=Path)
    args = parser.parse_args()
    print(verify(args.binary))


if __name__ == "__main__":
    main()
