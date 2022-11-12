VersaTul Caching
================

Getting Started
----------------

.. _installation:

Installation
------------

To use VersaTul Caching, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Caching -Version latest

Basic Information about VersaTul Caching
-----------------------------------------

The VersaTul Caching project is designed to provide a simplfied caching interface with the ability to change the underlining caching engine easily and quickly. 
The default cache engine is built on top of the Microsoft Extensions Caching Memory class, which provides an in memory caching store. 
This implementation can be easily replaced using the interface provided.

Components
-----------
Interaction can be achieved through the Cache Provider Interface: ``ICacheProvider<T>``
The Concrete class for the Cache Provider is ``MemCacheProvider<T>``
The Configuration interface for the cache provider is ``ICacheConfiguration``
The Concrete class for the configuration is ``CacheConfiguration``


Simple Example
----------------

.. code-block::c
    class Program
    {
        static void Main(string[] args)
        {
            //default configs
            var configSettings = new Builder().BuildConfig();
            
            var cacheProvider = new MemCacheProvider<Person>(new CacheConfiguration(configSettings));
            
            person = new Person { Age = 10, Name = "Bjorn" };

            cacheProvider.Add("Bjorn", person);

            var person = cacheProvider.Get("Bjorn");

        }

        Console.ReadLine();
    }


Use With a IoC Container
--------------------------

.. code-block:: c
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
