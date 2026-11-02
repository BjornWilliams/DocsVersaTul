# Runnable documentation samples

Each directory contains an executable consumer project for one public quickstart or scenario. The projects use central package management in `Directory.Packages.props`, declare every direct VersaTul dependency, and target `net8.0`, `net9.0`, and `net10.0`.

The central file pins released packages for normal documentation builds. Release validation replaces it with a temporary central package file and restores these projects from the `.nupkg` files packed from the current source. SQL uses a shared in-memory SQLite database, MongoDB validates its class map without a server, and Mailer sends to a local SMTP test server; no production service or credentials are required.

From the VersaTul repository root, run `pwsh ./scripts/Invoke-DocumentationSamplePackageValidation.ps1` to pack the VersaTul libraries in dependency order, restore these projects from the temporary local package feed, and build and run every sample for each directly supported target framework. Pass `-DocumentationSamplesRoot` when the DocsVersaTul checkout is in a different location and `-ExternalPackageSources` when external package dependencies need a specific feed.

The `Documentation samples / Build, run, and check sample output` GitHub Actions check runs on every pull request so it can be required without leaving an unrelated change with a skipped check. Configure it as required in the DocsVersaTul repository rules so a pull request cannot merge with a failed sample build, snippet inventory, or output assertion. The public-repository check restores the released package versions pinned in `Directory.Packages.props`; the VersaTul release validator separately checks samples against locally packed current-source packages.
