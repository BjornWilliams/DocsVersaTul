Caching
=======

.. _installation:

Installation
------------

To use Caching, first install it using nuget:

.. code-block:: console

   (.venv) PM> NuGet\Install-Package VersaTul.Caching -Version latest

Getting Started
----------------
The VersaTul Caching project is designed to provide a simple caching interface with the ability to change the underlining cache engine. 
The default cache engine is built on top of the Microsoft Extensions Caching Memory which provides in memory caching. 
The VersaTul Caching project also provides the ability to easily replace the underline caching engine using easily implemented interfaces.

Basic Information about VersaTul Caching
-----------------------------------------

Interaction can be achieved through the Cache Provider Interface: ``ICacheProvider<T>``
The Concrete class for the Cache Provider is ``MemCacheProvider<T>``
The Configuration interface for the cache provider is ``ICacheConfiguration``
The Concrete class for the configuration is ``CacheConfiguration``


Simple Examples
----------------

.. code-block:: console
    
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


Using With a IoC Container
--------------------------

.. code-block:: console

//Creating the IoC container
var builder = new ContainerBuilder();

//Populating the container

//default configs
var configSettings = new Builder().BuildConfig();

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

