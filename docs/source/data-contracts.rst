Data Contracts
==================

Getting Started
----------------
The VersaTul Data Contracts project provides generic interfaces that are supported throughout the Data manipulating projects in the VersaTul ecosystem. 
These tend to be more database-oriented projects. 
Developers who may want to change the underline implementation of these contracts can create their own implementation of such contract and supply it to the VersaTul project in which they require to change the behavior. 

Installation
------------

To use VersaTul Data Contracts, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Data.Contracts -Version latest


Main Components
----------------
#. ``IDataConnection`` : Represent the Database Connection details needed to connect to a database.
#. ``IRepository<TEntity, TKey>`` : Represents a collection of functionality that can be performed on a data store.
#. ``IUnitOfWork`` : Represents the absolute unit of work to be sent to a database.

Functional Summary
------------------
#. **string IDataConnection.GetConnectionString()** : Overloaded methods for getting the ConnectionString for the current application's default configuration.
#. **string IDataConnection.GetProviderName()** : Overloaded methods for getting the fully qualified provider name.
#. **TEntity IRepository<TEntity, TKey>.Add()** : Overloaded methods for adding the given entity to the data store.
#. **void IRepository<TEntity, TKey>.AddRange()** : Overloaded methods for adding the given entities to the data store.
#. **TEntity IRepository<TEntity, TKey>.Find()** : Overloaded methods for finding an entity with the given primary key values.
#. **TEntity IRepository<TEntity, TKey>.Get()** : Overloaded methods for getting entities in the data Store.
#. **TEntity IRepository<TEntity, TKey>.Update()** : Overloaded methods for updating entities in the data store.
#. **TEntity IRepository<TEntity, TKey>.Remove()** : Overloaded methods for deleting entities from the data store.
#. **TEntity IUnitOfWork.Commit()** : Overloaded methods for saving the changes from the DbContext out the database..
#. **TEntity IUnitOfWork.Rollback()** : Pull data from database and override changes in the Change Tracker. This method is not a true rollback in the database.

Code Examples
-------------

.. code-block:: c#
    :caption: Example implementation as found in VersaTul.Data.EFCore.

    // code shortened for breviate.
    public abstract class BaseRepository<TEntity, TKey> : IRepository<TEntity, TKey> where TEntity : class, new()
    {
        public TEntity Add(TEntity entity)
        {
            if (entity == null) { throw new ArgumentNullException(nameof(entity), "Argument cannot be null."); }

            return this.entity.Add(entity).Entity;
        }

        public void AddRange(IEnumerable<TEntity> entities) => entity.AddRange(entities);

        public TEntity Find(params object[] keyValues) => entity.Find(keyValues);
    }

    // code shortened for breviate.
    public abstract class BaseUnitOfWork : IUnitOfWork
    {
        public int Commit() => DataContext.SaveChanges();

        public void Rollback()
        {
            DataContext
                .ChangeTracker
                .Entries()
                .ToList()
                .ForEach(set => set.Reload());
        }
    }

    // code shortened for breviate.
    public class ConnectionInfo : IConnectionInfo
    {
        public ConnectionInfo(string connectionString, string providerName)
        {
            ConnectionString = connectionString;

            ProviderName = providerName;
        }
       
        public string ConnectionString { get; }

        public string ProviderName { get; }        
    }



Changelog
-------------

V1.0.8

* Dependent package updates
* Minor fixes

V1.0.7

* Code ported to dotnet core
* Documentaion completed
    