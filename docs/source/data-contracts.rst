Data Contracts
==============

Overview
--------

``VersaTul.Data.Contracts`` provides shared abstractions for repository-style data access, connection metadata, pagination, and unit-of-work patterns.

It is the base contract layer for data-oriented VersaTul packages such as EF Core and provider-specific access libraries.

When To Use This Package
------------------------

Use this package when you want to:

1. Define repository interfaces that stay independent of a concrete data technology.
2. Standardize unit-of-work behavior across projects.
3. Pass connection metadata through a common contract.
4. Represent paged requests and paged results consistently.
5. Add async stream support to repository abstractions.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Data.Contracts

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Data.Contracts -Version latest

Related Packages
----------------

1. :doc:`contracts` for more general-purpose abstractions.
2. :doc:`efcore` for a concrete implementation of repository and unit-of-work patterns.
3. :doc:`sql` and :doc:`mssql` for connection-oriented relational data access.

Core Types And Concepts
-----------------------

``IDataConnection``
   Standardizes how connection strings and provider names are retrieved.

``IRepository<TEntity, TKey>``
   Defines CRUD-style operations, queryable access, async reads, and range operations for a repository.

``IAsyncStreamRepository<TEntity, TKey>``
   Extends the repository model with cancellation-aware async streaming.

``IUnitOfWork``
   Defines transactional save and rollback behavior plus disposal semantics.

``IPagedRequest`` and ``PagedRequest``
   Represent page number, page size, and derived skip value.

``IPagedResult<T>`` and ``PagedResult<T>``
   Represent paged items, total count, current page, page size, and total page count.

Key Capabilities
----------------

1. Repositories support synchronous and asynchronous ``Add``, ``Find``, ``Get``, and range operations.
2. Repositories expose both ``IQueryable`` and async enumerable access patterns.
3. Paged request and result models can be reused across APIs and repository layers.
4. The contracts are flexible enough for EF Core, document databases, and custom persistence layers.

Repository Example
------------------

.. code-block:: csharp

   using VersaTul.Data.Contracts;

   public interface ICustomerRepository : IRepository<Customer, int>
   {
   }

   public class CustomerService
   {
       private readonly ICustomerRepository repository;

       public CustomerService(ICustomerRepository repository)
       {
           this.repository = repository;
       }

       public async Task<Customer> GetAsync(int id)
       {
           return await repository.GetAsync(id);
       }
   }

Paging Example
--------------

.. code-block:: csharp

   using VersaTul.Data.Contracts;

   var request = new PagedRequest
   {
       PageNumber = 2,
       PageSize = 25
   };

   var result = new PagedResult<Customer>
   {
       Items = customers,
       TotalCount = 240,
       PageNumber = request.PageNumber,
       PageSize = request.PageSize
   };

Notes
-----

1. ``IRepository<TEntity, TKey>`` is intentionally broad enough for multiple backing stores.
2. ``IAsyncStreamRepository<TEntity, TKey>`` is useful when the consumer prefers stream-first enumeration.
3. ``IUnitOfWork`` is most relevant in packages such as :doc:`efcore` where change tracking and commit behavior are explicit.
    