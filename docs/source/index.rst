.. meta::
    :google-site-verification: qzvlosH2brzdVklyvowF3R1QXvefZW6xph30oJPaPNc


VersaTul Documentation
======================

**VersaTul** is a collection of focused .NET libraries for common application work such as configuration, data access, import and export flows, logging, mail delivery, and scheduled processing.

It is designed for teams that want reusable building blocks without committing to one large framework. You can start with a single NuGet package for one concrete problem and add adjacent packages only when you need them.

If you are evaluating the library for the first time, the fastest path is:

1. Pick the developer job you need to solve.
2. Start with one package or one small package combination.
3. Follow a short quickstart or scenario path.
4. Expand into the package reference only after the first workflow is working.

Start By Problem
----------------

Use these paths if you want the quickest route to a relevant package.

1. I need strongly typed application settings: start with :doc:`getting-started`.
2. I need relational data access: start with :doc:`scenario-guides/sql-data-access`.
3. I need to import CSV or text data: start with :doc:`scenario-guides/file-import`.
4. I need export or formatting helpers: start with :doc:`scenario-guides/data-export`.
5. I need logging in a service or background process: start with :doc:`scenario-guides/logging-setup`.
6. I need a package starting set for my application type: start with :doc:`recommended-paths`.

Start In 5 Minutes
------------------

If you want a fast first win, start with the onboarding path instead of browsing the full catalog.

1. Read :doc:`getting-started` for a copy-paste configuration quickstart.
2. Read :doc:`package-selection` for an intent-first guide to the package ecosystem.
3. Use :doc:`scenario-guides/index` for end-to-end workflows that combine multiple packages.
4. Use :doc:`package-catalog` after you know the workflow or package family you want.

Adoption FAQ
------------

Common evaluation answers:

1. Start with one package, not the whole ecosystem.
2. Prefer :doc:`sql` when provider flexibility matters and :doc:`mssql` when SQL Server-specific behavior is the real requirement.
3. Use :doc:`logger` with a sink package such as :doc:`logger-file`; the base logger package is not a sink by itself.
4. Use :doc:`recommended-paths` if you want a package starting set by app type.
5. Use :doc:`faq` if you want the broader adoption and selection guidance in one place.

What To Read Next
-----------------

1. Read :doc:`getting-started` if you want the smallest copy-paste success case first.
2. Read :doc:`recommended-paths` if you already know your application shape.
3. Read :doc:`scenario-guides/index` if your main question is how packages combine in a real workflow.
4. Read :doc:`package-selection` if you still need help narrowing the first package family.

Popular Workflows
-----------------

These are the highest-value package combinations for first-time adopters.

1. Configuration bootstrap: start with :doc:`getting-started` and then add ``VersaTul.Configuration.Defaults``.
2. SQL-backed service: follow :doc:`scenario-guides/sql-data-access`.
3. File import pipeline: follow :doc:`scenario-guides/file-import`.
4. Export pipeline: follow :doc:`scenario-guides/data-export`.
5. Logging setup: follow :doc:`scenario-guides/logging-setup`.

How VersaTul Is Organized
-------------------------

The ecosystem is organized as focused NuGet packages that can be used independently or combined to build larger solutions. Across the library set you will find support for:

1. **Foundational application building blocks** such as contracts, configuration, utilities, and object conversion.
2. **Data access and data movement** including SQL, SQL Server, MongoDB, EF Core, bulk copy, file readers, and caching.
3. **File, transformation, and processing workflows** including compression, streamers, file handling, display metadata, and pipelines.
4. **Operational concerns** such as logging, mail delivery, and task scheduling.

.. note::

   These docs focus on the NuGet-distributed VersaTul library packages.

Start Here
----------

.. toctree::
   :maxdepth: 1

   getting-started
   package-selection
   scenario-guides/index
   recommended-paths
   compatibility
   faq
   package-catalog


Package Reference
-----------------

Foundation Packages
^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   configuration
   configuration-defaults
   contracts
   data-contracts
   converters
   extensions
   utilities

Data And Storage Packages
^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   caching
   bulk
   sql
   mssql
   mongodb
   efcore
   file-reader

File, Processing, And Integration Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   compression
   streamers
   display-attributes
   handler-file
   pipeline-infrastructure

Operational Packages
^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   logger
   logger-file
   logger-mail
   logger-web
   mailer
   scheduler
