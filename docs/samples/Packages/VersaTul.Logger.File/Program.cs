using VersaTul.Configurations;
using VersaTul.Handler.File;
using VersaTul.Logger;
using VersaTul.Logger.File;
using VersaTul.Logger.File.Configurations;
using VersaTul.Utilities;

var directory = Path.Combine(Path.GetTempPath(), $"versatul-log-{Guid.NewGuid():N}");
var settings = new ConfigSettings
{
    ["FilePath"] = directory,
    ["LogFileName"] = "app.log",
    ["MaxFileSize"] = 1_000_000L
};
var config = new LogFileConfiguration(settings, new CommonUtility());
var wrapper = new DirectoryWrapper();
var files = new FileUtility(wrapper, wrapper);
var logger = new FileLogger(config, new Archiver(config, files), new LogParser(), files);
await logger.LogAsync(new LogInfo(LogLevel.Information, "Startup", "Application started"));
if (!File.ReadAllText(config.FullLogFileName).Contains("Application started", StringComparison.Ordinal))
    throw new InvalidOperationException("The log record was not written.");
Console.WriteLine("Wrote one log record.");
Directory.Delete(directory, recursive: true);
