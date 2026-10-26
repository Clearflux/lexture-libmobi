# Changes from upstream

Upstream wrapper/source snapshot:
`awxkee/libmobi-swift@bbe180f247527f24be18526856a35473a2ad3fe6`.

## 2026-10-25 — Lexture integration

- `Package.swift`: explicitly build the Swift product as a dynamic library,
  declare macOS in addition to iOS, and exclude upstream encryption, SHA-1,
  and random-byte implementation files from the C target.
- `Sources/libmobic/include/mobi.h`: reject `USE_ENCRYPTION` and remove public
  declarations for removed encryption/decryption operations.
- `Sources/libmobic/read.c`: reject nonzero PalmDOC/MOBI encryption flags before
  conversion; do not attempt legacy key recovery.
- The upstream `Sources/libmobic/util.c` key-management compatibility stubs are
  retained unchanged; they are not replacement cryptographic implementations.
- Keep parsing, decompression, resources, and EPUB reconstruction for DRM-free
  input. Retain excluded upstream files for provenance only.

## 2026-10-26 — Corresponding-source publication preparation

- Publish the exact current vendored `Package.swift`, `Sources/`, and upstream
  placeholder tests; do not change their runtime behavior for this repository.
- Add the full LGPLv3 and GPLv3 texts, preserve the wrapper's CC0 license, and
  include the bundled miniz Unlicense notice.
- Add source hashes, build instructions, and standalone fail-closed regression
  scripts adapted from Lexture's local tests. The regression scripts accept the
  user's signing identity and optional team instead of hard-coding a team.
- Replace the upstream introductory README with fork-specific documentation;
  describe the source-publication and app-integration obligations separately.
