Logger File
===========

Overview
--------

``VersaTul.Logger.File`` implements the shared logging contract by writing parsed log entries to a rolling flat file.

It combines the base logger abstractions with file-system helpers and an archiving policy so applications can log to disk without handling rotation and file growth manually.

When To Use This Package
------------------------

Use this package when you want to:

1. Persist logs locally in text form.
2. Rotate log files when they reach a configured size.
3. Enable daily rolling archives and retention cleanup.
4. Keep the logging sink independent from your application code.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Logger.File

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Logger.File -Version latest

Related Packages
----------------

1. :doc:`logger` for the shared logging contracts and parser.
2. :doc:`handler-file` for file-system abstractions used by the logger.
3. :doc:`configuration-defaults` for baseline logger settings.

Core Types And Concepts
-----------------------

``IFileLogger`` and ``FileLogger``
   File-backed ``ILogger`` implementation.

``ILogFileConfiguration`` and ``LogFileConfiguration``
   Expose file path, file name, max size, rolling, and retention settings.

``IArchiver`` and ``Archiver``
   Handle log-file rollover and archived file naming.

Key Capabilities
----------------

1. Supports the full sync and async ``ILogger`` contract.
2. Appends parsed log rows to the configured log file.
3. Creates the target directory automatically when missing.
4. Rotates files before append when archiving conditions are met.
5. Supports daily rolling and retention cleanup through configuration.

Basic Example
-------------

.. code-block:: csharp

   using VersaTul.Logger;
   using VersaTul.Logger.Contracts;
   using VersaTul.Logger.File;
   using VersaTul.Logger.File.Contracts;

   var configSettings = new Builder()
       .AddOrReplace("MaxFileSize", 10_000_000)
       .AddOrReplace("LogFileName", "app_log")
       .AddOrReplace("FilePath", "C:\\logs")
       .BuildConfig();

   ILogFileConfiguration configuration = new LogFileConfiguration(configSettings);
   ILogParser parser = new LogParser();
   IFileHandler fileHandler = new FileUtility(new DirectoryWrapper(), new DirectoryWrapper());
   IArchiver archiver = new Archiver(configuration, fileHandler);

   ILogger logger = new FileLogger(configuration, archiver, parser, fileHandler);

   await logger.LogAsync(new LogInfo(LogLevel.Information, "Startup", "Application started"));

Configuration Notes
-------------------

``ILogFileConfiguration`` exposes:

1. ``MaxFileSize``
2. ``LogFileName``
3. ``FilePath``
4. ``FullFilePath``
5. ``FullLogFileName``
6. ``EnableDailyRolling``
7. ``RetentionDays``

Notes
-----

1. ``FileLogger`` serializes concurrent writes with ``SemaphoreSlim``.
2. Logged rows are written using the parser's tab format.
3. This package is a good default sink when local operational visibility matters more than centralized transport.
