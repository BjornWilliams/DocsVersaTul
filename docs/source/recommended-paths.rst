Recommended Paths
=================

This page gives opinionated starting points for common application types so new adopters do not have to assemble a package set from scratch.

Use these as small starting sets, not as instructions to install everything at once.

Console App Or Utility Tool
---------------------------

Start with:

1. :doc:`configuration`
2. :doc:`extensions` or :doc:`utilities`
3. :doc:`logger-file` if operational visibility matters

Why this path works:

It gives a small application explicit settings, reusable helpers, and simple local logging without adding unnecessary infrastructure.

Service With Relational Data Access
-----------------------------------

Start with:

1. :doc:`configuration`
2. :doc:`sql`
3. :doc:`data-contracts`
4. :doc:`logger` and a sink such as :doc:`logger-file`

Then add:

1. :doc:`mssql` only if SQL Server-specific behavior becomes necessary.

Best next read:

1. :doc:`scenario-guides/sql-data-access`

SQL Server Import Pipeline
--------------------------

Start with:

1. :doc:`file-reader`
2. :doc:`bulk`
3. :doc:`mssql`
4. :doc:`logger-file`

Why this path works:

It separates file parsing, schema mapping, upload execution, and diagnostics into clear package boundaries.

Best next read:

1. :doc:`scenario-guides/file-import`

Reporting Or Export Workflow
----------------------------

Start with:

1. :doc:`streamers`
2. :doc:`display-attributes`
3. :doc:`converters`
4. :doc:`compression` when archive output matters
5. :doc:`mailer` when exported files need delivery

Why this path works:

It keeps export structure, formatting, and delivery concerns modular.

Best next read:

1. :doc:`scenario-guides/data-export`

Operational Logging Baseline
----------------------------

Start with:

1. :doc:`logger`
2. :doc:`logger-file`

Then expand to:

1. :doc:`logger-mail` for alerting by email
2. :doc:`logger-web` for remote endpoint delivery

Best next read:

1. :doc:`scenario-guides/logging-setup`

Notification Or Mail Workflow
-----------------------------

Start with:

1. :doc:`configuration`
2. :doc:`mailer`
3. :doc:`streamers` when attachments are generated from exported data

Why this path works:

It keeps transport, settings, and attachment generation separate.

Background Processing Or Scheduling
-----------------------------------

Start with:

1. :doc:`scheduler`
2. :doc:`logger-file`
3. :doc:`configuration`

Why this path works:

Recurring jobs are much easier to adopt safely when scheduling, settings, and diagnostics are in place from the start.

Selection Rules
---------------

1. Start from the application problem, not the full package catalog.
2. Prefer one workflow path at a time.
3. Add sink or storage-specific packages only after the base workflow is working.
4. Use scenario guides when two or more packages are likely to be adopted together.

What To Read Next
-----------------

1. Read :doc:`package-selection` if your application type still maps to several possible starting sets.
2. Read :doc:`scenario-guides/index` if you want the end-to-end version of one of these paths.
3. Read :doc:`compatibility` if framework support and dependency shape are still part of the evaluation.