# Runnable documentation samples

Each directory contains an executable consumer project for one public quickstart or scenario. The projects use central package management in `Directory.Packages.props`, declare every direct VersaTul dependency, and target `net8.0`, `net9.0`, and `net10.0`.

The central file pins released packages for normal documentation builds. Release validation replaces it with a temporary central package file and restores these projects from the `.nupkg` files packed from the current source. SQL uses a shared in-memory SQLite database, MongoDB validates its class map without a server, and Mailer sends to a local SMTP test server; no production service or credentials are required.
