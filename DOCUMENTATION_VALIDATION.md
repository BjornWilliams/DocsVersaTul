# Documentation Validation

This repository uses Sphinx to build the VersaTul library documentation.

The content rewrite, internal link audit, and strict Sphinx HTML validation have been completed.

## Validation Goal

Use this checklist when you want to validate the documentation end to end after content changes.

## Prerequisites

1. Python 3.10 or later installed. If `python` is not on `PATH`, use the full interpreter path when creating the virtual environment.
2. `pip` available.
3. The dependencies from `docs/requirements.txt` installed in the active environment.

## Recommended Local Setup

From the repository root:

```console
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

## Current Environment Note

During the recent modernization work, strict validation completed successfully after using the real Python interpreter path directly and upgrading the docs toolchain to Python 3.14-compatible versions.

If `python` resolves only to the Microsoft Store alias on Windows, use the registered interpreter path instead of the alias when creating or invoking the local virtual environment.

The validated strict build command was:

```console
cd docs
..\.venv\Scripts\python.exe -m sphinx -n -W --keep-going -b html source build/html
```