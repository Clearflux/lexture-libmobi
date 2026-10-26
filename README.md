# Lexture libmobi

Source for the libmobi library and Swift wrapper used by Lexture, including
Lexture's local changes. This repository is published by Hangzhou Clearflux
Information Technology Co., Ltd.

This is not the source code of the Lexture app. It contains no dictionary data,
user books, app credentials, signing certificates, or private keys.

## Origin and changes

- C library: [bfabiszewski/libmobi](https://github.com/bfabiszewski/libmobi),
  copyright (c) 2014–2022 Bartek Fabiszewski, LGPL-3.0-or-later.
- Vendored source and Swift wrapper:
  [awxkee/libmobi-swift](https://github.com/awxkee/libmobi-swift) at commit
  [`bbe180f247527f24be18526856a35473a2ad3fe6`](https://github.com/awxkee/libmobi-swift/tree/bbe180f247527f24be18526856a35473a2ad3fe6).
- Lexture changes: dynamic library packaging for iOS and macOS, and fail-closed
  rejection of DRM-encrypted input. See [CHANGES.md](CHANGES.md) and
  [LEXTURE_INTEGRATION.md](LEXTURE_INTEGRATION.md).
- The compiled input files under `Sources/` and `Package.swift` are copied
  byte-for-byte from Lexture's vendored library. `SOURCE_MANIFEST.json` records
  their SHA-256 hashes. Original files excluded from compilation are retained
  for provenance and are explicitly identified in `Package.swift`.

## Supported use

The library parses DRM-free PalmDOC, MOBI/KF7, and KF8/AZW3 content and can
extract resources and reconstruct EPUB content. DRM-encrypted input is
rejected; this fork does not provide a DRM removal feature. File extensions
alone do not establish whether a book is supported.

## Licenses

This repository contains multiple licenses. The wrapper's upstream CC0 license
does **not** relicense the C library.

| Component | License / notice |
| --- | --- |
| libmobi C library and Lexture changes to it | [LGPL-3.0-or-later](COPYING.LESSER), together with [GPLv3](COPYING) |
| Upstream Swift wrapper | [CC0-1.0](LICENSES/CC0-1.0.txt); original upstream [LICENSE.md](LICENSE.md) is preserved |
| Bundled miniz | [Unlicense](LICENSES/Unlicense.txt), also preserved in source headers |
| New repository documentation and regression scripts | CC0-1.0, except third-party notices and license texts, which retain their original terms |

Copyright and license notices in individual source files remain authoritative.
The software is provided without warranty, as described in those licenses.

## Build

Install Apple's Xcode command-line tools and select the desired Xcode with
`xcode-select`. This snapshot was checked with Xcode 27.1 / Apple Swift 6.4
on Apple silicon. The package declares iOS 14 and macOS 11 as minimum library
platforms; this does not describe Lexture's own deployment requirements.

```sh
git clone git@github.com:Clearflux/lexture-libmobi.git
cd lexture-libmobi
swift build --configuration release
```

On macOS this produces `.build/release/liblibmobi.dylib` (the exact build path
can be obtained with `swift build --configuration release --show-bin-path`).
SwiftPM resolves the system zlib dependency; this package has no external Swift
package dependencies. The dynamic product includes both the Swift wrapper and
the C implementation. Use Xcode / SwiftPM to build for an iOS destination.

Before running a locally built native library, sign it with your own
certificate-backed Apple code-signing identity. Do not use an ad-hoc identity:

```sh
codesign --force --sign "Apple Development" .build/release/liblibmobi.dylib
codesign --verify --strict -R '=anchor apple generic' .build/release/liblibmobi.dylib
python3 scripts/verify_libmobi_no_drm.py --binary .build/release/liblibmobi.dylib
```

The offline regression compiles its own C test library, signs it with the
supplied identity, and verifies its Apple certificate chain before loading it:

```sh
python3 scripts/test_libmobi_no_drm.py --signing-identity "Apple Development"
```

It uses an original synthetic PalmDOC fixture, not a copyrighted book. It
checks plain-text extraction, rejection of nonzero encryption flags, unsupported
key-management stubs, absence of DRM algorithm symbols, and refusal to compile
with `USE_ENCRYPTION`.

## Release/source correspondence

The `lexture-source-2026-10-26` tag identifies the library source snapshot
prepared on 26 October 2026. It is a source snapshot, **not** a claim that an
App Store release with these exact bytes has already shipped. Future binary
releases must identify their exact matching source tag / commit and keep that
source available. Do not move or overwrite published source tags.

Publishing this repository provides access to this library's source. It does
not, by itself, establish compliance with every requirement for distributing
a combined app. See [COMPLIANCE.md](COMPLIANCE.md) for the remaining integration
checks, including replacement / relinking and any required installation
information.
