using VersaTul.Mailer;

var renderer = new MailTemplateRenderer();
var message = renderer.Render("Hello {{Name}}", new Dictionary<string, string> { ["Name"] = "Ada" });
Console.WriteLine(message);
