Support And Feedback
====================

Use the route that matches your request. Public GitHub issues are visible to
everyone. Remove credentials, personal information, and private application
data before posting. These forms are maintained in the public
`DocsVersaTul issue tracker <https://github.com/BjornWilliams/DocsVersaTul/issues/new/choose>`_.

.. list-table:: VersaTul support and disclosure routes
   :header-rows: 1

   * - Request
     - Route
     - Visibility
     - What to include
   * - Bug report
     - `Open a public bug report <https://github.com/BjornWilliams/DocsVersaTul/issues/new?template=bug_report.yml>`_
     - Public
     - Affected package and version, target framework, expected and actual result, reproduction steps, and the smallest useful code sample. Redact secrets and customer data.
   * - Usage question
     - `Ask a public usage question <https://github.com/BjornWilliams/DocsVersaTul/issues/new?template=usage_question.yml>`_
     - Public
     - Package and version, target framework, the result you want, what you tried, and a small code or configuration example with secrets removed.
   * - Feature proposal
     - `Propose a feature <https://github.com/BjornWilliams/DocsVersaTul/issues/new?template=feature_request.yml>`_
     - Public
     - Related package, the user problem, desired outcome, and known compatibility or migration constraints. A proposed API is optional.
   * - Documentation help
     - `Request documentation help <https://github.com/BjornWilliams/DocsVersaTul/issues/new/choose>`_ and choose **Documentation help**
     - Public
     - Page URL, the task you were trying to complete, what is unclear or incorrect, and an optional suggested correction.
   * - Security disclosure
     - See :doc:`security` for private disclosure guidance.
     - Private channel only
     - Do not open a public issue or pull request. Use GitHub's private report form if it is available; otherwise request a private channel through NuGet Contact owners without including vulnerability details.

For a bug report, separate the observed result from the expected result and
include steps that another contributor can follow. Keep reproductions small and
remove secrets, customer records, and unrelated application code. For a
feature proposal, explain the user problem first; a design or API proposal is
optional. For a documentation request, link to the page and describe the task
that the page did not help you complete.

Security concerns do not belong in public issues, discussions, pull requests,
or commits. If GitHub's Security tab does not offer private vulnerability
reporting, use **Contact owners** on the affected NuGet package page only to
request a private channel. Share details after the maintainer confirms the
reply channel is private. The repository's public ``SECURITY.md`` contains the
same instructions.

The repository's public ``CODE_OF_CONDUCT.md`` covers project interactions and
explains how to request a private channel for conduct concerns.
For repository layout and the per-package test workflow, see
:doc:`contributing`.

Support, release, and response expectations
--------------------------------------------

The repository owner and maintainers review public requests as time allows.
This issue tracker is a feedback channel, not a support contract. There is no
response-time or service-level commitment, guaranteed fix, emergency incident
response, paid support arrangement, or promise that a feature proposal will be
accepted. Do not use public issues for production incidents or urgent security
reports.

VersaTul NuGet packages are versioned and released independently. They do not
share a release date or fixed release cadence. Use the exact package version's
NuGet page for its framework assets and release notes. Current source build and
test coverage does not change the assets or support status of a version that
was already published. The :doc:`compatibility` page describes framework
status; :doc:`release-notes` describes package and documentation versions.

The ``2026.10`` documentation snapshot retains historical API information for
``VersaTul.Data.Sql`` 1.0.15 and ``VersaTul.Data.MsSql`` 1.0.13. Keeping those
pages available preserves existing links. It does not promise maintenance,
fixes, or future releases for those 1.x package lines. Other older package
majors are not declared supported by that initial snapshot.
