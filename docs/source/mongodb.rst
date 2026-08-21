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

``NoMap<TEntity>``
   A valid no-op map for repositories that rely on entity attributes or conventions. It exposes no extra-elements accessor and performs no class-map registration.

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
6. Repository predicates use MongoDB's native LINQ provider without an EF Core-specific expression dependency.

MongoDB Client Configuration
----------------------------

``DataConfiguration<TKey>`` composes TCP socket keep-alive setup and command-started event subscriptions in the same MongoDB cluster configurator. Registering command-event logging therefore preserves the configured socket behavior.

Within a ``DataConfiguration<TKey>`` instance, database resolution reuses one ``MongoClient`` for each normalized set of effective client settings. Repeated collection resolution therefore shares the driver's connection pool.

Command names remain available to ``LogCommand``, while payload logging is disabled by default. Set ``LogCommandPayload`` to ``true`` to include a sanitized payload; credential and common personal-data fields are always redacted, and additional comma-separated names can be supplied through ``CommandLogRedactedFields``.

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

The repository base supports connection override patterns, which are useful when the same repository shape needs to target another configured database. An override applies to the current async execution context; the repository's default collection remains unchanged, and concurrent contexts can select different connections without changing one another's active collection.

When using a singleton repository, select the override within the operation that needs it and keep subsequent work in that async flow. Do not treat a connection override as a process-wide repository setting.

Query and callback methods reject null predicates and callbacks with ``ArgumentNullException`` before contacting MongoDB. Async query methods honor a pre-cancelled ``CancellationToken``. ``ForEachAsync`` also checks cancellation before each callback, so cancellation cannot start another callback in the same cursor batch.

Notes
-----

1. ``DataConfiguration<TKey>`` centralizes collection naming, timeouts, and connection-string access.
2. ``BaseMap<TEntity>`` is the right place for BSON class-map customization and nested serializer setup.
3. ``WherePredicate<TEntity>`` keeps filtering expressions explicit and reusable.
