.. meta::
    :google-site-verification: qzvlosH2brzdVklyvowF3R1QXvefZW6xph30oJPaPNc


VersaTul Documentation
======================

**VersaTul** is a collection of reusable .NET libraries designed to solve common application concerns without forcing you into a single monolithic framework.

The ecosystem is organized as focused NuGet packages that can be used independently or combined to build larger solutions. Across the library set you will find support for:

1. **Foundational application building blocks** such as contracts, configuration, utilities, and object conversion.
2. **Data access and data movement** including SQL, SQL Server, MongoDB, EF Core, bulk copy, file readers, and caching.
3. **File, transformation, and processing workflows** including compression, streamers, file handling, display metadata, and pipelines.
4. **Operational concerns** such as logging, mail delivery, and task scheduling.

This documentation is being reorganized to support both first-time adopters and experienced users who need deeper package detail.

How To Use These Docs
---------------------

If you are new to VersaTul, start with the onboarding pages and use the package catalog to find the right entry point.

If you already know the package you need, jump directly to the package reference sections below.

Recommended starting points:

1. Read :doc:`getting-started` for the quickest path from zero context to first package usage.
2. Read :doc:`package-selection` if you are deciding which packages to adopt.
3. Use :doc:`package-catalog` to browse the full library surface area by category.

.. note::

   This project is under active development.
   
   For support, contact us via email. versatul.libraries@outlook.com


Start Here
----------

.. toctree::
   :maxdepth: 1

   getting-started
   package-selection
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

.. toctree::
   :hidden:

   Home <self>
   getting-started
   package-selection
   package-catalog
   caching
   compression
   configuration
   configuration-defaults
   contracts
   converters
   streamers
   data-contracts
   bulk
   sql
   mssql
   mongodb
   display-attributes
   efcore
   extensions
   handler-file
   logger
   logger-file
   logger-mail
   logger-web
   mailer
   pipeline-infrastructure
   scheduler
   file-reader
   utilities
