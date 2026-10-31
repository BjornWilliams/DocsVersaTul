using VersaTul.Extensions;

var name = "Ada".ToCamelCase();
var quantity = "42".To<int>();
Console.WriteLine($"{name}: {quantity}");
