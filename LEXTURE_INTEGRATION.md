# Lexture integration

This directory vendors `awxkee/libmobi-swift` at commit
`bbe180f247527f24be18526856a35473a2ad3fe6` (2026-02-04). Its C sources are
derived from `bfabiszewski/libmobi` and remain under LGPL-3.0-or-later; the
Swift wrapper is distributed under CC0-1.0.

The `libmobi` product is built as a dynamic library and declares the macOS
deployment platform in addition to iOS.

## DRM-free-only integration (2026-10-25)

- The package excludes `encryption.c/.h`, `sha1.c/.h`, and `randombytes.c/.h`
  from the C target. The original files remain here only as upstream source
  provenance; they are not compiled, copied into the app, or linked.
- `include/mobi.h` rejects `USE_ENCRYPTION` at compile time and no longer
  advertises the removed encrypt/decrypt functions. Existing compatibility
  key-management functions in `util.c` remain unsupported stubs, not algorithms.
- `read.c` rejects every nonzero PalmDOC/MOBI encryption flag before conversion,
  rather than attempting legacy type-1 key recovery.
- DRM-free PalmDOC, MOBI/KF7, KF8/AZW3 parsing, decompression, resources, font
  format obfuscation and EPUB reconstruction are retained. PDF handling and
  SQLCipher are separate app dependencies and are not included in this repository.

Run `scripts/test_libmobi_no_drm.py` for the fail-closed C contract and
`scripts/verify_libmobi_no_drm.py --binary PATH` on each built framework.

The modified library source is published in this repository. The Lexture app
also includes the LGPL, GPL, wrapper, and miniz license texts in Sources &
Licenses. Source publication does not alone verify the app's combined-work
obligations; see `COMPLIANCE.md`.
