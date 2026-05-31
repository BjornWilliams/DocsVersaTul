Choosing Packages
=================

VersaTul works best when you start from the job you need to get done, not from the full package list.

This page helps you choose the smallest package set that solves your current problem while avoiding unnecessary overlap.

If you are new to the ecosystem, use the decision sections below before browsing the full catalog.

Start With The Problem
----------------------

Use the problem you are trying to solve as the main selection criteria.

Fast Recommendations
^^^^^^^^^^^^^^^^^^^^

1. If you need application settings and lightweight configuration models, start with :doc:`configuration`.
2. If you need relational data access, start with :doc:`sql` or :doc:`mssql`.
3. If you need CSV or text-file imports, start with :doc:`file-reader`.
4. If you need export output, start with :doc:`streamers`.
5. If you need logging, start with :doc:`logger` and then add a sink package.
6. If you need scheduled work, start with :doc:`scheduler`.

Application Foundation
^^^^^^^^^^^^^^^^^^^^^^

Choose these when you need shared abstractions, settings, conversion helpers, or reusable utility methods.

1. :doc:`contracts`
2. :doc:`configuration`
3. :doc:`configuration-defaults`
4. :doc:`converters`
5. :doc:`extensions`
6. :doc:`utilities`

Data Access And Data Movement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Choose these when your application reads, writes, transforms, or transfers data.

1. :doc:`caching`
2. :doc:`data-contracts`
3. :doc:`bulk`
4. :doc:`sql`
5. :doc:`mssql`
6. :doc:`mongodb`
7. :doc:`efcore`
8. :doc:`file-reader`

Output, Transformation, And Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Choose these when you need export pipelines, file operations, compression, or object transformation workflows.

1. :doc:`compression`
2. :doc:`streamers`
3. :doc:`display-attributes`
4. :doc:`handler-file`
5. :doc:`pipeline-infrastructure`

Logging, Mail, And Scheduling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Choose these when you need operational tooling around application runtime behavior.

1. :doc:`logger`
2. :doc:`logger-file`
3. :doc:`logger-mail`
4. :doc:`logger-web`
5. :doc:`mailer`
6. :doc:`scheduler`

Common Package Combinations
---------------------------

These combinations are useful starting points for common scenarios.

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Scenario
     - Recommended starting packages
   * - Basic service application
     - ``VersaTul.Configurations``, ``VersaTul.Extensions``, ``VersaTul.Logger``
   * - SQL-backed application
     - ``VersaTul.Data.Sql`` or ``VersaTul.Data.MsSql``, ``VersaTul.Data.Contracts``
   * - File import pipeline
     - ``VersaTul.Data.FileReader``, ``VersaTul.Data.Bulk``, ``VersaTul.Handler.File``
   * - Export and formatting workflow
     - ``VersaTul.Collection.Streamers``, ``VersaTul.Display.Attributes``, ``VersaTul.Object.Converters``
   * - Background processing
     - ``VersaTul.Task.Scheduler``, ``VersaTul.Logger``, one concrete logger
   * - Notification workflow
     - ``VersaTul.Mailer``, ``VersaTul.Logger.Mail``

Decision Tables
---------------

Use these comparisons when multiple packages appear relevant.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Decision
     - Start here when
     - Avoid starting here when
   * - ``Data.Sql`` vs ``Data.MsSql``
     - Use ``Data.Sql`` when you want provider-agnostic relational access or may support more than one ADO.NET provider. Use ``Data.MsSql`` when you know SQL Server is the target and want SQL Server-specific support.
     - Avoid ``Data.MsSql`` as the first choice if database portability matters. Avoid ``Data.Sql`` if you already know you need SQL Server-specific behavior immediately.
   * - ``Logger`` vs logger sink packages
     - Use ``Logger`` as the shared core contract and parsing layer. Add ``Logger.File``, ``Logger.Mail``, or ``Logger.Web`` when you need an actual delivery target.
     - Avoid treating ``Logger`` alone as a full sink solution.
   * - ``FileReader`` vs ``Streamers`` vs ``Bulk``
     - Use ``FileReader`` to read delimited or text input. Use ``Streamers`` to write export formats. Use ``Bulk`` when the problem is high-volume data transfer into relational storage.
     - Avoid starting with ``Bulk`` if you only need to parse an input file. Avoid starting with ``Streamers`` if your workflow is import-only.

Start Here If
-------------

1. You are building a service and need sane configuration plus logging: start with :doc:`configuration`, :doc:`extensions`, and :doc:`logger`.
2. You are building a CRUD or reporting app on relational storage: start with :doc:`sql` or :doc:`mssql`, then add :doc:`data-contracts`.
3. You are importing flat files into a database: start with :doc:`file-reader`, then add :doc:`bulk` and optionally :doc:`handler-file`.
4. You are generating files or tabular exports: start with :doc:`streamers`, then add :doc:`display-attributes` and :doc:`converters`.
5. You are adding recurring background work: start with :doc:`scheduler` and :doc:`logger`.

Not The Best First Move If
--------------------------

1. You are pulling in multiple overlapping data packages before your storage direction is clear.
2. You are treating every VersaTul package as mandatory foundation.
3. You are trying to evaluate the ecosystem by reading package pages in isolation instead of starting from one workflow.

Selection Rules That Usually Help
---------------------------------

1. Start with the narrowest package that solves the current problem.
2. Add abstract or foundational packages only when they support the concrete package you are using.
3. Prefer one data-access strategy per service unless you have a clear integration need.
4. Treat logging as a base package plus a delivery implementation.
5. Treat streamers, converters, and display attributes as complementary packages rather than isolated ones.

Selection Rules That Usually Hurt
---------------------------------

1. Pulling in multiple data-access packages before the primary storage choice is clear.
2. Treating every library package as a required foundation.
3. Mixing package examples from unrelated workflows before one end-to-end path is working.

For Advanced Users
------------------

If you already know the architecture you want:

1. Use the interfaces and contracts pages to identify extension points.
2. Review the package reference pages for concrete types and typical wiring patterns.
3. Combine packages deliberately based on shared concepts, not only naming similarity.

What To Read Next
-----------------

1. Jump directly to the package page you plan to adopt first.
2. Read :doc:`package-catalog` when you want the broader map of adjacent packages.
3. Go back to :doc:`getting-started` if you want the smallest copy-paste entry point.
4. Use :doc:`scenario-guides/index` when you want an end-to-end workflow that combines several packages.