using VersaTul.Configurations;

var settings = new ConfigSettings { ["Name"] = "Ada", ["Age"] = 37 };
var configuration = new PersonConfiguration(settings);
Console.WriteLine($"{configuration.Name}, {configuration.Age}");

sealed class PersonConfiguration(ConfigSettings settings) : Configuration(settings)
{
    public string Name => Get<string>() ?? string.Empty;
    public int Age => Get<int>();
}
