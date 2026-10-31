using Microsoft.Data.Sqlite;
using System.Data.Common;
using VersaTul.Configurations;
using VersaTul.Data.Sql;
using VersaTul.Data.Sql.Configurations;

DbProviderFactories.RegisterFactory("Microsoft.Data.Sqlite", SqliteFactory.Instance);

const string connectionString = "Data Source=versatul-docs-sql;Mode=Memory;Cache=Shared";
await using var keepAlive = new SqliteConnection(connectionString);
await keepAlive.OpenAsync();

var settings = new ConfigSettings
{
    ["SqlDbConnectionName"] = "Example",
    ["CommandTimeout"] = 30,
    ["Example"] = new
    {
        ConnectionString = connectionString,
        ProviderName = "Microsoft.Data.Sqlite"
    }
};

var configuration = new DataConfiguration(settings);
var commands = new CommandFactory(configuration, new ProviderFactory());
var dataSource = new SqlDbDataSource(commands);

dataSource.Write(new DataCommand(
    "CREATE TABLE people (name TEXT NOT NULL);",
    DataCommandType.Query));
var inserted = dataSource.Write(new DataCommand(
    "INSERT INTO people (name) VALUES ('Ada');",
    DataCommandType.Query));
var name = dataSource.ExecuteScalar<string>(
    new DataCommand("SELECT name FROM people LIMIT 1;", DataCommandType.Query));

if (inserted != 1 || name != "Ada")
{
    throw new InvalidOperationException("The SQLite round trip returned an unexpected result.");
}

Console.WriteLine($"Saved {inserted} row; read back {name}.");
