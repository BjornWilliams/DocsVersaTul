Logging Setup Workflow
======================

This guide shows the simplest useful logging path for a service or background process: use the shared logging abstractions from ``VersaTul.Logger`` and write to disk with ``VersaTul.Logger.File``.

This is a strong first operational workflow because it gives you immediate visibility without forcing you into a centralized logging platform on day one.

When To Use This Workflow
-------------------------

Use this workflow when you need to:

1. Add structured log entries to an application quickly.
2. Capture exceptions and normal events through one shared contract.
3. Persist logs locally with rolling and retention support.

Packages To Install
-------------------

.. code-block:: console

   dotnet add package VersaTul.Logger
   dotnet add package VersaTul.Logger.File

Step 1: Define The File Logger Configuration
--------------------------------------------

.. code-block:: csharp

   using VersaTul.Configuration.Defaults;
   using VersaTul.Logger.File.Contracts;

   var configSettings = new Builder()
       .AddOrReplace("MaxFileSize", 10_000_000)
       .AddOrReplace("LogFileName", "app_log")
       .AddOrReplace("FilePath", "C:\\logs")
       .BuildConfig();

   ILogFileConfiguration configuration = new LogFileConfiguration(configSettings);

Step 2: Build The Logger
------------------------

.. code-block:: csharp

   using VersaTul.Handler.File;
   using VersaTul.Logger;
   using VersaTul.Logger.Contracts;
   using VersaTul.Logger.File;

   ILogParser parser = new LogParser();
   IFileHandler fileHandler = new FileUtility(new DirectoryWrapper(), new DirectoryWrapper());
   IArchiver archiver = new Archiver(configuration, fileHandler);

   ILogger logger = new FileLogger(configuration, archiver, parser, fileHandler);

Step 3: Log Useful Events
-------------------------

Log both normal application activity and failures through the same interface.

.. code-block:: csharp

   await logger.LogAsync(new LogInfo(LogLevel.Information, "Startup", "Application started"));

   try
   {
       throw new InvalidOperationException("Import failed");
   }
   catch (Exception ex)
   {
       await logger.LogAsync(new LogInfo(LogLevel.Error, "Import", "File import failed", traceId: "trace-42"), ex);
   }

What You Should See
-------------------

When this workflow is working:

1. The target log directory is created automatically if it does not exist.
2. Log rows are appended in the configured file format.
3. Exception details are captured through the shared parser and file sink.

Why This Workflow Helps
-----------------------

This package combination gives you a practical baseline for service diagnostics.

You get:

1. one logging contract,
2. one reusable payload model, and
3. one file-based sink with rolling support.

That is enough to add observability early without designing a full logging platform first.

Common Mistakes
---------------

1. Installing only ``VersaTul.Logger`` and expecting it to persist log entries by itself.
2. Mixing sink-specific behavior directly into application code instead of relying on the shared contract.
3. Waiting to add logging until after background jobs, imports, or scheduled tasks are already hard to debug.

Related Package Pages
---------------------

1. :doc:`/logger`
2. :doc:`/logger-file`

What To Read Next
-----------------

1. Read :doc:`/logger` for the shared contracts and parser details.
2. Read :doc:`/logger-file` for configuration properties and rolling behavior.
3. If email or HTTP delivery matters more than local files, compare :doc:`/logger-mail` and :doc:`/logger-web`.