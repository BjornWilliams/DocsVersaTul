VersaTul Streamers
================

Getting Started
----------------


.. code-block:: antlr-c#
    :caption:
    :options:

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