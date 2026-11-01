using System.Globalization;
using System.Text.Json;
using System.Text.Json.Serialization;
using VersaTul.Collection.Streamers;
using VersaTul.Display.Attributes;
using VersaTul.Handler.File;
using VersaTul.Object.Converters;
using VersaTul.Utilities;

CultureInfo.CurrentCulture = CultureInfo.InvariantCulture;

var outputDirectory = Path.Combine(Path.GetTempPath(), $"versatul-docs-export-{Guid.NewGuid():N}");
Directory.CreateDirectory(outputDirectory);

try
{
    var people = new[]
    {
        new Person
        {
            Name = "Ada",
            CreditLimit = 1250.456m,
            Age = 37,
            RegisteredOn = new DateTime(2024, 1, 15),
            Location = new Location { City = "London" },
            InternalNotes = "Do not include in either export"
        }
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
    var expectedCsv = string.Join(
        Environment.NewLine,
        "Full name,Credit limit,Age,Registered,Location",
        "Ada,1250.46,37,2024-01-15,City:London");
    const string expectedJson = "[{\"name\":\"Ada\",\"creditLimit\":1250.456,\"age\":37,\"registeredOn\":\"2024-01-15T00:00:00\",\"location\":{\"city\":\"London\"}}]";
    if (!string.Equals(savedCsv, expectedCsv, StringComparison.Ordinal) ||
        !string.Equals(savedJson, expectedJson, StringComparison.Ordinal))
    {
        throw new InvalidOperationException("The export files did not match the expected CSV and JSON content.");
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
    [Display(Name = "Full name", Sequence = 1)]
    public string Name { get; init; } = string.Empty;

    [Display(Name = "Credit limit", Decimals = 2, Sequence = 2)]
    public decimal CreditLimit { get; init; }

    [Display(Name = "Age", Sequence = 3)]
    public int Age { get; init; }

    [Display(Name = "Registered", DateFormattingString = "yyyy-MM-dd", Sequence = 4)]
    public DateTime RegisteredOn { get; init; }

    [Display(Name = "Location", Sequence = 5)]
    public Location Location { get; init; } = new();

    [Display(Ignore = true)]
    [JsonIgnore]
    public string InternalNotes { get; init; } = string.Empty;
}

public sealed class Location
{
    public string City { get; init; } = string.Empty;
}
