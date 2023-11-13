Data Sql
================

Getting Started
----------------
The VersaTul Data Sql project provides the ability to quickly create database access objects, 
usable on any supporting SQL databases. This project is built on top of the **System.Data.Common** namespace and
provides the functionality to quickly call stored procedures or plain text sql queries, then map the result into data objects using the provided helper methods.

Installation
------------

To use VersaTul Data Sql, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Data.Sql -Version latest

Main Components
----------------
#. ``IDataSource`` : Represents a composite of the Data role interfaces that provides read and write capabilities.
#. ``IProviderFactory`` : Represents a set of methods for creating instances of a provider's implementation of the data source classes.
#. ``IDataConfiguration`` : Represents a set of methods or properties for getting configuration values from setting store.
#. ``IParameter`` : Represents the set of properties and methods that describes a parameter passed into the Sql Command.
#. ``IParameterCollection`` : Represents a collection of IParameter objects.
#. ``IConnectionInfo`` : Represents a connection string details.
#. ``SqlDbDataSource`` :  Represent a default implementation of the IDataSource interface.
#. ``BaseDataService`` : Provides a starting point for custom data services used in projects. Provides all the basic or general database functionality.
#. ``ConnectionInfo`` : Represents a connection string info.
#. ``Parameter`` : Represents a parameter to a Command and optionally its mapping to DataSet columns.
#. ``ProviderFactory`` : Represents a set of methods for creating instances of a provider's implementation of the data source classes.
#. ``DataConfiguration`` : Provides a set of methods or properties for getting configuration values from setting store.
#. ``BulkCopy`` : Represents the functionality needed to efficiently bulk load a SQL Server table with data from another source.

Functional Summary
------------------
#. **DbDataReader BaseDataService.ExecuteReader()** : Overloaded method for reading a forward-only stream of rows from the data source.
#. **int BaseDataService.ExecuteNonQuery()** : Overloaded method for executing a given stored procedure and returns the affected number of rows count.
#. **void BaseDataService.ProcessReader(DbDataReader reader, ProccessReaderHandler handler)** : Helper method to iterate the given data reader and provide access to the data at each row via the helper methods. For example GetInt(),GetString(), or Get<TInput, TResult>().
#. **void ParameterCollection.Add(IParameter parameter)** : Adds the given IParameter object to the end of the parameter collection List.

Code Examples
-------------
.. code-block:: c#
    :caption: Simple Example Using Oracle as Database.

    using System.Data;
    using VersaTul.Configuration.Defaults.Sql;
    using VersaTul.Data.Sql;
    using VersaTul.Data.Sql.Configurations;
    using VersaTul.Data.Sql.Contracts;
    using VersaTul.Extensions;
    using VersaTul.Utilities;
    using VersaTul.Utilities.Contracts;

    namespace SqlDatabaseConnection
    {
        public class Program
        {
            static void Main(string[] args)
            {
                // Supported database engines.
                //MSSQL ---> System.Data.SqlClient.SqlClientFactory
                //SQLite ---> System.Data.SQLite.SQLiteFactory
                //MySql ---> MySql.Data.MySqlClient.MySqlClientFactory
                //PostgreSql ---> Npgsql.NpgsqlFactory
                //Oracle ---> Oracle.ManagedDataAccess.Client.OracleClientFactory

                //Register factory
                DbProviderFactories.RegisterFactory("Oracle.ManagedDataAccess.Client.OracleClientFactory", OracleClientFactory.Instance);

                // Setup configuration for Oracle Database querying
                var configSettings = new Builder().AddOrReplace(new[]
                {
                    //Tested with nuget package Oracle.ManagedDataAccess.Core Version 3.21.90
                    new KeyValuePair<string, object>("OracleSqlDb", new ConnectionInfo("User Id=SYS;Password=Secretdatabasepassword;Data Source=database-address.local.com/ORCLCDB;DBA Privilege=SYSDBA;", "Oracle.ManagedDataAccess.Client.OracleClientFactory")),
                    new KeyValuePair<string, object>("SqlDbConnectionName", "OracleSqlDb")

                }).BuildConfig();

                var dataConfiguration = new DataConfiguration(configSettings);

                // Setup needed class instance
                var providerFactory = new ProviderFactory();
                var commandFactory = new CommandFactory(dataConfiguration, providerFactory);
                var sqlDbDataSource = new SqlDbDataSource(commandFactory);
                var commonUtility = new CommonUtility();

                // Create our DAL or DataService class
                var dataService = new ProductDataService(sqlDbDataSource, commonUtility, commonUtility);

                // Get all products
                var products = dataService.Get();

                // get a known product 
                var product = dataService.Get(100);

                // Add a new product 
                var newProduct = dataService.Add(new Product
                {
                    CategoryId = 1,
                    Description = "Some product description",
                    ListPrice = 100.99m,
                    Name = "A cool Product Name",
                    StandardCost = 50.99m
                });

            }
        }

        // Data Model 
        public class Product
        {
            public int Id { get; set; }
            public string? Name { get; set; }
            public string? Description { get; set; }
            public decimal StandardCost { get; set; }
            public decimal ListPrice { get; set; }
            public int CategoryId { get; set; }
        }

        // DAL Or Data Service layer
        public interface IProductService
        {
            Product Add(Product product);
            Product? Get(int productId);
            IEnumerable<Product> Get();
        }

        // By inheriting from BaseDataService all project specific data service will have the common functionality they need to access the dataSource.        
        public class ProductDataService : BaseDataService, IProductService
        {
            public ProductDataService(IDataSource dataSource, INullFiltering filtering, IUtility utility) : base(dataSource, filtering, utility) { }

            // using stored command example 
            public IEnumerable<Product> Get()
            {
                var products = new List<Product>();

                // using the ProcessReader method to read the return DbDataReader from ExecuteReader.
                // technique commonly used to populate data models from returned data. 
                ProcessReader(ExecuteReader(new StoredCommand("GetAllProducts")), (position) =>
                {
                    // position parameter: useful for multiple result sets, this value represents which reader is currently being read from in the result set.
                    // this information can then be used to populate different models in the lambda helper method. 
                    products.Add(new Product
                    {
                        CategoryId = Get((Product prod) => prod.CategoryId),
                        Description = Get((Product prod) => prod.Description),
                        Id = Get((Product prod) => prod.Id),
                        ListPrice = Get((Product prod) => prod.ListPrice),
                        Name = Get((Product prod) => prod.Name),
                        StandardCost = Get((Product prod) => prod.StandardCost)
                    });
                });

                return products;
            }

            // using command text example 
            public Product? Get(int productId)
            {
                Product? product = null;

                var commandText = @"select  product_id as Id,
                                            product_name as Name,
                                            description as Description,
                                            standard_cost as StandardCost,
                                            list_price as ListPrice,
                                            category_id as CategoryId
                                    from products
                                    where product_id = :productId";

                var parameterCollection = new ParameterCollection();
                parameterCollection.Add(new Parameter("productId", productId, DbType.Int32, 0, ParameterDirection.Input));

                // using the ProcessReader method to read the return DbDataReader from ExecuteReader.
                // technique commonly used to populate data models from returned data. 
                ProcessReader(ExecuteReader(new DataCommand(commandText, DataCommandType.Query), parameterCollection), (position) =>
                {
                    product = new Product
                    {
                        CategoryId = Get((Product prod) => prod.CategoryId),
                        Description = Get((Product prod) => prod.Description),
                        Id = Get((Product prod) => prod.Id),
                        ListPrice = Get((Product prod) => prod.ListPrice),
                        Name = Get((Product prod) => prod.Name),
                        StandardCost = Get((Product prod) => prod.StandardCost)
                    };
                });

                return product;
            }

            // using stored procedure to insert data.
            public Product Add(Product product)
            {
                var parameterCollection = new ParameterCollection();
                parameterCollection.Add(new Parameter("description", product.Description, DbType.String, 500, ParameterDirection.Input));
                parameterCollection.Add(new Parameter("standard_cost", product.StandardCost, DbType.Decimal, 0, ParameterDirection.Input));
                parameterCollection.Add(new Parameter("product_name", product.Name, DbType.String, 500, ParameterDirection.Input));
                parameterCollection.Add(new Parameter("list_price", product.ListPrice, DbType.Decimal, 0, ParameterDirection.Input));
                parameterCollection.Add(new Parameter("category_id", product.CategoryId, DbType.Int32, 0, ParameterDirection.Input));
                parameterCollection.Add(new Parameter("product_id", product.Id, DbType.Int32, 0, ParameterDirection.Output));

                ExecuteNonQuery(new StoredCommand("InsertProduct"), parameterCollection);

                product.Id = parameterCollection["product_id"].Value.To<int>();

                return product;
            }
        }
    }


.. code-block:: c#
    :caption: Simple Example Using IoC and Oracle as Database.

    // AutoFac as IoC container
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            //Configs
            var configSettings = new Builder().AddOrReplace(new[]
            {
                new KeyValuePair<string,object>("OracleSqlDb", new ConnectionInfo("User Id=SYS;Password=Secretdatabasepassword;Data Source=database-address.local.com/ORCLCDB;DBA Privilege=SYSDBA;","Oracle.ManagedDataAccess.Client.OracleClientFactory")),
                new KeyValuePair<string, object>("SqlDbConnectionName", "OracleSqlDb")
            }).BuildConfig();

            // Registering config to help with creation of DataConfiguration class.
            builder.RegisterInstance(configSettings);

            //Singletons
            builder.RegisterType<CommonUtility>().As<IUtility>().As<INullFiltering>().As<IGenerator>().SingleInstance();
            builder.RegisterType<SqlDbDataSource>().As<IDataSource>().SingleInstance();
            builder.RegisterType<CommandFactory>().As<ICommandFactory>().SingleInstance();
            builder.RegisterType<ProviderFactory>().As<IProviderFactory>().SingleInstance();
            builder.RegisterType<DataConfiguration>().As<IDataConfiguration>().SingleInstance();

            //Per Dependency
            builder.RegisterType<EmployeeDataService>().As<IEmployeeService>().InstancePerLifetimeScope();
            builder.RegisterType<ProductDataService>().As<IProductService>().InstancePerLifetimeScope();
        }
    }

    // Data Service usage could look like the following:
    [Route("api/product")]
    public class ProductController: Controller
    {
        private readonly IProductService productService;

        public ProductController(IProductService productService)
        {
            this.productService = productService;
        }

        // Get
        [HttpGet]
        public IActionResult GetProducts()
        {
            var products = productService.Get();

            return OK(products);
        }

        [HttpGet("{id}")]
        public IActionResult GetProduct(string id)
        {
            var product = productService.Get(id);

            if(product == null)
                return NotFound();

            return OK(product);
        }
         
        [HttpPost]
        public IActionResult CreateProduct(CreateProductModel model)
        {
            var product = productService.Add(new Product
            {
                Name = model.Name
                Description = model.Description
                StandardCost = model.StandardCost
                ListPrice = model.ListPrice
                CategoryId = model.CategoryId
            });

            return OK(product);
        }
    } 