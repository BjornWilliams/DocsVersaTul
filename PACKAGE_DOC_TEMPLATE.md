# VersaTul Package Documentation Template

Use this template when modernizing or adding package documentation pages.

## Recommended Section Order

1. Overview
2. When To Use This Package
3. Installation
4. Related Packages
5. Core Types And Concepts
6. Key Capabilities
7. Basic Example
8. Deeper Example When Needed
9. Notes

## Preferred Page Shape

The current docs set uses a concise package-reference shape rather than long historical or changelog-heavy pages.

Use deeper sections only when the package genuinely benefits from them, for example:

1. Configuration Notes
2. Dependency Injection
3. Mapping Options
4. Async Example
5. Operational Notes

Avoid adding sections just to satisfy a template.

## Authoring Rules

1. Start with the user problem, not the implementation detail.
2. Keep one short beginner example near the top.
3. Add a deeper example only when it teaches composition, extensibility, or a non-obvious workflow.
4. Document interfaces and concrete implementations separately when both matter.
5. Use package names exactly as published in NuGet.
6. Prefer current .NET CLI install commands and keep the Package Manager Console variant as a secondary option.
7. Avoid long historical changelog sections unless a change materially affects users.
8. Use the VersaTul codebase as the source of truth over older docs text.
9. Focus on library packages only, not host or test projects.

## Package Rewrite Checklist

1. Verify the page against the current `.csproj` description.
2. Verify example types and method names against the current codebase.
3. Add related package links.
4. Remove outdated or duplicate examples.
5. Make sure the page helps both a first-time user and an advanced integrator.
6. Run editor diagnostics after rewriting the page.
7. Search for stale legacy fragments if the page was rebuilt from older content.