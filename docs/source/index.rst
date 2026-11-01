.. meta::
    :google-site-verification: qzvlosH2brzdVklyvowF3R1QXvefZW6xph30oJPaPNc


VersaTul Documentation
======================

**VersaTul** is a collection of focused .NET libraries for common application work such as configuration, data access, import and export flows, logging, mail delivery, and scheduled processing.

It is designed for teams that want reusable building blocks without committing to one large framework. For a first evaluation, choose one problem below and follow its guide; add adjacent packages only when the workflow needs them.

.. list-table:: Package proof at a glance
   :widths: 23 12 22 23 20

   * - **Targets**
       Current source directly builds and tests ``net8.0``, ``net9.0``, and ``net10.0``; .NET 10 is recommended for production. :doc:`compatibility` explains the assets in each published version.
     - **License**
       `MIT <https://licenses.nuget.org/MIT>`_
     - **Latest quickstart package**
       `VersaTul.Configurations 1.0.18 <https://www.nuget.org/packages/VersaTul.Configurations/1.0.18>`_
     - **Sample and build checks**
       The `pull-request workflow <https://github.com/BjornWilliams/DocsVersaTul/actions/workflows/documentation-samples.yml>`_ builds the docs and runs output-checked samples on all three target frameworks.
     - **Source and support**
       :doc:`repository-access` (sign-in may be required); :doc:`support` (public issue forms).

**Primary next step:** :doc:`getting-started` · **Secondary:** :doc:`package-catalog`

Start In 5 Minutes
------------------

**Before:** application code reads settings by string key and must remember which values are required or optional. **After:** define that contract once in a small ``Configuration`` type, then read ``ConnectionString``, ``TimeoutSeconds``, and ``ArchivePath`` as C# properties. The example uses ``VersaTul.Configurations`` and does not connect to a database or service.

Run the tested sample from the DocsVersaTul repository root:

.. code-block:: console

   dotnet run --project docs/samples/GettingStarted/GettingStarted.csproj --framework net8.0

The sample also targets ``net9.0`` and ``net10.0``. Its direct package version is pinned in ``docs/samples/Directory.Packages.props``.

.. literalinclude:: ../samples/GettingStarted/Program.cs
   :language: csharp
   :caption: Strongly typed settings sample

Expected output:

.. literalinclude:: ../samples/GettingStarted/ExpectedOutput.txt
   :language: text
   :caption: Output checked by the sample validator

Start By Problem
----------------

Use these paths if you want the quickest route to a relevant package.

1. I need strongly typed application settings: try the tested example above.
2. I need relational data access: start with :doc:`scenario-guides/sql-data-access`.
3. I need to import CSV or text data: start with :doc:`scenario-guides/file-import`.
4. I need export or formatting helpers: start with :doc:`scenario-guides/data-export`.
5. I need logging in a service or background process: start with :doc:`scenario-guides/logging-setup`.
6. I need a package starting set for my application type: start with :doc:`recommended-paths`.

Why VersaTul Is Different
-------------------------

VersaTul uses focused packages that teams can combine as a workflow grows:

1. **Choose the parts you need.** Start with one package and add adjacent packages only when useful. For logging, :doc:`logger` supplies shared contracts while :doc:`logger-file` adds a concrete file sink.
2. **Keep contracts separate from implementations.** :doc:`data-contracts` defines repository and unit-of-work contracts. Pair them with :doc:`efcore` when EF Core fits, use :doc:`sql` for provider-agnostic SQL commands, or choose :doc:`mssql` when SQL Server-specific behavior is required.
3. **Follow practical workflows.** The :doc:`scenario-guides/sql-data-access` sample uses shared in-memory SQLite, :doc:`scenario-guides/file-import` maps a checked-in CSV, and :doc:`scenario-guides/logging-setup` writes to a temporary directory. Their expected outputs are checked by the sample workflow across the three target frameworks.

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
