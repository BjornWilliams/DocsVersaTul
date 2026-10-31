using VersaTul.Pipeline.Infrastructure;

var total = new DoublePipeline().Execute(21);
Console.WriteLine(total);

sealed class DoublePipeline : Pipeline<int, int>
{
    public DoublePipeline() => Step = value => value * 2;
}
