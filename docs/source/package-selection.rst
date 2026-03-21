Choosing Packages
=================

VersaTul works best when you approach it as a toolbox.

This page helps you choose the smallest set of packages that solves your current problem while keeping room for later expansion.

The most reliable strategy is to start from the concrete problem, not the full library catalog.

Start With The Problem
----------------------

Use the problem you are trying to solve as the main selection criteria.

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

+-----------------------------------+-----------------------------------------------------------------------+
| Scenario                          | Recommended starting packages                                         |
+===================================+=======================================================================+
| Basic service application         | ``VersaTul.Configurations``, ``VersaTul.Extensions``, ``VersaTul.Logger`` |
+-----------------------------------+-----------------------------------------------------------------------+
| SQL-backed application            | ``VersaTul.Data.Sql`` or ``VersaTul.Data.MsSql``, ``VersaTul.Data.Contracts`` |
+-----------------------------------+-----------------------------------------------------------------------+
| File import pipeline              | ``VersaTul.Data.FileReader``, ``VersaTul.Data.Bulk``, ``VersaTul.Handler.File`` |
+-----------------------------------+-----------------------------------------------------------------------+
| Export and formatting workflow    | ``VersaTul.Collection.Streamers``, ``VersaTul.Display.Attributes``, ``VersaTul.Object.Converters`` |
+-----------------------------------+-----------------------------------------------------------------------+
| Background processing             | ``VersaTul.Task.Scheduler``, ``VersaTul.Logger``, one concrete logger |
+-----------------------------------+-----------------------------------------------------------------------+
| Notification workflow             | ``VersaTul.Mailer``, ``VersaTul.Logger.Mail``                         |
+-----------------------------------+-----------------------------------------------------------------------+

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

1. Read :doc:`package-catalog` for the full package landscape.
2. Jump directly to the package page you plan to adopt first.