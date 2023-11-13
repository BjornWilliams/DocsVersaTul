Data MsSql
==============

Getting Started
----------------
The VersaTul Data MsSql project provides the ability to quickly create database access objects, usable on Microsoft SQL Server databases. 
This project is built on top of a combination of System.Data.Common & System.Data.SqlClient namespaces.
These are used to provide the functionality to quickly call stored procedures or plain text sql queries, and map the result into data objects using the provided helper methods. 
The project also provides MsSql Bulk Copy functionality, which can be use to bulk insert data into a MsSQL Server databases.

Installation
------------

To use VersaTul Data MsSql, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Data.MsSql -Version latest

Main Components
----------------
#. ``ISqlDataSource`` : Represent functionality to get connected to a MsSQL Database and perform CRUD operations.
#. ``ISqlParameter`` : Represents a parameter to a SqlCommand object, and optionally, its mapping to DataSet columns; and is implemented by .NET Framework data providers that access data sources.
#. ``SqlDataSource`` : Concrete implementation of ISqlDataSource interface that represent functionality to get connected to a MsSQL Database and perform CRUD operations.
#. ``SqlParameter`` : Concrete implementation of ISqlParameter interface that represent functionality to get connected to a MsSQL Database and perform CRUD operations.
#. ``BulkCopy`` : Concrete implementation of IBulkCopy interface that lets you efficiently bulk load to a SQL Server table with data from another source.

Functional Summary
------------------
#. **void BulkCopy.DoCopy()** : Overloaded method for bulk inserting a given collection of CopyDetail objects.
#. **bool BulkCopy.IsAllUploaded** : Get a value indicating if all files are inserted successfully.
#. **int BulkCopy.BatchSize** : Gets or Sets the number of rows in each batch.
#. **bool BulkCopy.EnableStreaming** : Gets or Sets a value enabling or disabling streaming data from an IDataReader object.
#. **VersaTul Data MsSql** : shares most of its functionality with :doc:`sql`. See :doc:`sql` for more details on the functionality provided.

Code Examples
-------------

.. code-block:: c#
    :caption: Simple Example Using MsSql Server as Database.

    using Microsoft.SqlServer.Server;
    using System.Data;
    using System.Data.Common;
    using System.Data.SqlClient;
    using VersaTul.Configuration.Defaults.Sql;
    using VersaTul.Data.MsSql;
    using VersaTul.Data.MsSql.Contracts;
    using VersaTul.Data.Sql;
    using VersaTul.Data.Sql.Configurations;
    using VersaTul.Utilities;
    using VersaTul.Utilities.Contracts;
    using SqlParameter = VersaTul.Data.MsSql.SqlParameter;

    namespace MsSqlDatabaseConnection
    {
        public class Program
        {
            static void Main(string[] args)
            {
                //Register factory
                DbProviderFactories.RegisterFactory("System.Data.SqlClient", SqlClientFactory.Instance);

                // Setup configuration for MsSqlServer Database quering
                var configSettings = new Builder().AddOrReplace(new[]
                {
                    new KeyValuePair<string,object>("DemoDb", new ConnectionInfo("Server=127.0.0.1;Database=DemoDb;User Id=sa;Password=Secretdatabasepassword;","System.Data.SqlClient")),
                    new KeyValuePair<string,object>("AdventureWorks2019", new ConnectionInfo("Server=127.0.0.1;Database=AdventureWorks2019;User Id=sa;Password=Secretdatabasepassword;","System.Data.SqlClient")),
                    new KeyValuePair<string, object>("SqlDbConnectionName", "AdventureWorks2019") // default to AdventureWorks2019 database.

                }).BuildConfig();

                var dataConfiguration = new DataConfiguration(configSettings);

                // Setup needed class instance
                var providerFactory = new ProviderFactory();
                var commandFactory = new CommandFactory(dataConfiguration, providerFactory);
                var sqlDataSource = new SqlDataSource(commandFactory);
                var commonUtility = new CommonUtility();

                // Create our DAL or DataService class
                var dataService = new CustomerDataService(sqlDataSource, commonUtility, commonUtility);

                // Get a customer
                var customer = dataService.GetCustomer(customerId: 10);

                // Add list of customer 
                var customers = new List<Customer>() 
                {
                    new Customer{ FirstName = "Joe", LastName = "Money" },
                    new Customer{ FirstName = "Silly", LastName = "Sally" }
                };

                var amountAdded = dataService.AddCustomers(customers);

            }
        }

        // Data Model 
        public class Customer
        {
            public int CustomerId { get; set; }
            public string? FirstName { get; set; }
            public string? LastName { get; set; }
        }

        // Setup Support for SqlServer SqlDbType.Structured.
        internal class CustomerDataRecord : List<Customer>, IEnumerable<SqlDataRecord>
        {
            IEnumerator<SqlDataRecord> IEnumerable<SqlDataRecord>.GetEnumerator()
            {
                var sqlRow = new SqlDataRecord(
                        new SqlMetaData("FirstName", SqlDbType.NVarChar, 50),
                        new SqlMetaData("LastName", SqlDbType.NVarChar, 50)
                    );

                foreach (var customer in this)
                {
                    sqlRow.SetString(0, customer.FirstName);
                    sqlRow.SetString(1, customer.LastName);

                    yield return sqlRow;
                }
            }
        }

        // Setup for Connection String switching 
        public enum ConnectionName
        {
            DemoDb,
            AdventureWorks2019
        }

        // DAL or DataServices
        public interface ICustomerDataService
        {
            Customer? GetCustomer(int customerId);
            int AddCustomers(IEnumerable<Customer> customers);
        }

        // By inheriting from BaseDataService all project specific data service will have the common functionality they need to access the dataSource. 
        public class CustomerDataService : BaseDataService, ICustomerDataService
        {
            public CustomerDataService(ISqlDataSource dataSource, INullFiltering filtering, IUtility utility) : base(dataSource, filtering, utility) { }

            public Customer? GetCustomer(int customerId)
            {
                Customer? customer = null;

                var parameterCollection = new ParameterCollection();
                parameterCollection.Add(new SqlParameter("CustomerId", customerId, SqlDbType.Int, 0, ParameterDirection.Input));

                // Using the overloaded ExecuteReader method replacing the default datable connection string with given name here.
                // ConnectionName.DemoDb.ToString() - This can come in handy when you need to talk to multiple database from the one project.
                ProcessReader(ExecuteReader(new StoredCommand("GetCustomer"), parameterCollection, ConnectionName.DemoDb.ToString()), delegate
                {
                    customer = new Customer
                    {
                        CustomerId = Get((Customer customer) => customer.CustomerId),
                        FirstName = Get((Customer customer) => customer.FirstName),
                        LastName = Get((Customer customer) => customer.LastName)
                    };
                });

                return customer;
            }

            public int AddCustomers(IEnumerable<Customer> customers)
            {
                var customersRecords = new CustomerDataRecord();
                customers.ToList().ForEach(model => customersRecords.Add(model));

                var parameterCollection = new ParameterCollection();
                
                // Note SqlParameter used here.
                parameterCollection.Add(new SqlParameter("customers", customersRecords, SqlDbType.Structured, customersRecords.Count, ParameterDirection.Input));

                // Performing a bulk insert using MsSql Server Structured data type.
                return ExecuteNonQuery(new StoredCommand("dbo.BulkInsertCustomers"), parameterCollection, ConnectionName.DemoDb.ToString());
            }
        }
    }

.. code-block:: c#
    :caption: Simple Example Using IoC and MsSQL as Database.

    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            //Configs
            var configSettings = new Builder().AddOrReplace(new[]
            {
                new KeyValuePair<string,object>("DemoDb", new ConnectionInfo("Server=127.0.0.1;Database=DemoDb;User Id=sa;Password=Secretdatabasepassword;","System.Data.SqlClient")),
                new KeyValuePair<string,object>("AdventureWorks2019", new ConnectionInfo("Server=127.0.0.1;Database=AdventureWorks2019;User Id=sa;Password=Secretdatabasepassword;","System.Data.SqlClient")),
                new KeyValuePair<string,object>("SqlDbConnectionName", "AdventureWorks2019")
            }).BuildConfig();
            
            // Registering config to help with creation of DataConfiguration class.
            builder.RegisterInstance(configSettings);

            //Singletons
            builder.RegisterType<CommonUtility>().As<IUtility>().As<INullFiltering>().As<IGenerator>().SingleInstance();
            builder.RegisterType<SqlDataSource>().As<ISqlDataSource>().As<IDataSource>().SingleInstance();
            builder.RegisterType<CommandFactory>().As<ICommandFactory>().SingleInstance();
            builder.RegisterType<ProviderFactory>().As<IProviderFactory>().SingleInstance();
            builder.RegisterType<DataConfiguration>().As<IDataConfiguration>().SingleInstance();

            //Per Dependency
            builder.RegisterType<CustomerDataService>().As<ICustomerDataService>().InstancePerLifetimeScope();
        }
    }

    // Data Service usage could look like the following:
    [Route("api/customer")]
    public class CustomerController: Controller
    {
        private readonly ICustomerDataService customerDataService;

        public CustomerController(ICustomerDataService customerDataService)
        {
            this.customerDataService = customerDataService;
        }

        [HttpGet("{id}")]
        public IActionResult GetCustomer(string id)
        {
            var customer = customerDataService.Get(id);

            if(customer == null)
                return NotFound();

            return OK(customer);
        }
         
        [HttpPost]
        public IActionResult CreateCustomers(CreateCustomerModel customerModels)
        {
            var customers = new List<Customer>();

            customerModels.ForEach(model => customers.Add(new Customer
            {
                FirstName = model.FirstName
                LastName = model.LastName
            }));

            var amountInserted = customerDataService.Add(customers);

            return OK(amountInserted);
        }
    } 