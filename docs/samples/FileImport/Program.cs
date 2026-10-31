using VersaTul.Data.Bulk;
using VersaTul.Data.FileReader.Readers;
using ReaderOptions = VersaTul.Data.FileReader.FileOptions;

var fixturePath = Path.Combine(AppContext.BaseDirectory, "Fixtures", "people.csv");
using var reader = new CsvFileReader().Read(fixturePath, new ReaderOptions(hasHeader: true));

var mappings = new[]
{
    new BulkCopyColumnMapping("Name", "Name"),
    new BulkCopyColumnMapping("Age", "Age")
};
var copyDetail = new CopyDetail("People", reader, mappings);

var importedNames = new List<string>();
while (reader.Read())
{
    importedNames.Add(reader.GetString(reader.GetOrdinal("Name")));
}

Console.WriteLine($"Prepared {importedNames.Count} import rows for {copyDetail.DestinationName}: {string.Join(", ", importedNames)}");