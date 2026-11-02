using VersaTul.Collection.Streamers;
using VersaTul.Handler.File;
using VersaTul.Object.Converters;
using VersaTul.Utilities;

var wrapper = new DirectoryWrapper();
var files = new FileUtility(wrapper, wrapper);
using var streamer = new CsvStreamer(new CommonUtility(), files, new Flattener());
var people = new[] { new ExamplePerson { Name = "Ada", Age = 37 } };
using var csv = streamer.Create(people, "people").GetFileStream();
using var reader = new StreamReader(csv);
Console.WriteLine(reader.ReadToEnd().Trim());

public sealed class ExamplePerson
{
    public string Name { get; set; } = string.Empty;
    public int Age { get; set; }
}
