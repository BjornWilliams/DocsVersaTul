using System.Collections.Generic;
using VersaTul.Object.Converters;

var person = new { Name = "Ada", Address = new { City = "London" } };
var values = new ObjectProcessor().ToDictionary(person);
var address = values["Address"] as IDictionary<string, object?>
    ?? throw new InvalidOperationException("Address was not converted to a dictionary.");
Console.WriteLine(address["City"] ?? throw new InvalidOperationException("City was not converted."));
