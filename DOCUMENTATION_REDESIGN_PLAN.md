# VersaTul Documentation Redesign Plan

## Purpose

This plan breaks the VersaTul documentation refresh into clear, reviewable steps before any `.rst` pages are rewritten.

The goal is to produce documentation that works for:

1. Beginners who need a fast and reliable getting-started path.
2. Intermediate users who need package guidance, examples, and integration patterns.
3. Advanced users who need complete feature coverage, extension points, and implementation details.

## Current Status

Status as of 2026-03-21:

1. The documentation information architecture redesign has been completed.
2. The onboarding pages, package catalog pages, and grouped navigation are in place.
3. The duplicate FileReader page issue has been resolved.
4. The shared package-page template has been created and aligned to the rewritten docs.
5. The package rewrite pass has been completed for the library packages in scope.
6. Shared docs repository files such as `README.rst`, `pyproject.toml`, and `docs/source/conf.py` have been modernized.
7. Manual QA has been completed for internal `:doc:` links, toctree coverage, install-package naming, and common typo patterns.
8. Strict Sphinx HTML validation has been completed successfully with a local virtual environment on Python 3.14.

## Current Findings

The current documentation already has useful package pages, but it needs structural and editorial modernization.

### Issues Identified

1. The landing page is minimal and still feels like an early-stage documentation shell.
2. The documentation information architecture is flat, making discovery harder as the package count grows.
3. Some pages are outdated in tone and structure compared to the current library code.
4. Package naming is not always consistent between library names and doc filenames.
5. `VersaTul.Data.FileReader` currently has duplicate pages:
   - `docs/source/file-reader.rst`
   - `docs/source/filereader.rst`
6. The index toctree does not currently expose all existing topic pages.
7. The docs do not yet present a clear progression from beginner setup to advanced package usage.

## Library Scope To Cover

The documentation effort should focus on the NuGet-distributed library projects only.

### Foundation Packages

1. `VersaTul.Contracts`
2. `VersaTul.Configurations`
3. `VersaTul.Configuration.Defaults`
4. `VersaTul.Extensions`
5. `VersaTul.Utilities`
6. `VersaTul.Object.Converters`

### Data And Storage Packages

1. `VersaTul.Caching`
2. `VersaTul.Data.Contracts`
3. `VersaTul.Data.Bulk`
4. `VersaTul.Data.Sql`
5. `VersaTul.Data.MsSql`
6. `VersaTul.Data.MongoDB`
7. `VersaTul.Data.EFCore`
8. `VersaTul.Data.FileReader`

### File, Streaming, And Transformation Packages

1. `VersaTul.Compression`
2. `VersaTul.Collection.Streamers`
3. `VersaTul.Display.Attributes`
4. `VersaTul.Handler.File`
5. `VersaTul.Pipeline.Infrastructure`

### Communication And Scheduling Packages

1. `VersaTul.Logger`
2. `VersaTul.Logger.File`
3. `VersaTul.Logger.Mail`
4. `VersaTul.Logger.Web`
5. `VersaTul.Mailer`
6. `VersaTul.Task.Scheduler`

## Proposed Documentation Strategy

The redesign should be done in phases so each step is reviewable and the docs remain buildable throughout the work.

The phase breakdown below is retained as the implementation record for the completed modernization work.

## Phase 1: Audit And Content Inventory

### Goal

Create a trustworthy baseline of what exists today in code and docs.

### Tasks

1. Confirm the final list of library packages that should appear in the docs.
2. Map each package to its current `.rst` page.
3. Record missing topics, duplicate pages, inconsistent names, and outdated examples.
4. Identify cross-package concepts that should be documented once and reused.
5. Identify package relationships that should be visible to users, such as:
   - `Configurations` and `Configuration.Defaults`
   - `Contracts` and implementation packages
   - `Logger` and concrete logger packages
   - `Collection.Streamers`, `Display.Attributes`, and `Object.Converters`
   - `Data.Sql`, `Data.MsSql`, `Data.FileReader`, and `Data.Bulk`

### Deliverable

A finalized package inventory and gap list that drives the rewrite.

## Phase 2: Information Architecture Redesign

### Goal

Restructure the docs so users can navigate by learning stage and by package category.

### Tasks

1. Redesign the homepage to explain what VersaTul is, who it is for, and how the packages fit together.
2. Introduce a clearer navigation model built around package groups.
3. Add a beginner-first path with links to installation, configuration, and first-use examples.
4. Add an advanced path for users looking for package capabilities, extensibility, and integration patterns.
5. Normalize page names so they match the package names or an intentional short form consistently.
6. Remove or consolidate duplicate pages such as the two FileReader pages.

### Deliverable

An approved documentation structure and navigation model.

## Phase 3: Shared Content Template For Package Pages

### Goal

Create a consistent structure so every package page answers the same user questions.

### Tasks

1. Define a standard package page template.
2. Use sections that support both beginners and advanced users.
3. Standardize terminology across all docs.
4. Define how feature lists, examples, notes, warnings, and version-specific changes will be presented.

### Proposed Standard Package Page Sections

The final docs use the concise page shape captured in `PACKAGE_DOC_TEMPLATE.md`.

1. Overview
2. When To Use This Package
3. Installation
4. Related Packages
5. Core Types And Concepts
6. Key Capabilities
7. Basic Example
8. Deeper Example When Needed
9. Notes

### Deliverable

A reusable package-page blueprint for all `.rst` rewrites.

## Phase 4: Beginner Journey

### Goal

Make the docs usable for a new adopter with minimal prior context.

### Tasks

1. Add a clear introduction to the library ecosystem.
2. Add a quick-start page or homepage quick-start section.
3. Explain package selection with practical guidance such as:
   - which packages are foundational
   - which packages are optional
   - which packages are commonly used together
4. Add first-use examples that are short and realistic.
5. Add upgrade-friendly installation guidance for NuGet consumers.

### Deliverable

A complete onboarding path from landing page to first successful package usage.

## Phase 5: Advanced And Expert Guidance

### Goal

Expose the full power of the libraries for experienced users.

### Tasks

1. Document extension points and interfaces that users can swap or implement.
2. Document package composition patterns across the ecosystem.
3. Document advanced configuration and dependency-injection usage where relevant.
4. Add feature matrices or capability summaries for similar packages where useful.
5. Add clearer references to related packages and integration scenarios.

### Deliverable

Advanced guidance that helps experienced users use the libraries intentionally and completely.

## Phase 6: Package-by-Package Rewrite Pass

### Goal

Refresh each package page against the current codebase and package behavior.

### Recommended Rewrite Order

1. Foundation packages
2. Data packages
3. File and streaming packages
4. Logging, mail, and scheduling packages

### Detailed Rewrite Checklist Per Package

1. Verify package purpose against the current `.csproj` description and public API.
2. Update examples to match current code and naming.
3. Expand the feature list to show the actual supported functionality.
4. Document important interfaces, concrete implementations, and common usage flows.
5. Add related-package references.
6. Remove stale changelog noise unless it adds real user value.
7. Make sure each page helps both a first-time user and an advanced integrator, adding a deeper example only when it teaches a meaningful scenario.

### Deliverable

Modernized package pages that reflect the current state of the NuGet libraries.

## Phase 7: Cross-Cutting Quality Improvements

### Goal

Improve the quality and maintainability of the documentation as a whole.

### Tasks

1. Update project metadata in Sphinx configuration where needed.
2. Improve consistency in headings, tone, and terminology.
3. Check for broken links, duplicate topics, and missing toctree entries.
4. Ensure examples are syntactically consistent and readable.
5. Decide whether to add diagrams for package relationships and data flow.
6. Review whether package changelog content should stay in docs or move elsewhere.

### Deliverable

Cleaner, more maintainable documentation with fewer structural defects.

## Phase 8: Validation And Publish Readiness

### Goal

Ensure the docs build cleanly and read well before publishing.

### Tasks

1. Build the Sphinx docs locally and resolve warnings.
2. Review navigation from the perspective of a first-time user.
3. Review package pages from the perspective of an advanced user looking for depth.
4. Validate naming consistency across repo, package names, and docs pages.
5. Perform a final pass for clarity, spelling, and formatting.

### Deliverable

An approved documentation set ready for incremental publishing.

## Remaining Work

The content modernization and validation work are effectively complete.

Any remaining work is optional follow-up:

1. Spot-check the generated HTML in `docs/build/html` for visual polish.
2. Decide whether to commit the local `.venv` workflow guidance into broader contributor onboarding beyond this repository.