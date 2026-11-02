using VersaTul.Caching;
using VersaTul.Caching.Configurations;
using VersaTul.Configurations;

var cache = new MemCacheProvider<string>(
    new CacheConfiguration(new ConfigSettings { ["CacheDuration"] = 60 }));
var removal = new TaskCompletionSource<bool>(TaskCreationOptions.RunContinuationsAsynchronously);

cache.ItemRemoved += (_, _) => removal.TrySetResult(true);

cache.Add("profile:42", "Ada");
cache.Remove("profile:42");

await removal.Task.WaitAsync(TimeSpan.FromSeconds(5));
Console.WriteLine("Removed profile:42.");
