using System.Net;
using System.Net.Mail;
using System.Net.Sockets;
using System.Text;
using VersaTul.Configurations;
using VersaTul.Mailer;
using VersaTul.Mailer.Configurations;
using VersaTul.Mailer.SmtpClients;

using var listener = new TcpListener(IPAddress.Loopback, 0);
listener.Start();
var port = ((IPEndPoint)listener.LocalEndpoint).Port;
var capturedMessage = new TaskCompletionSource<string>(TaskCreationOptions.RunContinuationsAsynchronously);

var server = Task.Run(async () =>
{
    using var connection = await listener.AcceptTcpClientAsync();
    await using var stream = connection.GetStream();
    using var reader = new StreamReader(stream, Encoding.ASCII, false, 1024, leaveOpen: true);
    await using var writer = new StreamWriter(stream, Encoding.ASCII, 1024, leaveOpen: true)
    {
        NewLine = "\r\n",
        AutoFlush = true
    };

    await writer.WriteLineAsync("220 localhost test SMTP");
    var message = new StringBuilder();
    var readingMessage = false;

    while (await reader.ReadLineAsync() is { } line)
    {
        if (readingMessage)
        {
            if (line == ".")
            {
                readingMessage = false;
                capturedMessage.TrySetResult(message.ToString());
                await writer.WriteLineAsync("250 Message accepted");
            }
            else
            {
                message.AppendLine(line.StartsWith("..", StringComparison.Ordinal) ? line[1..] : line);
            }
        }
        else if (line.StartsWith("EHLO ", StringComparison.OrdinalIgnoreCase) ||
                 line.StartsWith("HELO ", StringComparison.OrdinalIgnoreCase))
        {
            await writer.WriteLineAsync("250 localhost");
        }
        else if (line.StartsWith("MAIL FROM:", StringComparison.OrdinalIgnoreCase) ||
                 line.StartsWith("RCPT TO:", StringComparison.OrdinalIgnoreCase))
        {
            await writer.WriteLineAsync("250 OK");
        }
        else if (line.Equals("DATA", StringComparison.OrdinalIgnoreCase))
        {
            readingMessage = true;
            await writer.WriteLineAsync("354 End data with <CR><LF>.<CR><LF>");
        }
        else if (line.Equals("QUIT", StringComparison.OrdinalIgnoreCase))
        {
            await writer.WriteLineAsync("221 Bye");
            break;
        }
        else
        {
            await writer.WriteLineAsync("250 OK");
        }
    }
});

var configuration = new MailConfiguration(new ConfigSettings
{
    ["SmtpServer"] = "127.0.0.1",
    ["SmtpPort"] = port,
    ["EnableSsl"] = false,
    ["UseDefaultCredentials"] = false,
    ["FromAddress"] = "alerts@example.test",
    ["ToAddress"] = "ops@example.test",
    ["MaxAttachmentSize"] = 1_000_000L,
    ["SmtpTimeoutMilliseconds"] = 5_000,
    ["RetryCount"] = 1
});

using var smtpClient = new SmtpClientWrapper(configuration);
var dispatcher = new MailDispatcher(smtpClient, configuration);
var sent = await dispatcher.SendMailAsync(
    configuration.FromAddress!,
    configuration.ToAddress!,
    "Sample notice",
    "The local SMTP sample is working.");

listener.Stop();
var messageText = await capturedMessage.Task.WaitAsync(TimeSpan.FromSeconds(10));
await server;

if (!sent || !messageText.Contains("Subject: Sample notice", StringComparison.Ordinal))
{
    throw new InvalidOperationException("The SMTP server did not capture the expected message.");
}

Console.WriteLine("SMTP test server accepted the message.");