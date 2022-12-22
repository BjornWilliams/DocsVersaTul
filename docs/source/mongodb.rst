Data MongoDB
================

Getting Started
----------------
The VersaTul Data MongoDB project provides a set of functionality for working with a MongoDB Database.
The project provides the ability to adds a single document, add a list of entities to a collection and many other functions.
It provides a base repository to support the repository pattern of accessing a database.

Installation
------------

To use VersaTul.Data.MongoDB, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Data.MongoDB -Version latest


Main Components
----------------
1. ``IRepository<TEntity, TKey>`` : Interface to support commong CRUD operations.
2. ``IDataConfiguration<TKey>`` : Interface for Configuration settings.
3. ``DataConfiguration<TKey>`` : Default implementation for Data Configuration interface. 
4. ``BaseRepository<TEntity, TMap, TKey>`` : Abstract class providing commong functionality for working with a MongoDB Database.
5. ``WherePredicate<TEntity>`` : Helper for generating search conditional expressions.
6. ``Entity`` : Abstract Entity for all the Business Entities.

Functional Summary
------------------
1. **TEntity Add(TEntity entity)** : Adds a single document.
2. **Add(IEnumerable<TEntity> entities)** : Adds the list of entities to the collection.
3. **IEnumerable<TEntity> Find(IPredicate<TEntity> predicate)** : Lazy loads any entity that matches given condiction.
4. **TEntity GetById(TKey id)** : Gets an entity for the given identifier.
5. **TEntity Update(TEntity entity)** : Updates a single entity.
6. **void Update(IEnumerable<TEntity> entities)** : Updates a collection with the given list of entities.
7. See :doc:`configuration-defaults` for more configuration settings.

Code Examples
-------------