Caching
=======

Overview
--------

``VersaTul.Caching`` provides a simple cache abstraction with a ready-to-use in-memory implementation built on ``Microsoft.Extensions.Caching.Memory``.

The package is useful when you want your application code to depend on a small cache contract instead of directly depending on the underlying cache engine.

When To Use This Package
------------------------

Use this package when you want to:

1. Cache frequently accessed objects in memory.
2. Hide the underlying cache implementation behind an interface.
3. Configure default cache duration from a shared configuration model.
4. Use absolute or sliding expiration policies.
5. React to cache item eviction events.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Caching

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Caching -Version latest

Related Packages
----------------

1. :doc:`configuration` for key/value configuration access.
2. :doc:`configuration-defaults` for baseline cache settings such as ``CacheDuration``.

Core Types And Concepts
-----------------------

``ICacheProvider`` and ``ICacheProvider<T>``
   The main cache abstraction for reading, writing, removing, and clearing cached entries.

``MemCacheProvider<T>``
   The default in-memory cache implementation.

``ICacheConfiguration`` and ``CacheConfiguration``
   Configuration types that provide settings such as the default cache duration.

``CacheExpiration``
   Expiration model for absolute or sliding expiration.

``ICacheClock``
   Clock abstraction used for expiration calculations and time-sensitive testing.

``MemCacheEventArgs``
   Event payload used when an item is removed from the cache.

Key Capabilities
----------------

1. ``Get()`` and ``GetAsync()`` return cached values or the default value for ``T`` on a cache miss.
2. ``Add()`` and ``SetAsync()`` support default duration, explicit duration, and ``CacheExpiration`` overloads.
3. ``IsExists()`` checks whether a key is present.
4. ``Remove()`` and ``Clear()`` remove one or all entries.
5. ``ItemRemoved`` lets you observe cache evictions.
6. ``MemCacheProvider<T>`` supports injecting ``MemoryCacheOptions``, ``ILoggerFactory``, and a custom ``ICacheClock``.

Basic Example
-------------

.. code-block:: csharp

   using VersaTul.Caching;
   using VersaTul.Caching.Configurations;
   using VersaTul.Caching.Contracts;
   using VersaTul.Configuration.Defaults.Caching;

   var configSettings = new Builder().BuildConfig();
   var cacheConfiguration = new CacheConfiguration(configSettings);

   ICacheProvider<Person> cacheProvider = new MemCacheProvider<Person>(cacheConfiguration);

   var person = new Person { Age = 10, Name = "Bjorn" };

   cacheProvider.Add("Bjorn", person);

   var cachedPerson = cacheProvider.Get("Bjorn");

Expiration Example
------------------

Use ``CacheExpiration`` when you want explicit absolute or sliding expiration behavior.

.. code-block:: csharp

   using VersaTul.Caching;

   cacheProvider.Add(
       "user:42",
       person,
       new CacheExpiration
       {
           Sliding = TimeSpan.FromMinutes(15)
       });

Async And Eviction Example
--------------------------

.. code-block:: csharp

   cacheProvider.ItemRemoved += (_, args) =>
   {
       Console.WriteLine($"Removed cache item {args.Key} because {args.Reason}");
   };

   await cacheProvider.SetAsync("profile:42", person, 120);
   var cached = await cacheProvider.GetAsync("profile:42");

Notes
-----

1. The default ``Add(key, value)`` overload uses ``CacheDuration`` from ``ICacheConfiguration``.
2. ``CacheExpiration`` must contain either an absolute or sliding value.
3. Inject a custom ``ICacheClock`` when you need deterministic time behavior in tests.