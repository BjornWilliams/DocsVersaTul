using VersaTul.Display.Attributes;

var property = typeof(Product).GetProperty(nameof(Product.Price))!;
var analyzer = new DisplayAnalyzer();
Console.WriteLine($"{analyzer.GetName(property)}: {analyzer.FormatPropertyValue(property, 19.999m)}");

sealed class Product
{
    [Display(Name = "Unit price", Decimals = 2)]
    public decimal Price { get; set; }
}
