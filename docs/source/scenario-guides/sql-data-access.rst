SQL Data Access Workflow
========================

This guide shows a clean path for building a reusable relational data-service layer with VersaTul.

The goal is not just to execute SQL once. The goal is to create a data access shape you can keep reusing across services and repositories.

The main package combination is:

1. ``VersaTul.Data.Sql`` for provider-agnostic command execution.
2. ``VersaTul.Configurations`` and ``VersaTul.Configuration.Defaults`` for explicit connection and timeout settings.
3. ``VersaTul.Data.MsSql`` only when SQL Server-specific behavior becomes necessary.

When To Use This Workflow
-------------------------

Use this workflow when you need to:

1. Keep relational data access logic out of controllers and handlers.
2. Standardize how commands, parameters, and mapping are handled.
3. Stay provider-agnostic unless a SQL Server-specific need is proven.

Prerequisites and Tested Versions
---------------------------------

- Install a .NET SDK that supports the target framework. The sample projects target ``net8.0``, ``net9.0``, and ``net10.0``; the documentation workflow validates all three.
- The runnable sample uses a shared in-memory SQLite database. No database server, credentials, or network service is required.

The runnable sample's pinned package versions are:

.. list-table:: Tested SQL data-access sample packages
   :header-rows: 1

   * - Package
     - Version
     - Role
   * - ``VersaTul.Data.Sql``
     - ``2.0.21``
     - Provider-agnostic command execution
   * - ``VersaTul.Configurations``
     - ``1.0.18``
     - Typed configuration settings
   * - ``Microsoft.Data.Sqlite``
     - ``10.0.13``
     - In-memory ADO.NET provider used by the sample

Why This Package Combination
----------------------------

``VersaTul.Data.Sql`` supplies the command factory and data-source API used by the tutorial. ``VersaTul.Configurations`` keeps the connection name, provider name, and timeout together in the settings object that ``DataConfiguration`` consumes. The sample adds ``Microsoft.Data.Sqlite`` only as its ADO.NET provider, so it can create a shared in-memory database without a server or credentials. Choose the provider package that matches your application when adapting the sample.

``VersaTul.Data.MsSql`` is not needed for this provider-neutral round trip. Add it only when the application needs SQL Server-specific features such as bulk copy or table-valued parameters.

Step 1: Configure The Connection
--------------------------------

Register the provider and build the configuration source.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using System.Data.Common;
   using VersaTul.Configuration.Defaults.Sql;

   DbProviderFactories.RegisterFactory("Oracle.ManagedDataAccess.Client.OracleClientFactory", OracleClientFactory.Instance);

   var configSettings = new Builder().AddOrReplace(new[]
   {
       new KeyValuePair<string, object>(
           "OracleSqlDb",
           new ConnectionInfo(
               "User Id=SYS;Password=Secret;Data Source=database-address.local.com/ORCLCDB;DBA Privilege=SYSDBA;",
               "Oracle.ManagedDataAccess.Client.OracleClientFactory")),
       new KeyValuePair<string, object>("SqlDbConnectionName", "OracleSqlDb")
   }).BuildConfig();

Step 2: Build The Data Source
-----------------------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using VersaTul.Data.Sql;
   using VersaTul.Data.Sql.Configurations;

   var dataConfiguration = new DataConfiguration(configSettings);
   var providerFactory = new ProviderFactory();
   var commandFactory = new CommandFactory(dataConfiguration, providerFactory);
   var dataSource = new SqlDbDataSource(commandFactory);

This gives you a reusable execution surface for reads, writes, async operations, and scalar values.

Step 3: Put Mapping In A Service Layer
--------------------------------------

Implement a project-specific data service on top of ``BaseDataService``.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using System.Data;
   using VersaTul.Data.Sql.Contracts;

   public class ProductDataService : BaseDataService
   {
       public ProductDataService(IDataSource dataSource, INullFiltering filtering, IUtility utility)
           : base(dataSource, filtering, utility)
       {
       }

       public Product? Get(int productId)
       {
           Product? product = null;

           var commandText = @"select product_id as Id,
                                      product_name as Name,
                                      description as Description
                               from products
                               where product_id = :productId";

           var parameters = new ParameterCollection();
           parameters.Add(new Parameter("productId", productId, DbType.Int32, 0, ParameterDirection.Input));

           ProcessReader(ExecuteReader(new DataCommand(commandText, DataCommandType.Query), parameters), _ =>
           {
               product = new Product
               {
                   Id = Get((Product model) => model.Id),
                   Name = Get((Product model) => model.Name),
                   Description = Get((Product model) => model.Description)
               };
           });

           return product;
       }
   }

When To Switch To MsSql
-----------------------

Stay on ``VersaTul.Data.Sql`` if provider-agnostic access is still a requirement.

Switch to :doc:`/mssql` when you need:

1. SQL Server-specific parameter handling,
2. table-valued parameters, or
3. SQL Server bulk copy.

What You Should See
-------------------

When this workflow is working:

1. Connection and provider settings stay explicit and centralized.
2. SQL execution stays behind a reusable service abstraction.
3. Mapping logic stays consistent across queries instead of being rewritten in each caller.

Cleanup, Cancellation, and Production Notes
--------------------------------------------

- The sample's ``await using`` SQLite connection keeps the shared in-memory database alive and closes it when the program exits. The database disappears with that connection.
- The sample uses synchronous calls for its tiny fixture. For application operations, use ``WriteAsync`` and ``ExecuteScalarAsync`` overloads that accept a ``CancellationToken``. Pass values as command parameters instead of building SQL from user input.
- Provider and command failures are allowed to surface. Handle them at the service boundary; production deployments should also provision a persistent schema, use transaction boundaries where needed, and keep credentials in managed configuration or a secret store.

Runnable Sample
---------------

The complete `SqlDataAccess project <https://github.com/BjornWilliams/DocsVersaTul/tree/VT-Upgrade-And-Revisions/docs/samples/SqlDataAccess>`_ creates and queries an ephemeral SQLite database. Clone the audit branch and run it from the repository root:

.. code-block:: console

   git clone --branch VT-Upgrade-And-Revisions https://github.com/BjornWilliams/DocsVersaTul.git
   cd DocsVersaTul
   dotnet run --project docs/samples/SqlDataAccess/SqlDataAccess.csproj --framework net8.0

The project also targets ``net9.0`` and ``net10.0``; substitute either framework in the command to run those targets. The sample source is included below for reference.

The deterministic input fixture creates a ``people`` table and inserts one row:

.. code-block:: sql

   CREATE TABLE people (name TEXT NOT NULL);
   INSERT INTO people (name) VALUES ('Ada');

.. literalinclude:: ../../samples/SqlDataAccess/Program.cs
   :language: csharp
   :caption: Program.cs

Its expected console output is:

.. literalinclude:: ../../samples/SqlDataAccess/ExpectedOutput.txt
   :language: text
   :caption: Expected output

Likely Failure Messages and Fixes
---------------------------------

1. ``error NETSDK1045: The current .NET SDK does not support targeting .NET 10.0.`` — Install the .NET 10 SDK, or run the sample with ``--framework net8.0`` or ``net9.0``.
2. ``error NU1301: Unable to load the service index for source https://api.nuget.org/v3/index.json.`` — Restore network access or configure the NuGet feed that contains the pinned packages, then rerun ``dotnet restore``.
3. ``InvalidOperationException: The SQLite round trip returned an unexpected result.`` — Keep the registered SQLite provider and shared in-memory connection string from the sample, and check that the create, insert, and select commands run against the same database.

Common Mistakes
---------------

1. Starting with ``VersaTul.Data.MsSql`` before SQL Server-specific requirements are clear.
2. Keeping SQL statements in controllers, handlers, or unrelated service layers.
3. Treating connection configuration as an incidental detail instead of part of the data-access contract.

Next Step
---------

When you need SQL Server-specific behavior, continue with :doc:`/mssql`.
