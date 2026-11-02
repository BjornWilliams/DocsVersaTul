using VersaTul.Data.Sql;

var command = new StoredCommand("dbo.GetCustomer", commandTimeout: 30);
Console.WriteLine($"{command.CommandType}: {command.CommandText}");
