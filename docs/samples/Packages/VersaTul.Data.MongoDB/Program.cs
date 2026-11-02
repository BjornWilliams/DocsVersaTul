using VersaTul.Data.MongoDB;

var car = new Car { Id = "roadster-1", Make = "VersaTul", Model = "Roadster", Year = 2026 };
Console.WriteLine($"{car.Make} {car.Model} ({car.Year})");

sealed class Car : Entity
{
    public string Make { get; set; } = string.Empty;
    public string Model { get; set; } = string.Empty;
    public int Year { get; set; }
}
