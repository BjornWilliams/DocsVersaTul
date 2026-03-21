Handler File
============

Overview
--------

``VersaTul.Handler.File`` wraps common file-system operations and adds typed file models for working with text, CSV, custom extensions, zip content, and raw streams.

The package is useful when you want file operations behind interfaces for easier testing and when higher-level packages need to persist typed file content rather than manually coordinate paths, extensions, and stream writes.

When To Use This Package
------------------------

Use this package when you want to:

1. Read or write files through abstractions instead of calling ``System.IO`` directly.
2. Save typed file content such as text, CSV, custom files, or zip streams.
3. Add async wrappers around common file operations.
4. Reuse path, extension, and directory helpers across the codebase.
5. Support export workflows from :doc:`streamers` and archive workflows from :doc:`compression`.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Handler.File

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Handler.File -Version latest

Related Packages
----------------

1. :doc:`streamers` for export generation that can be saved to disk.
2. :doc:`compression` for zip-based file content.
3. :doc:`file-reader` for the inverse workflow of turning files back into ``IDataReader`` instances.

Core Types And Concepts
-----------------------

``IFileHandler``
   Combines file and directory wrappers plus helper operations such as extension handling, file discovery, and line-by-line reading.

``IFileUtility`` and ``FileUtility``
   Higher-level file service for reading all content, saving typed files, and async wrappers.

``IDirectoryWrapper`` and ``IFileWrapper``
   Thin abstractions over file-system APIs used by the higher-level handlers.

``FileResult``
   Result model returned by reads, including existence and blank-file flags.

``FileInfo`` and typed variants
   File models such as ``TextFileInfo``, ``CsvFileInfo``, ``CustomFileInfo``, ``StreamFileInfo``, and ``ZipFileInfo``.

Key Capabilities
----------------

1. ``ReadAll()`` and ``ReadAllAsync()`` read text files into a ``FileResult``.
2. ``SaveOrUpdate()`` and ``SaveOrUpdateAsync()`` append or create text-based files.
3. ``Save()`` and ``SaveAsync()`` persist stream-based files.
4. Path and extension helpers simplify file naming and discovery.
5. Directory creation is handled automatically before writes.

Save Text Example
-----------------

.. code-block:: csharp

   using VersaTul.Handler.File;
   using VersaTul.Handler.File.Types;

   var directoryWrapper = new DirectoryWrapper();
   var fileUtility = new FileUtility(directoryWrapper, directoryWrapper);

   var file = new TextFileInfo("C:\\exports", "report", "Large amount of text to save");
   fileUtility.SaveOrUpdate(file);

Read Example
------------

.. code-block:: csharp

   var result = fileUtility.ReadAll("C:\\exports\\report.txt");

   if (result.IsExists)
   {
       foreach (var line in result.Content)
       {
           Console.WriteLine(line);
       }
   }

Save Stream Example
-------------------

.. code-block:: csharp

   using var memoryStream = new MemoryStream(System.Text.Encoding.UTF8.GetBytes("hello"));

   var streamFile = new ZipFileInfo("C:\\exports", "archive", memoryStream);
   await fileUtility.SaveAsync(streamFile);

Notes
-----

1. ``FileUtility`` uses a lock to serialize writes from the same process.
2. The async methods are wrapper-based async, which is useful for consistency at the service boundary.
3. The typed file models are the main value-add over direct ``System.IO`` usage.
