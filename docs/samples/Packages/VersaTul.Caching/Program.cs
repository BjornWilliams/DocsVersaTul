using VersaTul.Caching;
using VersaTul.Caching.Configurations;
using VersaTul.Configurations;

using var cache = new MemCacheProvider<string>(new CacheConfiguration(new ConfigSettings
{
    ["CacheDuration"] = 60
}));
cache.Add("greeting", "Hello from VersaTul");
Console.WriteLine(cache.Get("greeting"));
