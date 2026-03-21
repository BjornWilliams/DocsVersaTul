# VersaTul Package Documentation Template

Use this template when modernizing or adding package documentation pages.

## Recommended Section Order

1. Overview
2. When To Use This Package
3. Key Features
4. Installation
5. Dependencies And Related Packages
6. Core Types And Concepts
7. Basic Example
8. Advanced Example
9. Configuration
10. Common Patterns
11. Limitations And Gotchas
12. API Surface Summary
13. Related Packages
14. Version Notes

## Authoring Rules

1. Start with the user problem, not the implementation detail.
2. Keep one short beginner example near the top.
3. Include one deeper example that shows real composition or extensibility.
4. Document interfaces and concrete implementations separately.
5. Use package names exactly as published in NuGet.
6. Prefer current .NET CLI install commands and keep the Package Manager Console variant as a secondary option.
7. Avoid long historical changelog sections unless a change materially affects users.

## Package Rewrite Checklist

1. Verify the page against the current `.csproj` description.
2. Verify example types and method names against the current codebase.
3. Add related package links.
4. Remove outdated or duplicate examples.
5. Make sure the page helps both a first-time user and an advanced integrator.