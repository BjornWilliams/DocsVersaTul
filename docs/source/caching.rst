Caching
================

Getting Started
----------------
The VersaTul Caching project is designed to provide a simplified caching interface with the ability to change the underlining caching engine easily and quickly. 
The default cache engine is built on top of the Microsoft Extensions Caching Memory class, which provides an in memory caching store. 
This implementation can be easily replaced using the interface provided.

Installation
------------

To use VersaTul Caching, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Caching -Version latest


Main Components
----------------
#. ``ICacheProvider<T>`` : Adding and getting items from the cache can be achieved through the Cache Provider Interface.
#. ``MemCacheProvider<T>`` : This is a default concrete implementation of the Cache Provider interface. This can be replaced with another provider if so desires.
#. ``ICacheConfiguration`` : The Configuration interface for accessing default configurations.
#. ``CacheConfiguration`` : Default Concrete implementation of the configuration interface. 

Functional Summary
------------------
#. **ICacheProvider<T>.Get(string key)** : Retrieves the cache entry for the given key. If the cache entry is not found then the default of T is returned.
#. **ICacheProvider<T>.Add(string key, T data)** : Inserts the cache entry using the key for a default duration of 60 minutes.
#. **ICacheProvider<T>.Add(string key, T data, int cacheTime)** : Inserts the given item into the Cache using the given key for a the specified duration in minutes.
#. **ICacheProvider<T>.Add(string key, T data, CacheExpiration expiration)** : Inserts the given item into the Cache using the given key for the specified CacheExpiration.
#. **ICacheProvider<T>.IsExists(string key)** : Indicates if there is a cache entry for the key.
#. **ICacheProvider<T>.Remove(string key)** : Removes the cache entry from the cache for the given key.
#. See :doc:`configuration-defaults` for more configuration settings details for the caching project.

Code Examples
-------------

.. code-block:: c#
    :caption: Simple Example
    
    class Program
    {
        static void Main(string[] args)
        {
            // default configs - see configuration default for more details.
            var configSettings = new Builder().BuildConfig();
            
            // cache configuration
            var cacheConfiguration = new CacheConfiguration(configSettings);

            ICacheProvider<Person> cacheProvider = new MemCacheProvider<Person>(cacheConfiguration);

            person = new Person { Age = 10, Name = "Bjorn" };

            cacheProvider.Add("Bjorn", person);

            var person = cacheProvider.Get("Bjorn");
        }
        Console.ReadLine();
    }

.. code-block:: c#
    :caption: Simple Example With a (AutoFac) as the IoC Container
        
    // creating the IoC container
    var builder = new ContainerBuilder();

    // default configs - see configuration default for more details.
    var configSettings = new Builder().BuildConfig();

    // Populating the container
    builder.RegisterInstance(configSettings);

    builder
        .RegisterType<CacheConfiguration>()
        .As<ICacheConfiguration>()
        .SingleInstance();

    builder
        .RegisterGeneric(typeof(MemCacheProvider<>))
        .As(typeof(ICacheProvider<>))
        .SingleInstance();

    // static method where cache provider can be injected by autofac...
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

    // main
    using (var container = new IoCBuilder())
    {
        // calling the method from the main method
        CachingTest(container.Resolve<ICacheProvider<Person>>());
    }
