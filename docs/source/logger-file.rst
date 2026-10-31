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
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using VersaTul.Configurations;
   using VersaTul.Handler.File;
   using VersaTul.Logger;
   using VersaTul.Logger.File;
   using VersaTul.Logger.File.Configurations;
   using VersaTul.Utilities.Contracts;

   // utility is your application's IUtility implementation.
   var configuration = new LogFileConfiguration(new ConfigSettings
   {
       { "FilePath", "logs" },
       { "LogFileName", "app.txt" },
       { "MaxFileSize", 10_000_000L }
   }, utility);
   var handler = new FileUtility(new DirectoryWrapper(), new DirectoryWrapper());
   var logger = new FileLogger(configuration, new Archiver(configuration, handler), new LogParser(), handler);
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
2. Logged rows are written using the parser's single-line escaped tab format; backslashes are escaped as ``\\`` and tabs, carriage returns, and line feeds in fields are represented as ``\t``, ``\r``, and ``\n``.
3. This package is a good default sink when local operational visibility matters more than centralized transport.

Paths, concurrency, and ownership
----------------------------------------

Relative FilePath values resolve against IUtility.GetExecutingPath; rooted paths use
platform path rules. Use Path.Combine to construct nested paths and provide a simple
LogFileName. Active logs, archives, and retention scans use the resolved directory.
On Unix, backslashes are ordinary filename characters; migrate any files previously
created with a literal backslash, and review archives previously written relative to
the process working directory. Paths/configuration are trusted and must remain stable
during delivery. This API does not provide directory containment for untrusted names.

Logger instances in the same process coordinate by Path.GetFullPath of the destination.
Comparison is case-insensitive on Windows and ordinal on other platforms. Rotation,
retention, append, flush, and disposal share the same gate. Idle gates are removed;
different paths can proceed independently. Symbolic links, hard links, filesystem case
aliases on non-Windows systems, separate assembly load contexts, and other processes
are not coordinated. Use one canonical spelling and a single writer process for each
file. Standalone Archiver calls and external writers must not race logger delivery.
All logger instances for a file must use consistent rotation/retention settings and
an archiver configured for that same file. Custom callbacks must not re-enter logging
for the same path.

LogAsync schedules synchronous directory/rotation/open operations on the thread pool,
then awaits asynchronous writing and disposal. It does not block the caller on file
maintenance, but slow maintenance occupies a worker thread. Await every call; completion
means the writer has flushed and closed, not that storage has performed a durable fsync.
Exceptions propagate through the returned task and release the path gate. There is no
background queue to flush on logger disposal. Synchronous Log methods use native file
operations and run maintenance and parsing on the caller thread. Sync and async writes
share the path gate. Rotation checks run before append, so a single record may exceed
the configured size. Retention cleanup happens during rotation.

Migration: review custom callback thread assumptions for synchronous calls.
Single-Exception overloads require a non-null exception and now raise
``ArgumentNullException`` for null; replace catches of the prior
``NullReferenceException``. These changes require Major compatibility review.

.. BEGIN VERSATUL GENERATED PACKAGE QUICKSTART

Canonical package quickstart
----------------------------

Write escaped tab-delimited log records to files with size-based or daily rotation and optional retention.

Install the package in your application with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Logger.File

Minimal package example
^^^^^^^^^^^^^^^^^^^^^^^

This compiler-verified example is also used by the packed package README.

.. literalinclude:: ../samples/Packages/VersaTul.Logger.File/Program.cs
   :language: csharp
   :caption: VersaTul.Logger.File minimal package example

Expected output
^^^^^^^^^^^^^^^

.. literalinclude:: ../samples/Packages/VersaTul.Logger.File/ExpectedOutput.txt
   :language: text
   :caption: Expected output

Support
^^^^^^^

Documentation FAQ <https://docsversatul.readthedocs.io/en/latest/faq.html>_.

.. END VERSATUL GENERATED PACKAGE QUICKSTART
