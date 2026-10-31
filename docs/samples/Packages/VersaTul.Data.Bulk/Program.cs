using VersaTul.Data.Bulk;

var mapping = new BulkCopyColumnMapping("Name", "CustomerName");
var copy = new CopyDetail("Customers", reader: null, new[] { mapping });
Console.WriteLine($"{copy.DestinationName}: {mapping.SourceColumn} -> {mapping.DestinationColumn}");
