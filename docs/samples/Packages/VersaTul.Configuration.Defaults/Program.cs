using VersaTul.Configuration.Defaults.MongoDB;

var settings = new Builder()
    .AddOrReplace("ConnectionString", "mongodb://localhost:27017")
    .AddOrReplace("DatabaseName", "catalog")
    .BuildConfig();
Console.WriteLine(settings["DatabaseName"]);
