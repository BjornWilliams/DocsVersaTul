using VersaTul.Logger;

var entry = new LogInfo(LogLevel.Warning, "Storage", "Disk nearly full");
var json = new LogParser().Parse(entry, ParseFormat.Json);
if (!json.Contains("Disk nearly full", StringComparison.Ordinal))
    throw new InvalidOperationException("The log message was not serialized.");
Console.WriteLine("Serialized: Disk nearly full");
