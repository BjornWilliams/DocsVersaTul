using System.Net.Mail;
using VersaTul.Configurations;
using VersaTul.Logger;
using VersaTul.Logger.Mail;
using VersaTul.Mailer.Contracts;
using VersaTul.Mailer.Configurations;

var configuration = new MailConfiguration(new ConfigSettings
{
    ["FromAddress"] = "alerts@example.test",
    ["ToAddress"] = "ops@example.test"
});
var dispatcher = new RecordingDispatcher();
await using (var logger = new MailLogger(dispatcher, configuration, new LogParser()))
{
    await logger.LogAsync(new LogInfo(LogLevel.Error, "Payments", "Gateway timeout"));
    await logger.FlushAsync();
}
if (!dispatcher.LastBody.Contains("Gateway timeout", StringComparison.Ordinal))
    throw new InvalidOperationException("The log event was not delivered to the dispatcher.");
Console.WriteLine("Delivered one log event to the injected dispatcher.");

sealed class RecordingDispatcher : IMailDispatcher
{
    public string LastBody { get; private set; } = string.Empty;
    public bool SendMail(string fromAddress, string toAddress, string? subject, string? body) => Save(body);
    public bool SendMail(string fromAddress, string toAddress, string? subject, string? body, bool isHtml) => Save(body);
    public bool SendMail(string fromAddress, string toAddress, string? subject, string? body, bool isHtml, IEnumerable<Attachment>? attachments) => Save(body);
    public bool SendMail(string fromAddress, string toAddress, string? subject, string? body, bool isHtml, IEnumerable<IMailAttachment>? attachments) => Save(body);
    public bool SendTemplatedMail(string fromAddress, string toAddress, string? subject, string template, IDictionary<string, string> tokens, bool isHtml = true) => Save(template);
    private bool Save(string? body) { LastBody = body ?? string.Empty; return true; }
}
