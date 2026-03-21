Data MongoDB
============

Overview
--------

``VersaTul.Data.MongoDB`` provides repository-oriented access to MongoDB collections, along with configuration, mapping, connection override, and entity abstractions.

It is designed for projects that want MongoDB access wrapped in reusable repositories instead of scattering driver code throughout the application.

When To Use This Package
------------------------

Use this package when you want to:

1. Build MongoDB repositories around strongly typed entities.
2. Define collection mapping and serialization behavior in one place.
3. Use predicate-based filtering while keeping repository code reusable.
4. Override connection targets dynamically for the same repository shape.
5. Keep MongoDB configuration concerns separated from business logic.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Data.MongoDB

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Data.MongoDB -Version latest

Related Packages
----------------

1. :doc:`contracts` for predicate abstractions used by ``WherePredicate<TEntity>``.
2. :doc:`configuration-defaults` for MongoDB-related defaults such as timeout and connection-name keys.
3. :doc:`data-contracts` for broader repository and data-abstraction patterns elsewhere in the ecosystem.

Core Types And Concepts
-----------------------

``IDataConfiguration<TKey>`` and ``DataConfiguration<TKey>``
   MongoDB configuration types that expose connection name, timeout values, SSL settings, working database name, and collection lookup helpers.

``IEntity<TKey>`` and ``Entity``
   Entity abstractions for MongoDB document models.

``IRepository<TEntity, TKey>`` and ``BaseRepository<...>``
   Repository contracts and base implementations for CRUD, query, count, delete, update, and async operations.

``IEntityMap<TEntity>`` and ``BaseMap<TEntity>``
   Mapping abstractions for collection registration and BSON class-map configuration.

``WherePredicate<TEntity>``
   Predicate wrapper for repository filtering.

``CollectionName``
   Attribute for explicitly controlling collection naming.

Key Capabilities
----------------

1. Repositories expose synchronous and asynchronous CRUD operations.
2. Repositories are queryable and can be composed with LINQ.
3. Collection name resolution supports attributes and base-entity conventions.
4. Configuration can create typed collections from connection strings or ``MongoUrl`` instances.
5. Connection overrides let one repository shape target a different configured database.

Basic Repository Example
------------------------

.. code-block:: csharp

   using VersaTul.Data.MongoDB;
   using VersaTul.Data.MongoDB.Contracts;

   public class Car : Entity
   {
       public string Make { get; set; }
       public string Model { get; set; }
       public int Year { get; set; }
   }

   public class CarMap : BaseMap<Car>
   {
       public CarMap() : base("cars")
       {
       }
   }

   public interface ICarRepository : IRepository<Car>
   {
   }

   public class CarRepository : BaseRepository<Car, IEntityMap<Car>>, ICarRepository
   {
       public CarRepository(IDataConfiguration<string> configuration, IEntityMap<Car> entityMap)
           : base(configuration, entityMap)
       {
       }
   }

Filtering Example
-----------------

.. code-block:: csharp

   var cars = carRepository.Find(
       new WherePredicate<Car>(model => model.Make.Contains(searchTerm) || model.Model.Contains(searchTerm)));

Connection Override Notes
-------------------------

The repository base supports connection override patterns, which are useful when the same repository shape needs to target another configured database.

This is powerful, but it also means lifetime management matters. If you register repositories as singletons and change the active connection, that change can persist longer than you intended.

Notes
-----

1. ``DataConfiguration<TKey>`` centralizes collection naming, timeouts, and connection-string access.
2. ``BaseMap<TEntity>`` is the right place for BSON class-map customization and nested serializer setup.
3. ``WherePredicate<TEntity>`` keeps filtering expressions explicit and reusable.
