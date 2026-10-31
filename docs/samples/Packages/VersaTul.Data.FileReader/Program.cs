using VersaTul.Data.FileReader.Readers;
using ReaderOptions = VersaTul.Data.FileReader.FileOptions;

var path = Path.Combine(Path.GetTempPath(), $"versatul-{Guid.NewGuid():N}.csv");
await File.WriteAllTextAsync(path, "Id,Name\n1,Ada\n");
try
{
    using var reader = new CsvFileReader().Read(path, new ReaderOptions(hasHeader: true));
    if (!reader.Read()) throw new InvalidOperationException("The CSV row was not read.");
    Console.WriteLine(reader.GetString(1));
}
finally
{
    File.Delete(path);
}
