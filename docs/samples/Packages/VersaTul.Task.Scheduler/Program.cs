using VersaTul.Task.Scheduler.Contracts;
using VersaTul.Task.Scheduler.Setters.MethodCalls;

var calls = 0;
var methodCall = new DelegateMethodCall((Func<Task>)(() =>
{
    calls++;
    return Task.CompletedTask;
}));
await ((IAsyncMethodCall)methodCall).ExecuteAsync();
Console.WriteLine($"Executed {calls} async delegate.");
