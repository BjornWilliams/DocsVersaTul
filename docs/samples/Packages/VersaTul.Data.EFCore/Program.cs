using VersaTul.Configurations;
using VersaTul.Data.EFCore.Configurations;

var settings = new ConfigSettings
{
    ["EfDbConnectionName"] = "Reporting",
    ["Reporting"] = "Server=(localdb)\\mssqllocaldb;Database=Reports;Trusted_Connection=True;"
};
var connection = new DataConfiguration(settings).GetConnectionString();
Console.WriteLine(connection);
