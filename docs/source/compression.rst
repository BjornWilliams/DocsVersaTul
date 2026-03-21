Compression
===========

Overview
--------

``VersaTul.Compression`` provides a small abstraction over ``System.IO.Compression`` for zipping and unzipping in-memory files.

The package centers around ``ZipStream`` objects, which pair a file name, content type, and ``MemoryStream`` so higher-level workflows can archive generated files without dealing directly with zip entry wiring.

When To Use This Package
------------------------

Use this package when you want to:

1. Package one or many in-memory files into a zip archive.
2. Extract zip archives back into named in-memory streams.
3. Keep compression concerns separate from file generation logic.
4. Support workflows that generate exports before saving, emailing, or uploading them.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Compression

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Compression -Version latest

Related Packages
----------------

1. :doc:`streamers` for generating in-memory export streams.
2. :doc:`handler-file` for persisting compressed output to disk.

Core Types And Concepts
-----------------------

``ZipStream``
   Carries the file name, content type, and in-memory content to archive.

``IArchiver`` and ``Archiver``
   Write individual ``ZipStream`` instances into a ``ZipArchive``.

``IZipper`` and ``Zipper``
   Create zip archives from one or many ``ZipStream`` objects and can also unzip archive streams.

Key Capabilities
----------------

1. Zip a single ``ZipStream`` or a collection of them.
2. Choose a specific ``CompressionLevel`` when creating the archive.
3. Unzip archive streams back into ``ZipStream`` instances.
4. Filter extracted entries during unzip with a predicate.

Basic Example
-------------

.. code-block:: csharp

   using System.IO;
   using VersaTul.Compression;

   IArchiver archiver = new Archiver();
   IZipper zipper = new Zipper(archiver);

   var zipStream = new ZipStream
   {
       ContentType = "text/csv",
       FileName = "people.csv",
       Stream = new MemoryStream(System.Text.Encoding.UTF8.GetBytes("Name,Age\nJane,42"))
   };

   using var archive = zipper.Zip(zipStream);

Unzip Example
-------------

.. code-block:: csharp

   using var archiveStream = File.OpenRead("exports.zip");

   var files = zipper.Unzip(archiveStream, entryName => entryName.EndsWith(".csv"));

   foreach (var item in files)
   {
       Console.WriteLine(item.FileName);
   }

Notes
-----

1. ``ZipStream.Stream`` is a ``MemoryStream``, so this package is best suited to in-memory export workflows.
2. The package does not decide where archives are stored or sent; pair it with :doc:`handler-file` or :doc:`streamers` depending on your workflow.
