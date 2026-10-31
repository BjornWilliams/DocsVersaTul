using VersaTul.Configurations;
using VersaTul.Handler.File;
using VersaTul.Logger;
using VersaTul.Logger.File;
using VersaTul.Logger.File.Configurations;
using VersaTul.Utilities;

var directory = Path.Combine(Path.GetTempPath(), $"versatul-docs-log-{Guid.NewGuid():N}");
Directory.CreateDirectory(directory);

try
{
    var settings = new ConfigSettings
    {
        ["FilePath"] = directory,
        ["LogFileName"] = "app.log",
        ["MaxFileSize"] = 1_000_000L
    };
    var configuration = new LogFileConfiguration(settings, new CommonUtility());
    var wrapper = new DirectoryWrapper();
    var files = new FileUtility(wrapper, wrapper);
    var logger = new FileLogger(configuration, new Archiver(configuration, files), new LogParser(), files);

    await logger.LogAsync(new LogInfo(LogLevel.Information, "Startup", "Application started"));

    var logLines = await File.ReadAllLinesAsync(configuration.FullLogFileName);
    if (logLines.Length != 1 ||
        !logLines[0].Contains("LogLevel\tInformation", StringComparison.Ordinal) ||
        !logLines[0].Contains("CategoryName\tStartup", StringComparison.Ordinal) ||
        !logLines[0].Contains("LogMessage\tApplication started", StringComparison.Ordinal))
    {
        throw new InvalidOperationException("The file did not contain exactly the expected log record.");
    }

    Console.WriteLine("Wrote one log record.");
}
finally
{
    Directory.Delete(directory, recursive: true);
}
