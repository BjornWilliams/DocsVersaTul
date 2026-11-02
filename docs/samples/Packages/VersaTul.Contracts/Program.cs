using System.Linq.Expressions;
using VersaTul.Contracts;

var predicate = new MinimumLengthPredicate(4);
Console.WriteLine(predicate.Condition.Compile()("VersaTul"));

sealed class MinimumLengthPredicate(int minimumLength) : IPredicate<string>
{
    public Expression<Func<string, bool>> Condition { get; set; } = value => value.Length >= minimumLength;
}
