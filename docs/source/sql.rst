Data Sql
========

Overview
--------

``VersaTul.Data.Sql`` provides provider-agnostic relational data access built on top of ``System.Data.Common``.

It gives you a consistent way to execute stored procedures and text commands, pass parameters, switch connection names, and map result sets into your own service-layer models.

When To Use This Package
------------------------

Use this package when you want to:

1. Support relational databases through standard ADO.NET provider factories.
2. Execute stored procedures and text commands behind reusable service classes.
3. Keep SQL access logic in project-specific data services instead of controllers or handlers.
4. Read connection string and provider metadata from shared configuration.
5. Reuse synchronous and asynchronous execution patterns across multiple database engines.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Data.Sql

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Data.Sql -Version latest

Related Packages
----------------

1. :doc:`configuration` and :doc:`configuration-defaults` for settings and default SQL configuration keys.
2. :doc:`data-contracts` for shared connection abstractions.
3. :doc:`mssql` for SQL Server-specific capabilities built on this base.
4. :doc:`utilities` and :doc:`extensions` for conversion and mapping helpers commonly used inside data services.

Core Types And Concepts
-----------------------

``IDataSource`` and ``SqlDbDataSource``
   The execution surface for reads, writes, async operations, and scalar execution.

``IDataConfiguration`` and ``DataConfiguration``
   Configuration types that expose ``SqlDbConnectionName``, ``CommandTimeout``, and connection/provider lookup methods.

``ICommandFactory`` and ``CommandFactory``
   Build the underlying database command objects.

``IProviderFactory`` and ``ProviderFactory``
   Create provider-specific ADO.NET objects through registered provider factories.

``DataCommand`` and ``StoredCommand``
   Represent text commands and stored-procedure commands.

``IParameter``, ``Parameter``, ``IParameterCollection``, and ``ParameterCollection``
   Represent command parameters and parameter collections.

``BaseDataService``
   Base class for project-specific data services with helpers for readers, non-queries, scalars, and row mapping.

Key Capabilities
----------------

1. Works with any registered ADO.NET provider that supports ``DbProviderFactories``.
2. Supports synchronous and asynchronous read, write, and scalar execution paths.
3. Allows switching to a named connection at call time.
4. Uses ``BaseDataService.ProcessReader()`` to map one or many result sets into application models.
5. Supports both stored procedures and plain SQL text commands.

Basic Example
-------------

This example shows the typical pattern: configure the provider, build the SQL infrastructure, and implement a project-specific data service.

.. code-block:: csharp

   using System.Data;
   using System.Data.Common;
   using VersaTul.Configuration.Defaults.Sql;
   using VersaTul.Data.Sql;
   using VersaTul.Data.Sql.Configurations;
   using VersaTul.Data.Sql.Contracts;
   using VersaTul.Utilities;
   using VersaTul.Utilities.Contracts;

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

   var dataConfiguration = new DataConfiguration(configSettings);
   var providerFactory = new ProviderFactory();
   var commandFactory = new CommandFactory(dataConfiguration, providerFactory);
   var dataSource = new SqlDbDataSource(commandFactory);
   var utility = new CommonUtility();

Command And Mapping Example
---------------------------

``BaseDataService`` is intended to sit underneath a project-specific data service.

.. code-block:: csharp

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

Provider Notes
--------------

Common usage patterns include registering provider factories for engines such as:

1. SQL Server
2. SQLite
3. MySQL
4. PostgreSQL
5. Oracle

Notes
-----

1. ``DataConfiguration`` stores both the default connection-name key and the command timeout.
2. ``BaseDataService`` is the main extension point for application-specific repositories or data services.
3. Use :doc:`mssql` when you need SQL Server-specific types or bulk-copy integration on top of this base package.
