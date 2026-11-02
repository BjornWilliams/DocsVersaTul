using System.Text;
using VersaTul.Compression;

var zipper = new Zipper(new Archiver());
using var source = new MemoryStream(Encoding.UTF8.GetBytes("Hello from VersaTul"));
using var archive = zipper.Zip(new ZipStream { FileName = "greeting.txt", ContentType = "text/plain", Stream = source });
var extracted = zipper.Unzip(archive).Single();
using var reader = new StreamReader(extracted.Stream!);
Console.WriteLine(await reader.ReadToEndAsync());
