using VersaTul.Configurations;

var settings = new ConfigSettings
{
    { "ConnectionString", "Server=.;Database=Demo;Trusted_Connection=True;" },
    { "TimeoutSeconds", 30 },
    { "ArchiveDirectory", @"C:\Exports" }
};

var configuration = new StorageConfiguration(settings);

Console.WriteLine($"Connection: {configuration.ConnectionString}");
Console.WriteLine($"Timeout: {configuration.TimeoutSeconds}");
Console.WriteLine($"Archive: {configuration.ArchivePath}");

public sealed class StorageConfiguration(ConfigSettings settings) : Configuration(settings)
{
    public string ConnectionString => Get<string>() ?? throw new InvalidOperationException("ConnectionString is missing.");

    public int TimeoutSeconds => GetOrDefault<int>();

    public string ArchivePath => Get<string>("ArchiveDirectory") ?? throw new InvalidOperationException("ArchiveDirectory is missing.");
}
