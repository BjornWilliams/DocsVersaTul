Contracts
=========

Overview
--------

``VersaTul.Contracts`` contains small, reusable abstractions used across the VersaTul ecosystem.

These contracts are especially valuable when you want to keep higher-level code independent from a concrete implementation, or when you want a consistent shape for predicates, asynchronous commands, and asynchronous queries.

When To Use This Package
------------------------

Use this package when you want to:

1. Define query and command contracts without coupling to a concrete package.
2. Pass predicate expressions into repositories or data services.
3. Standardize asynchronous operations across your own application code.
4. Reuse the same abstractions that VersaTul data packages already understand.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Contracts

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Contracts -Version latest

Related Packages
----------------

1. :doc:`data-contracts` for database-oriented abstractions built on similar design principles.
2. :doc:`mongodb` and other data packages that can consume predicate-style abstractions.

Core Types And Concepts
-----------------------

``IPredicate<T>``
   Wraps an ``Expression<Func<T, bool>>`` so filtering logic can be passed around as an object.

``IAsyncExecutable`` and ``IAsyncExecutable<TInput>``
   Represent asynchronous command-style operations with no return value.

``IAsyncQuery<TOutput>`` and ``IAsyncQuery<TInput, TOutput>``
   Represent asynchronous query-style operations that return a value.

``ICancellableAsyncExecutable`` and ``ICancellableAsyncExecutable<TInput>``
   Add cancellation-token support to command-style contracts.

``ICancellableAsyncQuery<TOutput>`` and ``ICancellableAsyncQuery<TInput, TOutput>``
   Add cancellation-token support to query-style contracts.

Basic Example
-------------

``IPredicate<T>`` is commonly used to wrap filtering expressions in repository-style code.

.. code-block:: csharp

   using System;
   using System.Linq.Expressions;
   using VersaTul.Contracts;

   public class WherePredicate<TEntity> : IPredicate<TEntity>
   {
       public WherePredicate(Expression<Func<TEntity, bool>> expression)
       {
           Condition = expression;
       }

       public Expression<Func<TEntity, bool>> Condition { get; set; }
   }

   var predicate = new WherePredicate<User>(user => user.UserName.Contains(searchTerm));

That predicate object can then be passed into a repository or data service that expects an ``IPredicate<T>``.

Async Contract Example
----------------------

The async contracts are useful when you want application services to follow a clear, reusable execution shape.

.. code-block:: csharp

   using System.Threading;
   using System.Threading.Tasks;
   using VersaTul.Contracts;

   public class GetCustomerByIdQuery : ICancellableAsyncQuery<int, Customer>
   {
       public Task<Customer> ExecuteAsync(int input, CancellationToken cancellationToken = default)
       {
           // Query persistence or another service here.
           return Task.FromResult(new Customer { Id = input, Name = "Sample Customer" });
       }
   }

Notes
-----

1. These interfaces are intentionally small so they are easy to implement in your own services.
2. ``IPredicate<T>`` is particularly useful when you want to preserve LINQ expression trees instead of passing around compiled delegates.
3. The cancellable async variants are better when your code may run in web requests, background workers, or any environment where cancellation matters.