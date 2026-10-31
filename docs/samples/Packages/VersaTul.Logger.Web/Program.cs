using System.Net;
using Microsoft.Extensions.Http;
using VersaTul.Configurations;
using VersaTul.Logger;
using VersaTul.Logger.Web;
using VersaTul.Logger.Web.Configurations;

using var factory = new SuccessfulHttpClientFactory();
var configuration = new LogWebConfiguration(new ConfigSettings
{
    ["BaseUrl"] = "https://logs.example.test/api",
    ["LogEndPoint"] = "/events"
});
var logger = new WebLogger(factory, configuration, new LogParser());
await logger.LogAsync(new LogInfo(LogLevel.Information, "Startup", "Service ready"));
Console.WriteLine($"Requests sent: {factory.RequestCount}");

sealed class SuccessfulHttpClientFactory : IHttpClientFactory, IDisposable
{
    private readonly SuccessfulHandler handler;

    public SuccessfulHttpClientFactory() => handler = new SuccessfulHandler(() => RequestCount++);

    public int RequestCount { get; private set; }
    public HttpClient CreateClient(string name) => new(handler, disposeHandler: false);

    public void Dispose() => handler.Dispose();
}

sealed class SuccessfulHandler(Action onRequest) : HttpMessageHandler
{
    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        onRequest();
        return Task.FromResult(new HttpResponseMessage(HttpStatusCode.OK));
    }
}
