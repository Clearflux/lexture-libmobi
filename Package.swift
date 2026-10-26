// swift-tools-version: 5.7
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "libmobi",
    platforms: [.iOS(.v14), .macOS(.v11)],
    products: [
        .library(
            name: "libmobi",
            type: .dynamic,
            targets: ["libmobi"]),
    ],
    dependencies: [
        // Dependencies declare other packages that this package depends on.
        // .package(url: /* package url */, from: "1.0.0"),
    ],
    targets: [
        .target(
            name: "libmobi",
            dependencies: ["libmobic"]),
        .target(name: "libmobic",
                // These upstream sources are retained for provenance only. None
                // of their DRM, PC1, SHA-1 or random-byte code is shipped.
                exclude: ["encryption.c", "encryption.h", "sha1.c", "sha1.h",
                          "randombytes.c", "randombytes.h"],
                publicHeadersPath: "include",
                cSettings: [.define("HAVE_CONFIG_H"), .define("HAVE_STRDUP"), .define("USE_XMLWRITER")],
                linkerSettings: [
                    .linkedLibrary("z")
                ]),
    ]
)
