Caching
================

Getting Started
----------------
The VersaTul Caching project is designed to provide a simplfied caching interface with the ability to change the underlining caching engine easily and quickly. 
The default cache engine is built on top of the Microsoft Extensions Caching Memory class, which provides an in memory caching store. 
This implementation can be easily replaced using the interface provided.

.. _installation:

Installation
------------

To use VersaTul Caching, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Caching -Version latest


Components
-----------
1. ``ICacheProvider<T>`` : Interaction can be achieved through the Cache Provider Interface.
2. ``MemCacheProvider<T>`` : Default Concrete implementation of the Cache Provider interface.
3. ``ICacheConfiguration`` : The Configuration interface for accessing default configurations 
4. ``CacheConfiguration`` : Default Concrete implementation of the configuration interface. 

Functional Summary
------------------
1. **T Get(string key)** : Retrieves the cache entry for the given key. If the cache entry is not found then the default of T is returned.
2. **void Add(string key, T data)** : Inserts the cache entry using the key for a default duration of 60 minutes.
3. **void Add(string key, T data, int cacheTime)** : Inserts the given item into the Cache using the given key for a the specified duration in minutes.
4. **void Add(string key, T data, CacheExpiration expiration)** : Inserts the given item into the Cache using the given key for a the specified CacheExpiration.
5. **bool IsExists(string key)** : Indicates if there is a cache entry for the key.
6. **void Remove(string key)** : Removes the cache entry from the cache for the given key.

Code Examples
-------------

.. code-block:: c#
    :caption: Simple Example

    
    class Program
    {
        static void Main(string[] args)
        {
            //default configs
            var configSettings = new Builder().BuildConfig();
            
            //cache configuration
            var cacheConfiguration = new CacheConfiguration(configSettings);

            var cacheProvider = new MemCacheProvider<Person>(cacheConfiguration);

            person = new Person { Age = 10, Name = "Bjorn" };

            cacheProvider.Add("Bjorn", person);

            var person = cacheProvider.Get("Bjorn");
        }
        Console.ReadLine();
    }

.. code-block:: c#
    :caption: Use With a IoC Container
    
    
    //Creating the IoC container
    var builder = new ContainerBuilder();

    //default configs
    var configSettings = new Builder().BuildConfig();

    //Populating the container
    builder
        .RegisterType<CacheConfiguration>()
        .As<ICacheConfiguration>()
        .WithParameter("configSettings", configSettings)
        .SingleInstance();

    builder
        .RegisterGeneric(typeof(MemCacheProvider<>))
        .As(typeof(ICacheProvider<>))
        .SingleInstance();

    //Static method where cache provider can be injected by autofac...
    static void CachingTest(ICacheProvider<Person> cacheProvider)
    {
        var person = cacheProvider.Get("Bjorn");

        Console.WriteLine($"Is Person Null: {person == null}");

        if (person == null)
        {
            person = new Person { Age = 10, Name = "Bjorn" };

            cacheProvider.Add("Bjorn", person);

            Console.WriteLine($"Added Person: {person.Name}");
        }

        person = cacheProvider.Get("Bjorn");

        Console.WriteLine($"And Person Is: {person.Name}");
    }

    using (var container = new IoCBuilder())
    {
        //Calling the method from the main method
        CachingTest(container.Resolve<ICacheProvider<Person>>());
    }
