using VersaTul.Caching;
using VersaTul.Caching.Configurations;
using VersaTul.Caching.Contracts;
using VersaTul.Configurations;

using var cache = new MemCacheProvider<string>(
    new CacheConfiguration(new ConfigSettings { ["CacheDuration"] = 60 }));
ICacheProviderWithEvents<string> eventingCache = cache;
var removal = new TaskCompletionSource<string>(TaskCreationOptions.RunContinuationsAsynchronously);

eventingCache.ItemRemovedDetailed += (_, args) =>
    removal.TrySetResult($"{args.Key}: {args.Reason}");

eventingCache.Add("profile:42", "Ada");
eventingCache.Remove("profile:42");

var removed = await removal.Task.WaitAsync(TimeSpan.FromSeconds(5));
Console.WriteLine($"Removed {removed}.");