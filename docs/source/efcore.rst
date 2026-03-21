EFCore
======

Overview
--------

``VersaTul.Data.EFCore`` provides reusable repository and unit-of-work base classes for projects built on Entity Framework Core.

It is useful when you want consistent repository behavior across services without rewriting the same CRUD and commit logic around ``DbContext`` in every project.

When To Use This Package
------------------------

Use this package when you want to:

1. Build EF Core repositories from a shared base class.
2. Centralize ``DbContext`` commit and rollback behavior.
3. Reuse sync and async CRUD operations.
4. Add query specifications for reusable filtering logic.
5. Expose no-tracking query paths when read-only performance matters.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Data.EFCore

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Data.EFCore -Version latest

Related Packages
----------------

1. :doc:`data-contracts` for repository and unit-of-work abstractions.
2. :doc:`configuration` and :doc:`configuration-defaults` for connection-name and database settings.

Core Types And Concepts
-----------------------

``BaseRepository<TEntity, TKey>``
   Reusable EF Core repository base class with sync and async CRUD support.

``BaseUnitOfWork``
   Reusable unit-of-work base class that wraps a ``DbContext`` and provides ``Commit()``, ``CommitAsync()``, and ``Rollback()``.

``IUnitOfWork``
   EF Core unit-of-work contract extending the broader data contract model.

``IQuerySpecification<TEntity>``
   Query criteria abstraction used to compose filtered repository reads.

``DataConfiguration``
   Configuration type that exposes EF connection-name and connection-string access.

Key Capabilities
----------------

1. Repositories support sync and async CRUD paths.
2. Repositories expose ``AsQueryable()``, ``AsNoTrackingQueryable()``, and async enumeration.
3. Query specifications can be applied to queryable and async read methods.
4. ``BaseUnitOfWork`` centralizes save and rollback behavior over the EF Core change tracker.

Basic Example
-------------

.. code-block:: csharp

   using Microsoft.EntityFrameworkCore;
   using VersaTul.Data.Contracts;
   using VersaTul.Data.EFCore;

   public class PlayerData
   {
       public int Id { get; set; }
       public string Name { get; set; }
       public string FirstName { get; set; }
       public string LastName { get; set; }
   }

   public class DatabaseContext : DbContext
   {
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
   }

   public class UnitOfWork : BaseUnitOfWork
   {
       public UnitOfWork(DatabaseContext dataContext) : base(dataContext)
       {
       }
   }

   public class PlayerRepository : BaseRepository<PlayerData, int>
   {
       public PlayerRepository(VersaTul.Data.EFCore.Contracts.IUnitOfWork unitOfWork) : base(unitOfWork)
       {
       }
   }

Specification Example
---------------------

.. code-block:: csharp

   using System;
   using System.Linq.Expressions;
   using VersaTul.Data.EFCore.Contracts;

   public class ActivePlayerSpecification : IQuerySpecification<PlayerData>
   {
       public Expression<Func<PlayerData, bool>> Criteria => player => player.Name != null;
   }

   var activePlayers = await repository.GetAsync(new ActivePlayerSpecification());
   var query = repository.AsQueryable(new ActivePlayerSpecification());

Notes
-----

1. ``Rollback()`` reloads tracked entities from the database; it is not a database transaction rollback abstraction by itself.
2. ``AsNoTrackingQueryable()`` and ``GetNoTrackingAsync()`` are useful for read-only paths.
3. This package is a good fit when you want to enforce repository patterns consistently around EF Core rather than expose raw ``DbContext`` everywhere.