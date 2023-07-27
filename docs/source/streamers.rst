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
#. ``IStreamer`` : A base interface that represents the data contained in the stream and the functionality than can be applied to the data.
#. ``IStreamCreator`` : A base interface that represents the functionality for creating streamers.
#. ``ICsvStreamer`` : A specific stream type interface that represents the functionality for creating csv streamers.
#. ``ITabStreamer`` : A specific stream type interface that represents the functionality for creating tab streamers.
#. ``IJsonStreamer`` : A specific stream type interface that represents the functionality for creating json streamers.
#. ``BaseStreamer`` : A concrete implementation of the IStreamer and IStreamCreator interfaces. Providing common functionality for all streamers.
#. ``CsvStreamer`` : A concrete implementation of the ICsvStreamer interface.
#. ``JsonStreamer`` : A concrete implementation of the IJsonStreamer interface.
#. ``TabStreamer`` : A concrete implementation of the ITabStreamer interface.


Functional Summary
------------------
#. **IStreamer.GetFileStream()** : Returns the file data as a stream whose backing store is MemoryStream.
#. **IStreamCreator.Create<T>(IEnumerable<T> source, string fileName)** : Creates a Memory Stream from the given collection.



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
                Console.WriteLine("Hello, World!");

                // Create N number of data model
                var people = GetPeople(1000);

                // Create Needed Instances
                var iOWrapper = new IOWrapper();
                var utility = new CommonUtility();
                var handler = new FileHandler(iOWrapper, iOWrapper);
                var flattener = new Flattener();
                var zipper = new Zipper(new Archiver());
                var compressor = new Compressor(zipper);
                var fileUtil = new FileUtility(handler, iOWrapper);
                var fileConvert = new FileConverter(fileUtil, handler, compressor);

                // Creating the CsvStreamer Instance
                var csvStreamer = new CsvStreamer(utility, handler, flattener);

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