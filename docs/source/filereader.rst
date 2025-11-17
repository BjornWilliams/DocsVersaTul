VersaTul Data.FileReader
=========================

``VersaTul.Data.FileReader`` is a small library that provides simple, testable
file-reading helpers to produce ``IDataReader`` instances from common file
formats. It focuses on CSV and plain text files and exposes a thin
abstraction so callers can easily obtain forward-only readers that integrate
with other data-processing or bulk-copy components.

Features
--------

- Read a single file (CSV or text) and obtain an ``IDataReader``.
- Enumerate and read files from a directory based on extension filters.
- Pluggable readers via ``ICsvReader`` and ``ITextReader`` interfaces so you
  can replace or mock readers in tests.
- Supports options (``IOptions`` / ``FileOptions``) such as whether CSV files
  contain a header row.
- Returns readers wrapped so underlying streams are disposed when the reader
  is disposed.

Key types
---------

- ``IFileReader`` - high-level API for reading a single file or all files in a
  directory. Primary members include::

     IDataReader? Read(string directoryPath, string filename, IOptions options)
     IEnumerable<IDataReader> Read(string directoryPath, IOptions options)

- ``ICsvReader`` - CSV-specific reader that returns an ``IDataReader`` for a
  given file path and options.
- ``ITextReader`` - Plain-text reader that returns an ``IDataReader`` for a
  given file path and options.
- ``IOptions`` / ``FileOptions`` - Options to control reading behavior (for
  example ``HasHeader`` and ``ExtensionFilters``).
- ``DisposableDataReader`` - wrapper that ensures both the returned reader and
  its underlying stream are disposed together.

Installation
------------

This project is typically consumed as part of the larger VersaTul solution.
If distributed as a NuGet package, install it using::

   dotnet add package VersaTul.Data.FileReader

Quick usage
-----------

Read a single CSV file::

   var fileReader = new DataFileReader(fileUtility, csvReader, textReader);
   var options = new FileOptions { HasHeader = true };

   using var reader = fileReader.Read("C:\\path\\to", "file.csv", options);
   if (reader != null)
   {
       while (reader.Read())
       {
           // process columns via reader.GetValue(i) or reader.GetString(i)
       }
   }

Read all CSV and text files from a directory (respecting
``options.ExtensionFilters``)::

   var options = new FileOptions { HasHeader = true, ExtensionFilters = new [] { ExtensionFilters.CSV, ExtensionFilters.TEXT } };
   var readers = fileReader.Read("C:\\path\\to", options);

   foreach (var r in readers)
   {
       using (r)
       {
           while (r.Read()) { /* process row */ }
       }
   }

Notes
-----

- ``DataFileReader`` delegates actual parsing to the registered
  ``ICsvReader``/``ITextReader`` implementations so you can swap in different
  CSV parsers or mocks for testing.
- ``CsvFileReader`` in this project uses ``LumenWorks.Framework.IO.Csv``
  internally and returns an ``IDataReader`` that disposes the underlying
  stream when the reader is disposed.

Dependency injection
--------------------

When using an IoC container you can register the concrete types used by the
host. Example using Autofac (similar to the ``AppModule`` used in the sample
host project)::

   builder.RegisterType<FileUtility>().As<IFileUtility>().SingleInstance();
   builder.RegisterType<CsvFileReader>().As<ICsvReader>().SingleInstance();
   builder.RegisterType<TextFileReader>().As<ITextReader>().SingleInstance();
   builder.RegisterType<DataFileReader>().As<IFileReader>().SingleInstance();

Example using ``Microsoft.Extensions.DependencyInjection``::

   services.AddSingleton<IFileUtility, FileUtility>();
   services.AddSingleton<ICsvReader, CsvFileReader>();
   services.AddSingleton<ITextReader, TextFileReader>();
   services.AddSingleton<IFileReader, DataFileReader>();

Extensibility
-------------

- To support additional file formats add a reader that implements ``IReader``
  (or a format-specific interface) and update ``DataFileReader`` registration to
  include it.
- ``FileOptions.ExtensionFilters`` drives directory scanning; add and handle
  new ``ExtensionFilters`` values when extending supported formats.

Examples
--------

1) Print column headings and first N rows::

   var options = new FileOptions { HasHeader = true };
   using var reader = fileReader.Read("C:\\data", "customers.csv", options);

   if (reader != null)
   {
       // Print column names
       var fieldCount = reader.FieldCount;
       for (int i = 0; i < fieldCount; i++)
           Console.Write(reader.GetName(i) + (i + 1 < fieldCount ? ", " : "\n"));

       int row = 0;
       while (reader.Read() && row < 25)
       {
           for (int i = 0; i < fieldCount; i++)
               Console.Write(reader.GetValue(i) + (i + 1 < fieldCount ? " | " : "\n"));
           row++;
       }
   }

2) Using ``DataFileReader`` with a bulk copy operation::

   var options = new FileOptions { HasHeader = true };
   using var reader = fileReader.Read("C:\\data", "people.csv", options);

   var mappings = new List<IBulkCopyColumnMapping> {
       new BulkCopyColumnMapping<Person, Person>(p => p.Name, p => p.Name),
       new BulkCopyColumnMapping<Person, Person>(p => p.Age, p => p.Age)
   };

   var copyDetail = new CopyDetail("Persons", reader, mappings);
   bulkCopy.DoCopy(copyDetail);

   > Note: ``CopyDetail`` constructors in this solution expect an ``IDataReader`` for source data. Ensure the reader is disposed after the bulk operation completes.

3) Unit test: mock ``ICsvReader`` to return a controlled ``IDataReader``::

   var mockCsv = new Mock<ICsvReader>();
   var mockOptions = new FileOptions { HasHeader = true };

   // Build a simple DataTable and return its reader
   var dt = new DataTable();
   dt.Columns.Add("Id", typeof(int));
   dt.Columns.Add("Name", typeof(string));
   dt.Rows.Add(1, "Alice");

   mockCsv.Setup(c => c.Read(It.IsAny<string>(), It.IsAny<IOptions>())).Returns(dt.CreateDataReader());

   var fileReader = new DataFileReader(fileUtilityMock.Object, mockCsv.Object, textReaderMock.Object);
   var reader = fileReader.Read("C:\\path", "file.csv", mockOptions);
   Assert.NotNull(reader);

License
-------

This project follows the same license as the VersaTul solution. See the
repository ``LICENSE`` file for details.
