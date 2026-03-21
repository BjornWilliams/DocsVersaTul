Data MsSql
==========

Overview
--------

``VersaTul.Data.MsSql`` adds SQL Server-specific capabilities on top of :doc:`sql`, including SQL Server parameters, SQL Server data-source types, and a concrete ``IBulkCopy`` implementation.

Use it when you want the general service-oriented relational access model from ``VersaTul.Data.Sql`` but need SQL Server features such as structured parameters or transactional bulk import.

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

Notes
-----

1. If you only need generic relational access, start with :doc:`sql`.
2. Choose ``VersaTul.Data.MsSql`` when you need SQL Server-specific parameters or bulk import.
3. ``BulkCopy`` is designed as an all-or-nothing upload path and will attempt rollback on failure.
