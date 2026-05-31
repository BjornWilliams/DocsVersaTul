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

Packages To Install
-------------------

.. code-block:: console

   dotnet add package VersaTul.Data.Sql
   dotnet add package VersaTul.Configurations
   dotnet add package VersaTul.Configuration.Defaults

Step 1: Configure The Connection
--------------------------------

Register the provider and build the configuration source.

.. code-block:: csharp

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

Common Mistakes
---------------

1. Starting with ``VersaTul.Data.MsSql`` before SQL Server-specific requirements are clear.
2. Keeping SQL statements in controllers, handlers, or unrelated service layers.
3. Treating connection configuration as an incidental detail instead of part of the data-access contract.

Related Package Pages
---------------------

1. :doc:`/sql`
2. :doc:`/mssql`
3. :doc:`/configuration`
4. :doc:`/configuration-defaults`

What To Read Next
-----------------

1. Read :doc:`/sql` for the full relational package surface.
2. Read :doc:`/mssql` if SQL Server-specific behavior is the next requirement.
3. Read :doc:`file-import` if the next step is ingesting flat-file data into a relational store.