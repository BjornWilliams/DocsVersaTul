Logger
======

Overview
--------

``VersaTul.Logger`` provides the core logging abstractions shared by the file, mail, and web logger packages.

It defines a consistent logging contract, a standard log payload model, log levels, and a parser that can turn log events and exceptions into tabular, HTML, or JSON output.

When To Use This Package
------------------------

Use this package when you want to:

1. Define your own logger implementation against a common VersaTul contract.
2. Log both structured ``LogInfo`` entries and exceptions through the same interface.
3. Reuse shared parsing and formatting logic across multiple log sinks.
4. Keep application code independent from any single logging transport.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Logger

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Logger -Version latest

Related Packages
----------------

1. :doc:`logger-file` for flat-file logging.
2. :doc:`logger-mail` for email-based logging.
3. :doc:`logger-web` for HTTP endpoint logging.

Core Types And Concepts
-----------------------

``ILogger``
   Defines sync and async overloads for logging ``LogInfo``, ``Exception``, or both together.

``LogInfo``
   Standard log payload containing level, category, date, message, and optional trace identifier.

``ILogParser`` and ``LogParser``
   Convert log payloads and exception chains into ``Tab``, ``Html``, or ``Json`` output.

``LogLevel``
   Represents the severity of a log entry.

Key Capabilities
----------------

1. Log entries can be emitted synchronously or asynchronously.
2. ``LogInfo`` supports correlation through ``TraceId``.
3. ``LogParser`` walks inner exceptions and emits multi-depth exception details.
4. The parser supports output formats suitable for files, emails, and web payloads.

Basic Example
-------------

.. code-block:: csharp

   using VersaTul.Logger;
   using VersaTul.Logger.Contracts;

   public class DatabaseLogger : ILogger
   {
       private readonly ILogParser logParser;

       public DatabaseLogger(ILogParser logParser)
       {
           this.logParser = logParser;
       }

       public void Log(Exception exception) => LogAsync(exception).GetAwaiter().GetResult();
       public void Log(LogInfo logInfo) => LogAsync(logInfo).GetAwaiter().GetResult();
       public void Log(LogInfo logInfo, Exception exception) => LogAsync(logInfo, exception).GetAwaiter().GetResult();

       public Task LogAsync(Exception exception) => LogAsync(new LogInfo(LogLevel.Error, string.Empty, exception.Message), exception);
       public Task LogAsync(LogInfo logInfo) => LogAsync(logInfo, null);

       public Task LogAsync(LogInfo logInfo, Exception exception)
       {
           var payload = logParser.Parse(logInfo, exception, ParseFormat.Json);
           return SaveToDatabaseAsync(payload);
       }
   }

Parser Example
--------------

.. code-block:: csharp

   var parser = new LogParser();
   var info = new LogInfo(LogLevel.Error, "Orders", "Unable to process order", traceId: "trace-123");

   var html = parser.Parse(info, new InvalidOperationException("Boom"), ParseFormat.Html);
   var json = parser.Parse(info, ParseFormat.Json);

Notes
-----

1. ``LogInfo.ToString()`` produces a tab-separated representation, but the parser is the richer integration point.
2. The base package does not write anywhere by itself; sink packages provide the actual transport.
3. If you need a custom sink, implement ``ILogger`` and optionally reuse ``ILogParser``.
