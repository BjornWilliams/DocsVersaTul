using System.Data;
using VersaTul.Data.MsSql;

var parameter = new SqlParameter("@customerId", 42, SqlDbType.Int, 0, ParameterDirection.Input);
Console.WriteLine($"Prepared {parameter.Type} parameter for @customerId.");
