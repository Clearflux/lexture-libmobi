#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Offline, certificate-signed regression for the DRM-free libmobi contract."""
import argparse
import ctypes
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from verify_libmobi_no_drm import verify

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = "Apple Development"
TEAM = None
EXCLUDED = {"encryption.c", "sha1.c", "randombytes.c"}


def palmdoc(encryption=0):
    """Original synthetic PalmDOC fixture; contains no encrypted book content."""
    text = b"<html><body><p>Lexture DRM-free fixture.</p></body></html>"
    header = bytearray(78)
    header[:20] = b"Lexture test fixture"
    header[60:68] = b"TEXtREAd"
    struct.pack_into(">H", header, 76, 2)
    records = struct.pack(">II", 96, 0) + struct.pack(">II", 112, 1) + b"\0\0"
    record0 = struct.pack(">HHIHHHH", 1, 0, len(text), 1, 4096, encryption, 0)
    return bytes(header) + records + record0 + text


class LibmobiNoDRMTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="lexture-no-drm-")
        cls.folder = Path(cls.temporary.name)
        cls.source = ROOT / "Sources/libmobic"
        cls.binary = cls.folder / "libmobi-test.dylib"
        # Compile the manifest's actual source inventory, not a second exclusion
        # list that could hide a future regression in Package.swift.
        package = subprocess.run(["swift", "package", "--package-path",
                                  str(cls.source.parents[1]), "describe", "--type", "json"],
                                 check=True, capture_output=True, text=True)
        target = next(t for t in json.loads(package.stdout)["targets"] if t["name"] == "libmobic")
        if EXCLUDED.intersection(target["sources"]):
            raise AssertionError("Package manifest re-enabled DRM implementation sources")
        sources = [str(cls.source / name) for name in target["sources"] if name.endswith(".c")]
        subprocess.run(["xcrun", "clang", "-dynamiclib", "-DHAVE_STRDUP", "-DUSE_XMLWRITER",
                        "-I" + str(cls.source / "include"), "-I" + str(cls.source),
                        *sources, "-lz", "-o", str(cls.binary)], check=True,
                       capture_output=True)
        # Never execute/load an ad-hoc signed local native test product.
        subprocess.run(["codesign", "--force", "--sign", IDENTITY, str(cls.binary)],
                       check=True, capture_output=True)
        requirement = '=anchor apple generic'
        if TEAM:
            if not TEAM.isalnum():
                raise ValueError("The signing team must contain only letters and numbers")
            requirement += f' and certificate leaf[subject.OU] = "{TEAM}"'
        subprocess.run(["codesign", "--verify", "--strict", "-R", requirement,
                        str(cls.binary)], check=True, capture_output=True)
        cls.lib = ctypes.CDLL(str(cls.binary))
        cls.lib.mobi_init.restype = ctypes.c_void_p
        cls.lib.mobi_free.argtypes = [ctypes.c_void_p]
        cls.lib.mobi_load_file.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        cls.lib.mobi_drm_setkey.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        cls.lib.mobi_has_drmkey.argtypes = [ctypes.c_void_p]
        cls.lib.mobi_has_drmkey.restype = ctypes.c_bool
        cls.lib.mobi_get_rawml.argtypes = [ctypes.c_void_p, ctypes.c_char_p,
                                         ctypes.POINTER(ctypes.c_size_t)]
        cls.libc = ctypes.CDLL(None)
        cls.libc.fopen.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        cls.libc.fopen.restype = ctypes.c_void_p
        cls.libc.fclose.argtypes = [ctypes.c_void_p]

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def load(self, flag):
        fixture = self.folder / f"flag-{flag}.mobi"
        fixture.write_bytes(palmdoc(flag))
        data = self.lib.mobi_init()
        self.assertTrue(data)
        file = self.libc.fopen(bytes(fixture), b"rb")
        self.assertTrue(file)
        try:
            result = self.lib.mobi_load_file(data, file)
        finally:
            self.libc.fclose(file)
        self.addCleanup(self.lib.mobi_free, data)
        return result, data

    def test_plain_palmdoc_still_loads_and_extracts(self):
        result, data = self.load(0)
        self.assertEqual(result, 0)
        text = ctypes.create_string_buffer(4096)
        size = ctypes.c_size_t(4096)
        self.assertEqual(self.lib.mobi_get_rawml(data, text, ctypes.byref(size)), 0)
        self.assertIn(b"Lexture DRM-free fixture.", text.value)

    def test_legacy_and_current_drm_flags_are_rejected(self):
        for flag in (1, 2, 3, 65535):
            with self.subTest(flag=flag):
                result, _ = self.load(flag)
                self.assertEqual(result, 5, "MOBI_FILE_ENCRYPTED required")

    def test_no_key_recovery_or_decryption_capability(self):
        _, data = self.load(0)
        self.assertFalse(self.lib.mobi_has_drmkey(data))
        self.assertEqual(self.lib.mobi_drm_setkey(data, None), 13)
        self.assertEqual(self.lib.mobi_drm_setkey(data, b"invalid"), 13)

    def test_binary_contains_no_drm_algorithms(self):
        self.assertEqual(verify(self.binary)["drm_implementations"], 0)

    def test_build_refuses_encryption_flag(self):
        result = subprocess.run(["xcrun", "clang", "-DUSE_ENCRYPTION", "-fsyntax-only",
                                 "-x", "c", "-I" + str(self.source / "include"), "-"],
                                input='#include "mobi.h"\n', text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be built without DRM", result.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--signing-identity", default=IDENTITY)
    parser.add_argument("--signing-team", help="Optional Apple development team identifier")
    args = parser.parse_args()
    ROOT, IDENTITY, TEAM = args.root.resolve(), args.signing_identity, args.signing_team
    unittest.main(argv=[__file__, "-v"])
