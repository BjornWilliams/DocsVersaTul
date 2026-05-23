Collection Streamers
====================

Overview
--------

``VersaTul.Collection.Streamers`` turns in-memory collections or forward-only ``IDataReader`` sources into reusable export streams such as CSV, tab-delimited text, JSON, and JSONL.

The package is designed for workflows where a collection or row reader needs to be serialized once and then reused for multiple outputs, such as saving to disk, compressing into a zip archive, emailing as attachments, or converting to an ``IDataReader`` for downstream processing.

When To Use This Package
------------------------

Use this package when you want to:

1. Export collections to CSV, tab-delimited, or JSON files.
2. Reuse the same serialized output for file, email, and compression workflows.
3. Convert collections to ``IDataReader`` form for bulk-processing scenarios.
4. Apply display metadata from :doc:`display-attributes` during output generation.
5. Add cancellation-aware stream generation for large exports.
6. Write very large exports directly to disk without buffering the full file in memory.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Collection.Streamers

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Collection.Streamers -Version latest

Related Packages
----------------

1. :doc:`display-attributes` for column naming, ordering, and value formatting.
2. :doc:`compression` for zip-based export packaging.
3. :doc:`handler-file` for saving exported streams to disk.
4. :doc:`bulk` and :doc:`mssql` for ``IDataReader``-driven import workflows.

Core Types And Concepts
-----------------------

``IStreamer``
   Represents an export stream with file metadata, headings, an ``IDataReader``, and ``GetFileStream()`` methods.

``IStreamCreator``
   Defines the ``Create<T>()`` entry point used to bind a collection to a streamer instance.

``IDataReaderStreamCreator``
   Adds a ``Create(IDataReader, ...)`` path for binding existing forward-only row readers.

``IFileWritableStreamer``
   Adds ``WriteToFile()`` for writing export output directly to disk.

``CsvStreamer``, ``TabStreamer``, and ``JsonStreamer``
   Built-in export implementations for common flat-file formats.

``BaseStreamer``
   Common base class that owns file name handling, collection and reader binding, and cancellation-aware generation.

``FileConverter``
   Saves a streamer to disk, optionally as a compressed zip file.

``CompressTransport``
   Converts one or many streams into email attachments and compresses them when needed to stay within size limits.

``MailTransporter``
   Sends stream-based attachments through the mailer stack.

Key Capabilities
----------------

1. ``Create<T>()`` binds a collection to a reusable streamer instance.
2. ``Create(IDataReader, ...)`` binds an existing reader directly to a streamer.
3. ``GetFileStream()`` returns the serialized output as a ``MemoryStream``.
4. ``GetFileStream(CancellationToken)`` adds cancellation support during generation.
5. ``WriteToFile()`` writes output directly to disk.
6. ``CollectionReaderExtensions.ToReader()`` turns collections into ``IDataReader`` instances.
7. ``FileConverter.Save()`` can persist a streamer as plain output or compressed zip content.

Basic CSV Example
-----------------

.. code-block:: csharp

   using VersaTul.Collection.Streamers;
   using VersaTul.Handler.File;
   using VersaTul.Object.Converters;
   using VersaTul.Utilities;

   var utility = new CommonUtility();
   var directoryWrapper = new DirectoryWrapper();
   var fileUtility = new FileUtility(directoryWrapper, directoryWrapper);
   var flattener = new Flattener();

   var csvStreamer = new CsvStreamer(utility, fileUtility, flattener);

      using var fileStream = csvStreamer
         .Create(people, "people")
         .GetFileStream();

IDataReader Example
-------------------

.. code-block:: csharp

   using VersaTul.Collection.Streamers.Extensions;

   using var reader = people.ToReader();

   while (reader.Read())
   {
       Console.WriteLine(reader.GetValue(0));
   }

Direct To Disk Example
----------------------

.. code-block:: csharp

   using VersaTul.Collection.Streamers.Contracts;

   var filePath = ((IFileWritableStreamer)csvStreamer.Create(people, "people"))
      .WriteToFile("C:\\exports");

IDataReader To Disk Example
---------------------------

.. code-block:: csharp

   using System.Data;
   using VersaTul.Collection.Streamers.Contracts;

   IDataReader reader = dataService.ExecuteReader(command);

   var filePath = ((IFileWritableStreamer)csvStreamer.Create(reader, "orders-export"))
      .WriteToFile("C:\\exports");

Save To Disk Example
--------------------

.. code-block:: csharp

   using VersaTul.Collection.Streamers.Compressions;
   using VersaTul.Collection.Streamers.Converters;
   using VersaTul.Compression;

   var zipper = new Zipper(new Archiver());
   var compressor = new Compressor(zipper);
   var fileConverter = new FileConverter(fileUtility, compressor);

   var streamer = csvStreamer.Create(people, "people");
   fileConverter.Save(streamer, "C:\\exports", compressed: true);

Notes
-----

1. ``BaseStreamer`` reinitializes its internal reader and output stream state each time ``Create(...)`` is called.
2. ``CsvStreamer`` supports a custom encoding strategy for value escaping.
3. ``WriteToFile()`` is the preferred path for very large exports because rows can be written directly to disk.
4. ``FileConverter.Save()`` uses direct file writing automatically for non-compressed output when the streamer supports it.
5. This package works especially well with :doc:`display-attributes` when exported column names and formatted values matter.
