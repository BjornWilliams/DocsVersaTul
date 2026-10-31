# Documentation Validation

This repository uses Sphinx to build the VersaTul library documentation.

The content rewrite, internal link audit, and strict Sphinx HTML validation have been completed.

## Validation Goal

Use this checklist when you want to validate the documentation end to end after content changes.

## Pull request validation

The `.github/workflows/documentation-samples.yml` workflow runs for every pull
request. Its required `Build, run, and check sample output` job validates the
snippet inventory, installs the exact dependencies in `docs/requirements.txt`,
runs the strict Sphinx command below, then builds and checks the published-package
samples. The `main` branch requires this status check before merge.

The independent `Check external documentation links` job checks external HTTP
and HTTPS links in `README.rst` and `docs/source`. It uses lychee v0.24.2 with
retry settings from `lychee.toml`; it is not a required branch-protection check,
so an unavailable external site does not block documentation authoring.

## Prerequisites

1. Python 3.12 installed. Read the Docs and the pull-request workflow both select Python 3.12.
2. `pip` available.
3. The dependencies from `docs/requirements.txt` installed in the active environment.

## Recommended Local Setup

From the repository root:

```console
python --version
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r docs/requirements.txt
```

## Build Commands

### Standard HTML build

From the repository root:

```console
cd docs
make.bat html
```

Or run Sphinx directly:

```console
cd docs
python -m sphinx -b html source build/html
```

### Strict validation build

This is the preferred verification pass after documentation edits because it treats warnings as errors and enables stricter checks.

```console
cd docs
python -m sphinx -n -W --keep-going -b html source build/html
```

Meaning of the flags:

1. `-n` enables nitpicky mode for stricter cross-reference validation.
2. `-W` turns warnings into build failures.
3. `--keep-going` reports more than the first warning.

Read the Docs uses the same warning policy. The root `.readthedocs.yaml` enables
`sphinx.fail_on_warning`, which adds `-W --keep-going`; `nitpicky = True` in
`docs/source/conf.py` supplies the cross-reference checks enabled locally by `-n`.
This keeps missing references and other Sphinx warnings fatal in both builds.

## What To Check

After the build:

1. Confirm the HTML output exists under `docs/build/html`.
2. Open `docs/build/html/index.html` and spot-check navigation.
3. Confirm package pages render code blocks, tables, and toctrees correctly.
4. Confirm no warnings were produced in strict mode.

## Typical Failure Categories

1. Missing `:doc:` targets.
2. Invalid toctree entries.
3. Malformed reStructuredText tables or headings.
4. Unknown directives or missing Sphinx extensions.
5. Broken indentation inside code blocks.

## Quick Triage Order

When the build fails:

1. Fix missing references first.
2. Fix heading and section structure next.
3. Fix malformed tables and literal blocks after that.
4. Re-run the strict build until it completes cleanly.

## Toolchain parity

The hosted build and pull-request workflow both use Python 3.12. The exact Sphinx
version, 9.1.0, and the theme/search extensions are pinned in
`docs/requirements.txt`. Use Python 3.12 locally and install that requirements
file to validate with the same toolchain.

If `python` resolves only to the Microsoft Store alias on Windows, use the registered interpreter path instead of the alias when creating or invoking the local virtual environment.

The validated strict build command was:

```console
cd docs
..\.venv\Scripts\python.exe -m sphinx -n -W --keep-going -b html source build/html
```
