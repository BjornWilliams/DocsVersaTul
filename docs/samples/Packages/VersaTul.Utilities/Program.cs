using VersaTul.Utilities;

var batches = new CollectionUtility<int>().MakeBatches(Enumerable.Range(1, 7), batchSize: 3);
Console.WriteLine(string.Join(" | ", batches.Select(batch => string.Join(",", batch))));
