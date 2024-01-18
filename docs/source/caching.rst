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
#. ``ICacheProvider<T>`` : Adding and retrieving items from the cache can be achieved using this interface.
#. ``MemCacheProvider<T>`` : This is a default concrete implementation of the Cache Provider interface. This can be replaced with another provider if so desired.
#. ``ICacheConfiguration`` : The cache configuration interface for accessing configuration settings. See :doc:`configuration-defaults` for more details on configuration settings.
#. ``CacheConfiguration`` : This is the default concrete implementation of the cache configuration interface. 

Functional Summary
------------------
#. **T ICacheProvider<T>.Get(string key)** : Retrieves the cache entry for the given key. If the cache entry is not found then the default of T is returned.
#. **void ICacheProvider<T>.Add()** : Overloaded method for inserting the cache entry using the key for a the specified duration.
#. **bool ICacheProvider<T>.IsExists(string key)** : Indicates if there is a cache entry for the key.
#. **void ICacheProvider<T>.Remove(string key)** : Removes the cache entry from the cache for the given key.

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
    :caption: Simple Example With (AutoFac) as the IoC Container
        
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

    // static method where cache provider can be injected by autofac.
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



Changelog
-------------

V1.0.13

* Add Memory Cache Option support
* Minor fixes

V1.0.12

* Minor fixes

V1.0.11

* Minor fixes

V1.0.10

* Interface improvements 

V1.0.9

* Code ported to dotnet core
* Documentaion completed