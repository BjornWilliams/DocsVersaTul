using System.Text.Json;
using System.Text.Json.Serialization;
using VersaTul.Collection.Streamers;
using VersaTul.Handler.File;
using VersaTul.Object.Converters;
using VersaTul.Utilities;

var outputDirectory = Path.Combine(Path.GetTempPath(), $"versatul-docs-export-{Guid.NewGuid():N}");
Directory.CreateDirectory(outputDirectory);

try
{
    var people = new[]
    {
        new Person { Name = "Ada", Age = 37 }
    };

    var wrapper = new DirectoryWrapper();
    var files = new FileUtility(wrapper, wrapper);
    using var streamer = new CsvStreamer(new CommonUtility(), files, new Flattener());
    using var csvStream = streamer.Create(people, "people").GetFileStream();
    using var csvReader = new StreamReader(csvStream);
    var csv = await csvReader.ReadToEndAsync();

    var json = JsonSerializer.Serialize(
        people,
        new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase });

    var csvPath = Path.Combine(outputDirectory, "people.csv");
    var jsonPath = Path.Combine(outputDirectory, "people.json");
    await File.WriteAllTextAsync(csvPath, csv);
    await File.WriteAllTextAsync(jsonPath, json);

    var savedCsv = (await File.ReadAllTextAsync(csvPath)).TrimEnd();
    var savedJson = await File.ReadAllTextAsync(jsonPath);
    if (!savedCsv.Contains("Ada", StringComparison.Ordinal) ||
        !savedJson.Contains("\"name\":\"Ada\"", StringComparison.Ordinal))
    {
        throw new InvalidOperationException("The export files did not contain the expected person.");
    }

    Console.WriteLine("people.csv:");
    Console.WriteLine(savedCsv);
    Console.WriteLine("people.json:");
    Console.WriteLine(savedJson);
}
finally
{
    Directory.Delete(outputDirectory, recursive: true);
}

public sealed class Person
{
    public string Name { get; init; } = string.Empty;
    public int Age { get; init; }
}