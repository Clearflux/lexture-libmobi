# Integration checks — 26 October 2026

This record documents completed technical tests, not a legal compliance
certificate. The production library source remains the immutable
`lexture-source-2026-10-26` snapshot. The temporary probe below was used only
in private test builds and was not added to that snapshot or shipped in Lexture.

## What was tested

1. Build the published library source with Xcode 27.1 / Swift 6.4 after adding
   a temporary, recognizable stderr marker to `mobi_load_file`. The marker
   changes neither the public interface nor the parsing result.
2. Replace the embedded `libmobi.framework` binary in an isolated copy of the
   Lexture test host. Do not relink its application logic against a different
   library interface.
3. Preserve the framework's dynamic-library install name, and sign the modified
   framework and copied app with a certificate-backed Apple development identity.
4. Remove development-only absolute build-directory runpaths from the isolated
   test-host copies and remove Xcode's build-products framework search override.
   Otherwise a successful test can silently execute the original build-directory
   library rather than the replacement. These are test-harness changes, not
   changes to Lexture's production search-path configuration.
5. Run the app's real DRM-free MOBI/AZW3 import test and its DRM-protected-input
   rejection test. Confirm both the loader's embedded-framework path and the
   temporary marker in the actual test-process output.

## Results

| Environment | Result | Executed replacement confirmed |
| --- | --- | --- |
| Apple-silicon Mac, macOS 26.6.2 | Both import tests passed; no skips | Yes: app-embedded framework path and marker output |
| Apple-silicon iPad simulator, iOS 26.5 | Both import tests passed; no skips | Yes: installed simulator app's framework path and marker output |

Separately, source-link, notice, localization and import checks passed on both
platforms: 19 selected tests per platform, no failures or skips. These are
targeted checks, not the full Lexture regression suite.

The initial development-path test run passed its functional tests but did not
execute the marked replacement. It is **not** counted as replacement evidence.
Only the isolated-path run described above establishes that result.

## What this does not prove

- The test copies were Debug app hosts signed with the **publisher's own**
  Apple development certificate, not an unrelated end user's certificate.
- The iOS result is a simulator result, not a physical-device replacement test.
- No App Store-downloaded binary, store encryption, receipt, App Attest, iCloud,
  keychain migration, or membership-server behavior was validated by this test.
- This repository does not provide Lexture's proprietary application object
  files, application source, complete app bundle, or an end-user relinking kit.
- No signing key, provisioning profile, user book, dictionary database, or
  test-host app binary is published here.

The completed tests establish interface-compatible replacement behavior in the
stated test environments. A distribution-specific mechanism and terms still
need to be selected and validated before representing the entire combined-app
distribution as satisfying every applicable LGPL requirement.
