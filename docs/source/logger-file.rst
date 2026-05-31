Logger File
===========

Overview
--------

``VersaTul.Logger.File`` implements the shared logging contract by writing parsed log entries to a rolling flat file.

It combines the base logger abstractions with file-system helpers and an archiving policy so applications can log to disk without handling rotation and file growth manually.

Why Use This Package
--------------------

Use this package when you want the simplest practical sink for service diagnostics and batch-job visibility.

Its main value is that it gives you a usable rolling file logger without pushing sink-specific logic into application code.

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
4. :doc:`scenario-guides/logging-setup` for an end-to-end logger setup walkthrough.

Start Here If
-------------

1. Local files are a sufficient first logging destination.
2. You want rotation and retention behavior without writing it yourself.
3. You are adding operational visibility to a service, scheduler, or import process quickly.

Not The Right First Package If
------------------------------

1. You only need the shared logging contract and have not chosen a sink yet.
2. Centralized remote delivery matters more than local visibility.

Works Well With
---------------

1. :doc:`logger` for the shared logging contract and parser.
2. :doc:`configuration-defaults` when you want baseline logging settings.
3. :doc:`scenario-guides/logging-setup` when you want the end-to-end setup path first.

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

Expected Result
---------------

When this package is working well:

1. the target directory is created automatically,
2. log entries are written through one shared contract, and
3. rotation behavior happens through configuration instead of custom code in the application.

Next Step
---------

1. Read :doc:`scenario-guides/logging-setup` for the full service-logging workflow.
2. Read :doc:`logger` if you want the sink-agnostic contract details behind this implementation.
3. Compare :doc:`logger-mail` when alerts should be delivered instead of just stored on disk.

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
