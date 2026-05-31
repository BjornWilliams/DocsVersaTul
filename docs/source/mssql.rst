Data MsSql
==========

Overview
--------

``VersaTul.Data.MsSql`` adds SQL Server-specific capabilities on top of :doc:`sql`, including SQL Server parameters, SQL Server data-source types, and a concrete ``IBulkCopy`` implementation.

Use it when you want the general service-oriented relational access model from ``VersaTul.Data.Sql`` but need SQL Server features such as structured parameters or transactional bulk import.

Why Use This Package
--------------------

Choose this package when SQL Server is not just one possible provider but an intentional platform choice.

Its strongest adoption value comes from removing the need to build your own SQL Server bulk-copy wrapper and parameter-handling layer.

When To Use This Package
------------------------

Use this package when you want to:

1. Target Microsoft SQL Server specifically.
2. Reuse the ``BaseDataService`` workflow with SQL Server-specific types.
3. Pass SQL Server parameters such as structured values.
4. Bulk import ``IDataReader`` data into SQL Server tables.
5. Validate and upload multiple bulk-copy items in a single transaction.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Data.MsSql

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Data.MsSql -Version latest

Related Packages
----------------

1. :doc:`sql` for the provider-agnostic relational foundation.
2. :doc:`bulk` for shared bulk-copy abstractions and result models.
3. :doc:`file-reader` for producing ``IDataReader`` sources from files.
4. :doc:`scenario-guides/file-import` for a file-to-SQL Server import workflow.
5. :doc:`scenario-guides/sql-data-access` for a relational data-service workflow.

Start Here If
-------------

1. You know SQL Server is the target database.
2. You need structured parameters, table-valued parameters, or SQL Server bulk import.
3. Your import workflow already produces ``IDataReader`` input and now needs a concrete upload path.

Not The Right First Package If
------------------------------

1. Database portability still matters.
2. You only need generic relational reads and writes.
3. You are still solving file parsing or export generation instead of SQL Server-specific data access.

Works Well With
---------------

1. :doc:`sql` when you want to understand the provider-agnostic base model first.
2. :doc:`bulk` for shared copy-detail and mapping contracts.
3. :doc:`file-reader` when import files are the source for bulk upload.
4. :doc:`scenario-guides/file-import` for a full import workflow.

Core Types And Concepts
-----------------------

``ISqlDataSource`` and ``SqlDataSource``
   SQL Server-specialized data source types layered on the generic SQL package.

``ISqlParameter`` and ``SqlParameter``
   SQL Server-specific parameter types.

``IDataConfiguration`` and ``DataConfiguration``
   SQL Server configuration types that add ``BulkCopyTimeout`` to the base SQL configuration surface.

``BulkCopy``
   Concrete ``IBulkCopy`` implementation for SQL Server uploads.

``IBulkCopyService`` and validator/wrapper types
   Internal service layer used to validate and execute SQL Server bulk-copy operations.

``TableValuedParameter``
   Support for SQL Server table-valued or structured parameter scenarios.

Key Capabilities
----------------

1. Inherits most relational query and command features from :doc:`sql`.
2. Supports SQL Server-specific parameters through ``SqlParameter``.
3. Supports all-or-nothing transactional bulk-copy behavior.
4. Supports async bulk copy and optional progress callbacks.
5. Uses ``BulkCopyTimeout`` from configuration during upload operations.

Basic Data-Service Example
--------------------------

.. code-block:: csharp

   using System.Data.Common;
   using System.Data.SqlClient;
   using VersaTul.Configuration.Defaults.Sql;
   using VersaTul.Data.MsSql;
   using VersaTul.Data.MsSql.Contracts;
   using VersaTul.Data.Sql;

   DbProviderFactories.RegisterFactory("System.Data.SqlClient", SqlClientFactory.Instance);

   var configSettings = new Builder().AddOrReplace(new[]
   {
       new KeyValuePair<string, object>(
           "AdventureWorks2019",
           new ConnectionInfo(
               "Server=127.0.0.1;Database=AdventureWorks2019;User Id=sa;Password=Secret;",
               "System.Data.SqlClient")),
       new KeyValuePair<string, object>("SqlDbConnectionName", "AdventureWorks2019")
   }).BuildConfig();

   var dataConfiguration = new VersaTul.Data.MsSql.Configurations.DataConfiguration(configSettings);
   var providerFactory = new ProviderFactory();
   var commandFactory = new CommandFactory(dataConfiguration, providerFactory);
   var dataSource = new SqlDataSource(commandFactory);

Bulk Copy Example
-----------------

The bulk-copy path is the main reason to choose this package over the provider-agnostic SQL package alone.

.. code-block:: csharp

   using VersaTul.Data.Bulk;
   using VersaTul.Data.MsSql.Bulk;

   var copyDetail = new CopyDetail(
       destinationName: "Persons",
       reader: peopleReader,
       columnMappings: new[]
       {
           new BulkCopyColumnMapping<Person, Person>(model => model.Name, model => model.Name),
           new BulkCopyColumnMapping<Person, Person>(model => model.Age, model => model.Age)
       });

   var result = await bulkCopy.DoCopyAsync(
       new[] { copyDetail },
       dBConnectionName: "AdventureWorks2019",
       progressCallback: progress => Console.WriteLine($"Processed {progress.ProcessedItems} items"));

Expected Result
---------------

When this package is the right fit:

1. SQL Server-specific requirements stay in one package boundary,
2. bulk imports use a supported concrete implementation instead of custom upload code, and
3. application code does not need to reinvent transaction-aware bulk copy.

Next Step
---------

1. Read :doc:`scenario-guides/file-import` if the next requirement is CSV or text import into SQL Server.
2. Read :doc:`bulk` if you want deeper mapping-model detail.
3. Go back to :doc:`sql` if you need to compare the SQL Server-specific path against the provider-agnostic base path.

Notes
-----

1. If you only need generic relational access, start with :doc:`sql`.
2. Choose ``VersaTul.Data.MsSql`` when you need SQL Server-specific parameters or bulk import.
3. ``BulkCopy`` is designed as an all-or-nothing upload path and will attempt rollback on failure.
