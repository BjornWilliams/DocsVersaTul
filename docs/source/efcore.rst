EFCore
================

Getting Started
----------------
The VersaTul EFCore project provides the ability to quickly create project specific database repositories running on Microsoft Entity Framework Core ORM.
This project provides generic repository functionality that can be reused to create project specific repositories.
CRUD operations are defined both Synchronous and Asynchronous methods.

Installation
------------

To use VersaTul EFCore, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.EFCore -Version latest

Main Components
----------------
#. ``IUnitOfWork`` : Provides the functionality needed to support absolute unit of work.
#. ``BaseRepository<TEntity, TKey>`` : Abstract class that provides common functionality for CRUD operations.
#. ``BaseUnitOfWork`` : Default implementation of **IUnitOfWork**. 
#. ``DataConfiguration``` : Default implementation of the Configuration needed to connect to database.


Functional Summary
------------------
#. **TEntity Add(TEntity entity)** : Add the given entity to the database.
#. **TEntity Find(params object[] keyValues)** : Finds an entity with the given primary key values.
#. **IEnumerable<TEntity> Get()** : Gets all entities from the database.
#. **TEntity Update(TEntity entity)** : Updates the given entity in the database.
#. **TEntity Remove(TEntity entity)** : Deletes the given entity from the database.

Code Examples
-------------

.. code-block:: c#
    :caption: Sample Repository Database Call

    //DataModel
    public class PlayerData
    {
        public int Id { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public DateTime CreatedDate { get; set; }
    }

    //Create DbContext class
    public class DatabaseContext : DbContext
    {
        // IDataConnection - will be supplied from container 
        // provides framework for get connection string
        private readonly IDataConnection dataConnection;
        
        public DatabaseContext(IDataConnection dataConnection)
        {
            this.dataConnection = dataConnection;
        }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer(dataConnection.GetConnectionString());
            }
        }

        public DbSet<PlayerData> Players { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<PlayerData>().HasKey(x => x.Id);
        }
    }