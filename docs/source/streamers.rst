Collection Streamers
====================

Getting Started
----------------
The VersaTul Collection Streamers provides functionality that enables developers to quickly convert a collection of objects in memory into a data-reader that can be used for Bulk inserting data into a SQL Database, or be used to generate flat files.
Developers can use the streamers to:

#. Convert a Collection to a Data-Reader.
#. Convert from a Data-Reader to other file formats such as CSV, TAB or Json.
#. Compress converted data into Zip files.
#. Transport the converted data via e-mail.

The Streamers project also works with :doc:`display-attributes` which is used to manipulate the properties on the objects in the collection such as formatting the data or renaming the property with a desired display name.

Installation
------------

To use VersaTul Collection Streamers, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Collection.Streamers -Version latest

Main Components
----------------
#. ``IStreamer`` : A base interface that represents the data contained in the stream and the functionality that can be applied to the data.
#. ``IStreamCreator`` : A base interface that represents the functionality for creating streamers.
#. ``ICsvStreamer`` : A specific stream type interface that represents the functionality for creating csv streamers.
#. ``ITabStreamer`` : A specific stream type interface that represents the functionality for creating tab streamers.
#. ``IJsonStreamer`` : A specific stream type interface that represents the functionality for creating json streamers.
#. ``BaseStreamer`` : A concrete implementation of the IStreamer and IStreamCreator interfaces. Providing common functionality for all streamers.
#. ``CsvStreamer`` : A concrete implementation of the ICsvStreamer interface.
#. ``JsonStreamer`` : A concrete implementation of the IJsonStreamer interface.
#. ``TabStreamer`` : A concrete implementation of the ITabStreamer interface.
#. ``IMailTransporter`` : Represents a set of functionality to send streamers via email attachments.
#. ``IStreamFileConverter`` : Represent a set of conversion techniques that can be applied to a Streamer.
#. ``ICompressTransport`` : Represents a set of functionality to reduce streamers for transport over the network.
#. ``CollectionReaderExtensions`` : Contains the ToReader method that can be used to convert any collection to an IDataReader.

Functional Summary
------------------
#. **MemoryStream IStreamer.GetFileStream()** : Returns the file data as a stream whose backing store is MemoryStream.
#. **IStreamer IStreamCreator.Create<T>(IEnumerable<T> source, string fileName)** : Creates a Memory Stream from the given collection.
#. **bool IMailTransporter.Transport()** : Overloaded method for transferring a given IStreamer or list of IStreamers via email to given recipient.
#. **void IStreamFileConverter.Save(IStreamer streamer, string filePath, bool compressed = false)** : Convert the given IStreamer to a physical file on disc at the given path.
#. **IEnumerable<Attachment> ICompressTransport.GetAttachments(long maxAttachmentSize, StreamContainer streamContainer)** : Creates a list of Attachment from the given StreamContainer instance.
#. **CollectionReader<T> CollectionReaderExtensions.ToReader<T>(this IEnumerable<T> collection)** : Convert the given collection into a CollectionReader of T or an IDataReader.

Code Examples
-------------

.. code-block:: c#
    :caption: Simple Example of CsvStreamer.

    using VersaTul.Collection.Streamers;
    using VersaTul.Collection.Streamers.Compressions;
    using VersaTul.Collection.Streamers.Converters;
    using VersaTul.Compression;
    using VersaTul.Handler.File;
    using VersaTul.Object.Converters;
    using VersaTul.Utilities;

    namespace CollectionStreamers
    {
        class Program
        {
            static void Main(string[] args)
            {
                // Create N number of data model
                var people = GetPeople(1000);

                // Create Needed Instances
                var directoryWrapper = new DirectoryWrapper();
                var utility = new CommonUtility();
                var flattener = new Flattener();
                var zipper = new Zipper(new Archiver());
                var compressor = new Compressor(zipper);
                var fileUtil = new FileUtility(directoryWrapper, directoryWrapper);
                var fileConvert = new FileConverter(fileUtil, compressor);

                // Creating the CsvStreamer Instance
                var csvStreamer = new CsvStreamer(utility, fileUtil, flattener);

                // Create CSV from given people collection
                var csv = csvStreamer.Create(people, "people");

                // Save csv to Path
                fileConvert.Save(csv, "C:\\your\\file\\path\\here\\", false);
            }

            // Helper method for generating list of data model.
            private static IEnumerable<Person> GetPeople(int amount)
            {
                var people = new List<Person>(amount);
                var names = new[]
                {
                    "John Doe",
                    "Jane Smith",
                    "Susan Williams",
                    "Mike Burger",
                    "Joe Williams",
                    "Timmy Smith",
                    "Lisa Ray",
                    "Stanley Smith",
                    "Sam Jones",
                };

                for (int i = 0; i < amount; i++)
                {
                    people.Add(new Person
                    {
                        Age = i + 10,
                        Name = CommonUtil.RandomSampler(names),
                        AccountBalance = (100.99m * i),
                        BestFriend = CommonUtil.RandomSampler(people)
                    });
                }

                return people;
            }
        }

        // Data Model
        public class Person
        {
            public int Age { get; set; }
            public string? Name { get; set; }
            public decimal AccountBalance { get; set; }
            public IEnumerable<Person>? Friends { get; set; }
            public Person? BestFriend { get; set; }
        }

        // Helper class
        public static class CommonUtil
        {
            public static T? RandomSampler<T>(IList<T> source)
            {
                var max = source.Count;

                if (max == 0)
                    return default;

                var rand = new Random();
                var position = rand.Next(max);

                return source[position];
            }
        }
    }


.. code-block:: c#
    :caption: IoC Example of CsvStreamer.
    
    namespace CollectionStreamers
    {
        // AutoFac Module
        public class AppModule : Module
        {
            protected override void Load(ContainerBuilder builder)
            {
                // Configs
                
                // VersaTul.Configuration.Defaults.Mailer
                var configSettings = new Builder().AddOrReplace(new[]
                {
                    new KeyValuePair<string,object>("FromAddress", "author@versatul.com"),
                    new KeyValuePair<string,object>("ToAddress", "joesmith@domain.com"),
                    new KeyValuePair<string,object>("SmtpServer", "127.0.0.1"),
                    new KeyValuePair<string,object>("SmtpPort", 25)
                }).BuildConfig();

                builder.RegisterInstance(configSettings);

                // Singletons

                // VersaTul.Handler.File
                builder.RegisterType<DirectoryWrapper>().As<IDirectoryWrapper>().As<IFileWrapper>().SingleInstance();
                builder.RegisterType<FileUtility>().As<IFileUtility>().As<IFileHandler>().SingleInstance();

                // VersaTul.Compression
                builder.RegisterType<Compressor>().As<ICompressor>().SingleInstance();
                builder.RegisterType<Zipper>().As<IZipper>().SingleInstance();
                builder.RegisterType<Archiver>().As<IArchiver>().SingleInstance();

                // VersaTul.Utilities
                builder.RegisterType<CommonUtility>().As<IUtility>().SingleInstance();

                // VersaTul.Object.Converters
                builder.RegisterType<Flattener>().As<IFlattener>().SingleInstance();

                // VersaTul.Mailer
                builder.RegisterType<MailConfiguration>().As<IMailConfiguration>().SingleInstance();
                builder.RegisterType<SmtpClientWrapper>().As<ISmtpClient>().SingleInstance();

                // VersaTul.Collection.Streamers
                builder.RegisterType<CompressTransport>().As<ICompressTransport>().SingleInstance();

                // Per Dependency

                // VersaTul.Collection.Streamers
                builder.RegisterType<FileConverter>().As<IStreamFileConverter>().InstancePerDependency();
                builder.RegisterType<CsvStreamer>().As<ICsvStreamer>().InstancePerDependency();
                builder.RegisterType<TabStreamer>().As<ITabStreamer>().InstancePerDependency();
                builder.RegisterType<JsonStreamer>().As<IJsonStreamer>().InstancePerDependency();
                builder.RegisterType<MailTransporter>().As<IMailTransporter>().InstancePerDependency();

                // VersaTul.Mailer
                builder.RegisterType<MailDispatcher>().As<IMailDispatcher>().InstancePerDependency();
            }
        }

        public class CollectionConverter
        {
            // injecting container for simplicity
            public void Execute(AppContainer appContainer, string type, string output, string compressed)
            {
                // generate list of person to convert. 
                var people = GetPeople(1000);

                IStreamer? streamer = null;
                IStreamCreator streamCreator;

                switch (type)
                {
                    case "csv":
                        streamCreator = appContainer.Resolve<ICsvStreamer>();
                        streamer = streamCreator.Create(people, "people");
                        break;
                    case "tab":
                        streamCreator = appContainer.Resolve<ITabStreamer>();
                        streamer = streamCreator.Create(people, "people");
                        break;
                    case "json":
                        streamCreator = appContainer.Resolve<IJsonStreamer>();
                        streamer = streamCreator.Create(people, "people");
                        break;
                }

                switch (output)
                {
                    case "file":
                        OutputToFile(streamer, appContainer, "filePath\\here", compressed == "yes");
                        break;
                    case "screen":
                        OutputToScreen(streamer);
                        break;
                    case "email":
                        OutputToEmail(streamer, appContainer);
                        break;
                }

                streamer.Dispose();
            }

            // send file via email. 
            private static void OutputToEmail(IStreamer streamer, AppContainer appContainer)
            {
                var mailTransporter = appContainer.Resolve<IMailTransporter>();
                var mailConfiguration = appContainer.Resolve<IMailConfiguration>();

                mailTransporter.Transport(
                    mailConfiguration.FromAddress,
                    mailConfiguration.ToAddress,
                    "Stream Test Email Sent",
                    "Please see attached files.",
                    streamer);
            }

            // send file to console.
            private static void OutputToScreen(IStreamer streamer)
            {
                StreamReader streamReader = new(streamer.GetFileStream());

                string streamAsString = streamReader.ReadToEnd();

                Console.WriteLine(streamAsString);
            }

            // send file to disc.
            private static void OutputToFile(IStreamer streamer, AppContainer appContainer, string filePath, bool compressed)
            {
                IStreamFileConverter fileConverter = appContainer.Resolve<IStreamFileConverter>();

                fileConverter.Save(streamer, filePath, compressed);
            }

            // Helper method for generating list of data model.
            private static IEnumerable<Person> GetPeople(int amount)
            {
                var people = new List<Person>(amount);
                var names = new[]
                {
                    "John Doe",
                    "Jane Smith",
                    "Susan Williams",
                    "Mike Burger",
                    "Joe Williams",
                    "Timmy Smith",
                    "Lisa Ray",
                    "Stanley Smith",
                    "Sam Jones",
                };

                for (int i = 0; i < amount; i++)
                {
                    people.Add(new Person
                    {
                        Age = i + 10,
                        Name = CommonUtil.RandomSampler(names),
                        AccountBalance = (100.99m * i),
                        BestFriend = CommonUtil.RandomSampler(people)
                    });
                }

                return people;
            }
        }
    }

.. code-block:: c#
    :caption: Simple Example of converting a collection to IDataReader.

    // Create N number of data model
    var people = GetPeople(1000);

    // Extension method call 
    var reader = people.ToReader();




Changelog
-------------    

V1.0.19

* Dependent package updates

V1.0.18

* Send file as email attachment added
* Minor fixes

V1.0.17

* Dependent package updates
* Minor fixes

V1.0.16

* Minor fixes

V1.0.15

* File Compression support
* Dependent package updates
* Minor fixes

V1.0.14

* Dependent package updates
* Minor fixes

V1.0.13

* Interface changes 
* Add Ability to pass Collection to Streamer Classes
* Minor fixes

V1.0.12

* Code ported to dotnet core
* Documentation completed
