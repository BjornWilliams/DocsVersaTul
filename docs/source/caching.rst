VersaTul Caching
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
``ICacheProvider<T>`` :Interaction can be achieved through the Cache Provider Interface.
``MemCacheProvider<T>`` :Default Concrete implementation of the Cache Provider interface.
``ICacheConfiguration`` :The Configuration interface for accessing default configurations 
``CacheConfiguration`` :Default Concrete implementation of the configuration interface. 

Code Examples
-------------

.. code-block:: c
    :caption: Simple Example

    
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

.. code-block:: c
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