Data FileReader
===============

Overview
--------

``VersaTul.Data.FileReader`` provides simple, testable file-reading helpers that produce ``IDataReader`` instances from common file formats.

It is especially useful when your downstream workflow already expects ``IDataReader`` input, such as a bulk-copy pipeline or a tabular import process.

When To Use This Package
------------------------

Use this package when you want to:

1. Read CSV, text, or JSON files through a consistent abstraction.
2. Enumerate files in a directory by extension and turn each into an ``IDataReader``.
3. Inject format-specific readers for testing or replacement.
4. Feed file data directly into :doc:`bulk` or :doc:`mssql` bulk-copy workflows.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

  dotnet add package VersaTul.Data.FileReader

Or with the Package Manager Console:

.. code-block:: console

  PM> NuGet\Install-Package VersaTul.Data.FileReader -Version latest

Related Packages
----------------

1. :doc:`bulk` for generic bulk-copy contracts built around ``IDataReader`` input.
2. :doc:`mssql` for SQL Server bulk-copy workflows.
3. :doc:`handler-file` for broader file-system operations used alongside reader workflows.

Core Types And Concepts
-----------------------

``IFileReader`` and ``DataFileReader``
  The main API for reading a single file or a directory of files into ``IDataReader`` instances.

``ICsvReader`` and ``CsvFileReader``
  CSV-specific reader abstraction and implementation.

``ITextReader`` and ``TextFileReader``
  Plain-text reader abstraction and implementation.

``IOptions`` and ``FileOptions``
  File-reader options for header handling, extension filters, and directory search behavior.

``ExtensionFilters``
  Enum that describes the supported file types.

``DisposableDataReader``
  Wrapper that ensures the returned reader and its underlying stream are disposed together.

Key Capabilities
----------------

1. Read one file by directory and file name.
2. Read all matching files in a directory based on ``ExtensionFilters``.
3. Control whether the file contains a header row.
4. Control directory search behavior with ``SearchOption``.
5. Swap reader implementations for tests or alternate parsing behavior.

Basic Example
-------------

.. code-block:: csharp

  using VersaTul.Data.FileReader;

  var fileReader = new DataFileReader(fileUtility, csvReader, textReader);
  var options = new FileOptions { HasHeader = true };

  using var reader = fileReader.Read("C:\\path\\to", "file.csv", options);

  if (reader != null)
  {
     while (reader.Read())
     {
        // Consume row data here.
     }
  }

Directory Example
-----------------

.. code-block:: csharp

  var options = new FileOptions
  {
     HasHeader = true,
     ExtensionFilters = new[] { ExtensionFilters.CSV, ExtensionFilters.TEXT },
     SearchOption = SearchOption.AllDirectories
  };

  var readers = fileReader.Read("C:\\data", options);

  foreach (var item in readers)
  {
     using (item)
     {
        while (item.Read())
        {
        }
     }
  }

Bulk Workflow Example
---------------------

.. code-block:: csharp

  var options = new FileOptions { HasHeader = true };
  using var reader = fileReader.Read("C:\\data", "people.csv", options);

  var mappings = new List<IBulkCopyColumnMapping>
  {
     new BulkCopyColumnMapping<Person, Person>(p => p.Name, p => p.Name),
     new BulkCopyColumnMapping<Person, Person>(p => p.Age, p => p.Age)
  };

  var copyDetail = new CopyDetail("Persons", reader, mappings);
  await bulkCopy.DoCopyAsync(copyDetail);

Dependency Injection
--------------------

Typical registrations look like this:

.. code-block:: csharp

  builder.RegisterType<FileUtility>().As<IFileUtility>().SingleInstance();
  builder.RegisterType<CsvFileReader>().As<ICsvReader>().SingleInstance();
  builder.RegisterType<TextFileReader>().As<ITextReader>().SingleInstance();
  builder.RegisterType<DataFileReader>().As<IFileReader>().SingleInstance();

Notes
-----

1. ``DataFileReader`` delegates parsing to the registered reader implementations.
2. ``FileOptions`` defaults to common text, CSV, and JSON extension filters.
3. This package is most valuable when your next processing step wants an ``IDataReader`` instead of raw file lines.
