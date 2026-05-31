Data FileReader
===============

Overview
--------

``VersaTul.Data.FileReader`` provides simple, testable file-reading helpers that produce ``IDataReader`` instances from common file formats.

It is especially useful when your downstream workflow already expects ``IDataReader`` input, such as a bulk-copy pipeline or a tabular import process.

Why Use This Package
--------------------

Use this package when the hard part of the problem is turning flat files into a tabular shape the rest of your pipeline can consume.

Its main value is that it bridges file input into ``IDataReader``-based workflows without forcing you to hand-roll parsing glue for every import job.

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
4. :doc:`scenario-guides/file-import` for an end-to-end file-to-database workflow.

Start Here If
-------------

1. Your source data is in CSV, text, or JSON files.
2. The next processing step expects ``IDataReader`` input.
3. You want the import path to remain testable and replaceable.

Not The Right First Package If
------------------------------

1. Your real need is export generation rather than import parsing.
2. You need direct SQL Server bulk upload but do not yet have file input in a readable shape.
3. You only need raw file-system utilities instead of tabular readers.

Works Well With
---------------

1. :doc:`bulk` when the next step is schema mapping and transport-neutral bulk copy.
2. :doc:`mssql` when the destination is SQL Server bulk upload.
3. :doc:`handler-file` when files must be discovered, moved, or archived around the import process.
4. :doc:`scenario-guides/file-import` when you want the full workflow before going deeper into the reference page.

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

Expected Result
---------------

When this package is working well:

1. import code stays focused on workflow instead of parsing details,
2. files become ``IDataReader`` sources that other VersaTul packages can consume directly, and
3. one-file and many-file imports follow the same mental model.

Next Step
---------

1. Read :doc:`scenario-guides/file-import` if you want to connect the reader to a complete database import path.
2. Read :doc:`bulk` if the next question is column mapping and copy results.
3. Read :doc:`mssql` if SQL Server bulk upload is the real destination.

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
