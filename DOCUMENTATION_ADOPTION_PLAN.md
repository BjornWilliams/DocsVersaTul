# VersaTul Documentation Adoption Plan

## Objective

Increase developer adoption by making the documentation answer four questions faster:

1. What problem does VersaTul solve for me?
2. Which package should I install first?
3. What does working code look like in a realistic scenario?
4. How do the packages fit together as I expand usage?

## Current Assessment

The documentation is structurally healthier than a typical package-doc site. The package coverage is broad, the navigation is no longer broken, and most package pages already include installation guidance and code samples.

The main adoption issue is not missing reference material. The issue is that the experience still feels reference-first instead of outcome-first.

## What Is Working

1. The site has clear package-group organization.
2. The main onboarding pages exist and are easy to find.
3. Most package pages include code snippets and related-package references.
4. The docs appear to be aligned to the NuGet package surface instead of unrelated host projects.

## Friction Points That Likely Hurt Adoption

### 1. The homepage explains categories, but not developer outcomes

The landing page explains the library groups well, but it does not quickly prove value through a few concrete developer jobs such as:

1. Read config safely in a service.
2. Import a CSV into a database.
3. Add logging with a concrete sink.
4. Export records to CSV or JSON.

For a new adopter, package categories are weaker than use-case entry points.

### 2. The getting-started path does not deliver a fast first win

The current getting-started page tells readers how to choose a package and install one, but it stops short of giving them a short copy-paste path to a successful result in a small sample app.

That leaves the user to do the integration work mentally.

### 3. Package selection is organized by package family, not by job to be done

The current selection page is helpful, but it still expects the developer to understand the VersaTul package model before they understand their own best entry point.

For adoption, the first-level navigation should start with practical intents such as:

1. I need data access.
2. I need import or export tooling.
3. I need logging.
4. I need scheduling.
5. I need configuration and utility building blocks.

### 4. The docs show APIs, but not enough end-to-end package combinations

Several pages have useful API examples, but there are not enough scenario guides showing how multiple packages combine to solve a real task.

This is especially important for the parts of VersaTul that become more compelling together than alone.

### 5. The site needs stronger “why this package” messaging

Many package pages explain what the package contains, but not always the practical tradeoff:

1. Why choose this package over writing a small internal helper?
2. When should this package be preferred over an alternative VersaTul package?
3. What complexity does it remove?
4. What kind of application benefits most?

### 6. There is no obvious adoption ladder

The docs do not yet guide developers through a staged journey such as:

1. Start with one package.
2. Add one adjacent package.
3. Combine them in a realistic workflow.
4. Expand into advanced usage only after the basics work.

That ladder matters because VersaTul is an ecosystem, not a single binary decision.

## Recommended Content Strategy

The next iteration should optimize for time-to-value, package discovery, and confidence.

### Pillar 1: Lead With Use Cases

Shift the top-level experience from package catalog first to scenario first.

Add clear paths for:

1. Configuration and app setup.
2. SQL or MongoDB data access.
3. File import pipelines.
4. Export and formatting workflows.
5. Logging and operational support.
6. Background or scheduled processing.

### Pillar 2: Give Every New User A Fast Success Path

Create at least one short quickstart that can be completed in a few minutes and demonstrates visible value.

Good quickstart candidates:

1. Load strongly typed configuration.
2. Read a CSV file and process rows.
3. Log an exception through a concrete logger.
4. Export a collection to CSV.

### Pillar 3: Show Package Combinations, Not Only Package Pages

Add scenario guides that explain how packages work together in realistic workflows.

High-value combinations:

1. `Configurations` + `Configuration.Defaults`
2. `Data.FileReader` + `Data.Bulk`
3. `Collection.Streamers` + `Display.Attributes` + `Object.Converters`
4. `Logger` + `Logger.File` or `Logger.Mail`
5. `Data.Sql` + `Data.Contracts`

### Pillar 4: Improve Conversion-Oriented Navigation

Add stronger calls to action that move a reader forward:

1. Start with a quickstart.
2. Choose a package by use case.
3. Compare related packages.
4. Follow a complete scenario.
5. Go deeper into the API reference.

### Pillar 5: Reduce Decision Anxiety

Use comparison tables, “start here if” guidance, and opinionated recommendations so developers do not need to reverse-engineer the ecosystem.

## Proposed Deliverables

### Workstream 1: Reframe The Homepage

Goal: make the landing page sell the value of the ecosystem in less than a minute.

Tasks:

1. Rewrite the hero section around outcomes instead of package categories.
2. Add a “Start by problem” section with 4 to 6 primary developer intents.
3. Add a “Popular workflows” section that links into scenario guides.
4. Add a “Start in 5 minutes” quickstart callout.
5. Add a concise “How VersaTul is organized” section after the value-first content, not before it.

Acceptance criteria:

1. A new visitor can identify a relevant entry point in under 30 seconds.
2. The page answers what VersaTul is, who it is for, and what to try first.

### Workstream 2: Build A Real Quickstart Track

Goal: give new adopters one copy-paste path to a visible success.

Tasks:

1. Expand the current getting-started page into a true quickstart track.
2. Add a minimal sample project flow with prerequisites, install command, code snippet, expected result, and next step.
3. Add one quickstart per high-value package family over time.
4. Add “what you should see” checkpoints so developers can verify progress quickly.
5. Add “common mistakes” notes for configuration names, package combinations, and required setup.

Acceptance criteria:

1. A developer can complete one quickstart without reading multiple package pages first.
2. Each quickstart has a clear success outcome and next recommended step.

### Workstream 3: Replace Package-First Selection With Intent-First Selection

Goal: help developers choose packages using their problem statement.

Tasks:

1. Redesign the package-selection page around developer jobs to be done.
2. Add decision tables such as SQL versus MsSql, Logger core versus concrete logger sinks, and Streamers versus FileReader versus Bulk for different workflows.
3. Add “best first package” recommendations for common application types.
4. Add “avoid this combination when” guidance where packages overlap or are commonly misunderstood.

Acceptance criteria:

1. The page helps a reader choose an initial package set without already knowing VersaTul naming.
2. The page reduces ambiguity across similar packages.

### Workstream 4: Add Scenario Guides

Goal: prove how the ecosystem helps with real application work.

Tasks:

1. Create a scenario-guides section in the docs navigation.
2. Write an import workflow guide using `Data.FileReader` and `Data.Bulk`.
3. Write an export workflow guide using `Collection.Streamers`, `Display.Attributes`, and `Object.Converters`.
4. Write a logging setup guide using `Logger` and one concrete sink.
5. Write a relational data access guide using `Data.Sql` or `Data.MsSql` with shared configuration.
6. Link every involved package page back to the relevant scenario guide.

Acceptance criteria:

1. At least three end-to-end workflows exist and are reachable from the homepage.
2. Scenario guides include package install steps, code, expected behavior, and related next steps.

### Workstream 5: Strengthen Package Pages For Adoption

Goal: make each package page answer “why should I use this?” more clearly.

Tasks:

1. Add or tighten a “why use this package” section on each page.
2. Add “start here if” and “not the right package if” guidance where helpful.
3. Add “works well with” callouts for companion packages.
4. Ensure every page has one minimal example and one realistic example when the package is ecosystem-oriented.
5. Add expected inputs and outputs for examples where the result is not obvious.

Acceptance criteria:

1. Each package page explains value, fit, and adjacent packages clearly.
2. A first-time reader can decide whether to adopt the package without scanning source code.

### Workstream 6: Improve Trust Signals And Adoption UX

Goal: help developers feel safe adopting the packages.

Tasks:

1. Add a version and compatibility page covering supported .NET targets and package maturity signals.
2. Add a “recommended first packages” page for common solution types.
3. Add a concise FAQ for common adoption questions.
4. Add a “migration from custom helpers” page that explains when VersaTul replaces ad hoc internal utility code well.
5. Add badges or summary metadata where they add credibility without clutter.

Acceptance criteria:

1. The docs answer common evaluation concerns without requiring repository exploration.
2. New adopters can assess fit, stability, and starting scope quickly.

## Implementation Sequence

Use this order to maximize impact early:

1. Reframe homepage.
2. Build one true quickstart.
3. Redesign package-selection around intents.
4. Publish first three scenario guides.
5. Upgrade the highest-traffic package pages.
6. Add FAQ, compatibility, and trust pages.

## Task Backlog

### Phase 1: Entry Experience

Status: Completed on 2026-05-31.

1. Rewrite `docs/source/index.rst` with a stronger value proposition and scenario entry points.
2. Expand `docs/source/getting-started.rst` into a copy-paste quickstart.
3. Rewrite `docs/source/package-selection.rst` around developer intents and comparison tables.
4. Update `docs/source/package-catalog.rst` so it supports discovery after orientation, not before it.

### Phase 2: Scenario Content

Status: Completed on 2026-05-31.

1. Add `docs/source/scenario-guides/index.rst`.
2. Add `docs/source/scenario-guides/file-import.rst`.
3. Add `docs/source/scenario-guides/data-export.rst`.
4. Add `docs/source/scenario-guides/logging-setup.rst`.
5. Add `docs/source/scenario-guides/sql-data-access.rst`.
6. Add the new scenario-guides to the homepage and toctrees.

### Phase 3: Package-Page Reinforcement

Status: Completed on 2026-05-31.

1. Prioritize package pages most likely to influence adoption: configuration, sql, mssql, file-reader, streamers, logger, logger-file, and mailer.
2. Add stronger “why use this” framing to the prioritized pages.
3. Add “works well with” and “next step” sections to the prioritized pages.
4. Normalize examples so they show setup, action, and expected result.

### Phase 4: Evaluation And Trust

Status: Completed on 2026-05-31.

1. Add `docs/source/faq.rst`.
2. Add `docs/source/compatibility.rst`.
3. Add `docs/source/recommended-paths.rst`.
4. Add a simple adoption-oriented FAQ section to the homepage.

### Phase 5: Validation

Status: Completed on 2026-05-31.

1. Run strict Sphinx validation after each workstream.
2. Review navigation from the perspective of a first-time .NET package evaluator.
3. Check that every onboarding page ends with an obvious next action.
4. Check that every scenario guide links to the involved package pages and back again.

## Success Metrics

Use a mix of qualitative and quantitative signals.

1. Reduced bounce-off from the landing page.
2. Increased visits from homepage to package pages through scenario links.
3. Increased visits to getting-started and scenario-guide pages.
4. Faster time for a new developer to identify a first package.
5. More issue or discussion activity that references docs-guided onboarding rather than source-code exploration.

## Recommendation

If the goal is to improve adoption quickly, the first delivery slice should be small and conversion-oriented:

1. Rewrite the homepage.
2. Turn getting-started into a real quickstart.
3. Redesign package-selection around developer intents.
4. Add one scenario guide for file import and one for logging.

That batch should provide the largest adoption gain before a full second rewrite of every package page.