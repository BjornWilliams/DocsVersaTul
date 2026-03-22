Package Catalog
===============

This page is the high-level map of the VersaTul library ecosystem.

Use it when you want to understand how the packages are grouped, what each package is for, and which packages are commonly used together.

It is a navigation page first, not a replacement for the package reference pages.

Foundation Packages
-------------------

These packages provide shared abstractions, configuration support, helpers, and reusable building blocks.

1. :doc:`contracts` for shared interfaces used throughout the ecosystem.
2. :doc:`configuration` for application setting access and configuration lookup.
3. :doc:`configuration-defaults` for standard default settings used by VersaTul packages.
4. :doc:`converters` for object-to-dictionary and related conversion workflows.
5. :doc:`extensions` for common extension methods.
6. :doc:`utilities` for general-purpose helper functionality.

Data And Storage Packages
-------------------------

These packages focus on querying, repository patterns, copying data, reading files, and caching.

1. :doc:`caching` for in-memory caching abstractions and implementations.
2. :doc:`data-contracts` for database-oriented contracts and shared data abstractions.
3. :doc:`bulk` for bulk data movement scenarios.
4. :doc:`sql` for provider-based relational data access built on common ADO.NET abstractions.
5. :doc:`mssql` for Microsoft SQL Server-specific data access and bulk-copy support.
6. :doc:`mongodb` for repository-style MongoDB access.
7. :doc:`efcore` for reusable EF Core repository patterns.
8. :doc:`file-reader` for reading CSV and text files as ``IDataReader`` sources.

File, Processing, And Transformation Packages
---------------------------------------------

These packages help when your workflow involves export, formatting, compression, file access, or multi-step processing.

1. :doc:`compression` for stream compression and decompression.
2. :doc:`streamers` for exporting collections to output formats such as CSV, tab-delimited text, or JSON.
3. :doc:`display-attributes` for metadata-driven output formatting.
4. :doc:`handler-file` for file-system operations and disk-based workflows.
5. :doc:`pipeline-infrastructure` for composing filter and transformation pipelines.

Operational Packages
--------------------

These packages support logging, message delivery, and scheduled execution.

1. :doc:`logger` for shared logging contracts and core behavior.
2. :doc:`logger-file` for file-based logging.
3. :doc:`logger-mail` for email-based logging.
4. :doc:`logger-web` for endpoint or web-based logging.
5. :doc:`mailer` for SMTP-based email sending.
6. :doc:`scheduler` for recurring and event-driven scheduling workflows.

Relationship Highlights
-----------------------

Some packages are most valuable when understood together.

1. :doc:`logger`, :doc:`logger-file`, :doc:`logger-mail`, and :doc:`logger-web` form a shared logging stack.
2. :doc:`configuration` and :doc:`configuration-defaults` usually appear together in application setup.
3. :doc:`streamers`, :doc:`display-attributes`, and :doc:`converters` complement each other in export scenarios.
4. :doc:`file-reader` and :doc:`bulk` fit naturally in import and migration workflows.
5. :doc:`contracts` and :doc:`data-contracts` define extension points reused by multiple concrete packages.

Recommended Browsing Paths
--------------------------

1. New users should start at :doc:`getting-started`.
2. Users evaluating adoption should read :doc:`package-selection`.
3. Experienced users can use this page as a jump table into the full package reference.