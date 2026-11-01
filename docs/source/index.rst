.. meta::
    :google-site-verification: qzvlosH2brzdVklyvowF3R1QXvefZW6xph30oJPaPNc


VersaTul Documentation
======================

**VersaTul** is a collection of focused .NET libraries for common application work such as configuration, data access, import and export flows, logging, mail delivery, and scheduled processing.

It is designed for teams that want reusable building blocks without committing to one large framework. For a first evaluation, choose one problem below and follow its guide; add adjacent packages only when the workflow needs them.

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

Choose a problem above and follow its linked guide to a first working result. Use :doc:`package-catalog` when you are ready to compare related packages.

Package Selection Notes
-----------------------

Keep the first workflow small:

1. Prefer :doc:`sql` when provider flexibility matters and :doc:`mssql` when SQL Server-specific behavior is required.
2. Pair :doc:`logger` with a sink package such as :doc:`logger-file`; the base logger package is not a sink by itself.

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
   dotnet-10-upgrade
   support
   security
   repository-access
   release-notes
   api-reference
   api-contract-policy
   snippet-inventory
   faq
   package-catalog
   package-inventory


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
