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

Prerequisites and Tested Versions
---------------------------------

- Install a .NET SDK that supports the target framework. The sample projects target ``net8.0``, ``net9.0``, and ``net10.0``; the documentation workflow validates all three.
- The runnable sample writes to a temporary local directory. It needs no logging service, credentials, or production filesystem path.

The runnable sample pins these package versions:

.. list-table:: Tested file-logging sample packages
   :header-rows: 1

   * - Package
     - Version
     - Role
   * - ``VersaTul.Logger``
     - ``1.0.11``
     - Shared logging contract, payload, and parser
   * - ``VersaTul.Logger.File``
     - ``1.0.32``
     - File sink
   * - ``VersaTul.Configurations``
     - ``1.0.18``
     - File logger settings
   * - ``VersaTul.Handler.File``
     - ``1.0.21``
     - File and directory operations
   * - ``VersaTul.Utilities``
     - ``1.0.16``
     - Shared formatting utilities

Why This Package Combination
----------------------------

``VersaTul.Logger`` defines the shared log event and parser contracts, while ``VersaTul.Logger.File`` writes those events to a local file. ``VersaTul.Configurations`` supplies the file path, log name, and size limit. The sample also constructs the sink with ``VersaTul.Handler.File`` and ``VersaTul.Utilities`` helpers, so those are direct project dependencies too. This gives a small application a real file-backed result without adding a logging service or credentials.

Step 1: Define The File Logger Configuration
--------------------------------------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

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
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

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
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

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

Cleanup, Cancellation, and Production Notes
--------------------------------------------

- The sample removes its unique temporary log directory in ``finally``. A production path should have deliberate permissions, retention, backup, and disk-space monitoring.
- The sample lets file-system and logger errors propagate to its caller. Catch and report them at the application boundary, and avoid writing credentials, tokens, or sensitive personal data to logs.
- ``FileLogger`` also implements ``ICancellableFileLogger`` for calls that need a ``CancellationToken``. Cancellation covers the asynchronous write and path gate, but cannot interrupt synchronous rotation and a cancelled append may leave partial output. The basic ``ILogger`` contract shown in the guide has no cancellation parameter.

Runnable Sample
---------------

The complete `FileLogging project <https://github.com/BjornWilliams/DocsVersaTul/tree/VT-Upgrade-And-Revisions/docs/samples/FileLogging>`_ writes to a temporary directory and reads the resulting log record. Clone the audit branch and run it from the repository root:

.. code-block:: console

   git clone --branch VT-Upgrade-And-Revisions https://github.com/BjornWilliams/DocsVersaTul.git
   cd DocsVersaTul
   dotnet run --project docs/samples/FileLogging/FileLogging.csproj --framework net8.0

The project also targets ``net9.0`` and ``net10.0``; substitute either framework in the command to run those targets. The sample source is included below for reference.

The sample logs this input event:

.. code-block:: csharp
   :caption: Input event for the runnable sample.

   new LogInfo(LogLevel.Information, "Startup", "Application started")

The log record includes a timestamp, so the sample asserts and prints these stable fields as its deterministic result:

.. code-block:: text

   LogLevel: Information
   CategoryName: Startup
   LogMessage: Application started

.. literalinclude:: ../../samples/FileLogging/Program.cs
   :language: csharp
   :caption: Program.cs

Its expected console output is:

.. literalinclude:: ../../samples/FileLogging/ExpectedOutput.txt
   :language: text
   :caption: Expected output

Why This Workflow Helps
-----------------------

This package combination gives you a practical baseline for service diagnostics.

You get:

1. one logging contract,
2. one reusable payload model, and
3. one file-based sink with rolling support.

That is enough to add observability early without designing a full logging platform first.

Likely Failure Messages and Fixes
---------------------------------

1. ``error NETSDK1045: The current .NET SDK does not support targeting .NET 10.0.`` — Install the .NET 10 SDK, or run the sample with ``--framework net8.0`` or ``net9.0``.
2. ``error NU1301: Unable to load the service index for source https://api.nuget.org/v3/index.json.`` — Restore network access or configure the NuGet feed that contains the pinned packages, then rerun ``dotnet restore``.
3. ``InvalidOperationException: The file did not contain exactly the expected log record.`` — Check that the temporary directory is writable and that the configured path, log filename, level, category, and message match the sample.

Common Mistakes
---------------

1. Installing only ``VersaTul.Logger`` and expecting it to persist log entries by itself.
2. Mixing sink-specific behavior directly into application code instead of relying on the shared contract.
3. Waiting to add logging until after background jobs, imports, or scheduled tasks are already hard to debug.

Next Step
---------

For the shared logger contracts and parser details, continue with :doc:`/logger`.
