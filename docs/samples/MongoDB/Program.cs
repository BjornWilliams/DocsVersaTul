using MongoDB.Bson;
using MongoDB.Bson.Serialization;
using VersaTul.Data.MongoDB;

var map = new CarMap();
var car = new Car
{
    Id = ObjectId.GenerateNewId().ToString(),
    Make = "Volvo",
    Model = "EX30",
    Year = 2026
};
var document = car.ToBsonDocument();

if (!document.Contains("make"))
{
    throw new InvalidOperationException("The car map did not apply the expected element name.");
}

Console.WriteLine($"Mapped collection: {map.CollectionName}; make field: {document.Contains("make")}");

public sealed class Car : Entity
{
    public string Make { get; set; } = string.Empty;
    public string Model { get; set; } = string.Empty;
    public int Year { get; set; }
    public BsonDocument ExtraElements { get; set; } = new();
}

public sealed class CarMap : BaseMap<Car>
{
    public CarMap() : base("cars", car => car.ExtraElements)
    {
    }

    public override void Register(BsonClassMap<Car> classMap)
    {
        base.Register(classMap);
        classMap.MapMember(car => car.Make).SetElementName("make");
        classMap.MapMember(car => car.Model).SetElementName("model");
        classMap.MapMember(car => car.Year).SetElementName("year");
    }
}
