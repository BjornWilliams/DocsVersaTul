using VersaTul.Handler.File;

var root = Path.Combine(Path.GetTempPath(), $"versatul-files-{Guid.NewGuid():N}");
Directory.CreateDirectory(root);
var path = Path.Combine(root, "daily-report.csv");
File.WriteAllLines(path, ["Name,Status", "Import,complete"]);
var wrapper = new DirectoryWrapper();
var files = new FileUtility(wrapper, wrapper);
try
{
    var result = files.ReadAll(path);
    Console.WriteLine(string.Join(Environment.NewLine, result.Content ?? Array.Empty<string>()));
}
finally
{
    Directory.Delete(root, recursive: true);
}
