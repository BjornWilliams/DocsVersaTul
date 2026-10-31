# DocsVersaTul Agent Instructions

## Repository Overview

This documentation repository is hosted on GitHub and its approved work is tracked in Azure Boards. The authoritative imported User Story and Task IDs are annotated in the sibling VersaTul repository under `../VersaTul/Work.Tasks`.

For cross-repository audit work, also review `../VersaTul/Work.Tasks/IMPLEMENTATION_AGENT_NOTES.md` for the current branch handoff and shared workflow conventions.

Before implementing approved documentation work, locate the exact Azure User Story and Task IDs in:

- `../VersaTul/Work.Tasks/DOCUMENTATION_ADOPTION_TASKS_2026-08.md`
- or the applicable correctness, package, or feature backlog when documentation is a child action of that work.

## Mandatory Azure Boards Commit Linking

Because DocsVersaTul is hosted on GitHub, use the Azure Boards GitHub syntax:

- Link only while work remains: `AB#<task-id>` and `AB#<user-story-id>`.
- Resolve a completed Task while keeping its parent open: `Fixes AB#<task-id>` and link-only `AB#<user-story-id>`.
- Resolve the final Task and completed User Story: repeat the keyword, for example `Fixes AB#<task-id>` and `Fixes AB#<user-story-id>`.
- Repeat `Fixes` for every completed work item. Do not use one keyword followed by a comma-separated list.
- Never resolve a User Story until all child Tasks and acceptance criteria are complete.
- If one Task spans DocsVersaTul and VersaTul, use link-only mentions until the complete cross-repository result is ready; do not close it after only one repository's portion is finished.

Example Task-completion commit:

```text
Correct package quickstart examples

Fixes AB#<task-id>
AB#<user-story-id>
```

The GitHub repository must be connected to the Azure Boards project, and the commit or pull request must reach the default branch before transition rules apply. Verify the Azure state after merge.

These rules apply when a commit is requested or otherwise authorized; they do not independently authorize an agent to commit, push, open a pull request, or merge.

Official reference: https://learn.microsoft.com/en-us/azure/devops/boards/github/link-to-from-github?view=azure-devops
