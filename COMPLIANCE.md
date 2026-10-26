# Source availability and app integration

This repository supplies the modified library source and its Swift wrapper,
not the source of the entire Lexture application. Source publication is one
part of the distributor's obligations, not an automatic compliance certificate.

## Library source publication

- Preserve original copyrights, licenses, and warranty disclaimers.
- Identify Lexture's modifications and their dates.
- Provide the source actually used for each distributed binary, including
  relevant build/interface files and build instructions.
- Identify the corresponding immutable source tag or commit beside the binary
  distribution and in the app's Sources & Licenses screen. Keep older matching
  sources accessible when the library changes; a pointer to the unmodified
  upstream project is not a substitute for this fork's source.

## Combined-app requirements to verify separately

GNU LGPLv3 section 4 addresses combined works. The app distributor must also
check, among other applicable requirements:

- Prominent notice that the library is used, with copies of LGPLv3 and GPLv3.
- Terms that do not restrict modification of the library portions or reverse
  engineering for debugging those modifications.
- A suitable shared-library mechanism that operates with an interface-compatible
  modified library, **or** the corresponding-source/application-code path
  specified in section 4(d)(0). Merely selecting `.dynamic` in SwiftPM is not
  proof that a shipped app permits replacement.
- Any required installation information under section 4(e), taking account of
  signing, entitlements, distribution restrictions, and the actual supported
  platform. Do not represent an untested replacement or re-signing procedure
  as working, and never publish private signing keys or certificates.

This repository does not yet supply or certify a complete iOS/macOS app
replacement, re-signing, or relinking workflow. That integration must be
validated against the specific app binary and distribution terms before
claiming that all LGPL distribution obligations have been satisfied.

Authoritative license texts:

- [GNU LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.html)
- [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)

This notice is technical compliance documentation, not legal advice or a
guarantee of compatibility with a particular app store's terms.
