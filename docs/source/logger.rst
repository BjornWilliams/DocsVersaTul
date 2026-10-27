Logger
======

Overview
--------

``VersaTul.Logger`` provides the core logging abstractions shared by the file, mail, and web logger packages.

It defines a consistent logging contract, a standard log payload model, log levels, and a parser that can turn log events and exceptions into tabular, HTML, or JSON output.

Why Use This Package
--------------------

Use this package when you want one logging contract that can survive changes in delivery target.

Its value is the shared model: application code can emit ``LogInfo`` and exceptions once, while sink packages decide where those logs end up.

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


Related Packages
----------------

1. :doc:`logger-file` for flat-file logging.
2. :doc:`logger-mail` for email-based logging.
3. :doc:`logger-web` for HTTP endpoint logging.
4. :doc:`scenario-guides/logging-setup` for a practical file-logging setup.

Start Here If
-------------

1. You want application code to depend on a logger contract instead of a concrete sink.
2. You need shared parsing and payload formatting across several logging outputs.
3. You may add or change sinks later.

Not The Right First Package If
------------------------------

1. You need logs written somewhere immediately and have not chosen a sink package.
2. You are looking for email delivery or file rotation behavior rather than shared logging contracts.

Works Well With
---------------

1. :doc:`logger-file` for local disk logging.
2. :doc:`logger-mail` for email-based alerting.
3. :doc:`logger-web` for HTTP-based transport.
4. :doc:`scenario-guides/logging-setup` when you want the fastest useful logging workflow.

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
5. HTML keys and values are encoded before they are placed in table cells.
6. Tab output escapes backslashes, tabs, carriage returns, and line feeds so field boundaries and physical log records cannot be injected by data.

Output Safety
-------------

``LogParser`` HTML output encodes every key and value before writing it into an HTML cell. Tab output and ``LogInfo.ToString()`` keep their tab-separated layout while escaping backslashes as ``\\`` and representing tabs, carriage returns, and line feeds as ``\t``, ``\r``, and ``\n``. Consumers that need the original field text should reverse these escapes after splitting the fields.

Timestamp Format and Migration
------------------------------

``LogParser.Parse`` emits ``LogDate`` in invariant ISO 8601 round-trip format in
HTML, tab, and JSON output. ``LogInfo.ToString()`` uses the same format. Timestamps
include seven fractional-second digits; UTC inputs end in ``Z`` (for example,
``2026-01-15T12:30:45.1234567Z``), while local inputs include the local UTC offset.
Unspecified ``DateTime`` inputs are interpreted as local wall times and include
the local offset. ``LogInfo.Date`` retains its supplied value and kind, and the
default constructor continues to capture local time.

This is a **major-version output-format change**. Update ingestion rules that
expect culture-specific long date/time text to accept ISO 8601 with either ``Z``
or a numeric offset. After extracting the timestamp, use
``DateTimeOffset.Parse(value, CultureInfo.InvariantCulture)``. JSON retains its
string-valued ``LogDate`` property and existing schema; tab field positions do
not change. Existing historical records need a separate legacy parsing path
using the original writer's culture and time zone.

Prefer UTC inputs for unambiguous timestamps across machines and daylight-saving
transitions. Local and unspecified values follow .NET's local offset rules,
including ambiguous or invalid wall times; formatting does not validate those
times. File, mail, and web sinks using the built-in parser inherit this format
when consuming the updated Logger package. Custom parsers control their own
output. Arbitrary dictionary values and archive filenames are outside this
timestamp policy. Constructor and interface signatures are unchanged.

Basic Example
-------------

Supply separate native synchronous and asynchronous database callbacks. Keep their
dependencies alive through each call; the sink borrows them. The synchronous
callback must use the provider's native synchronous API. It must not block the
asynchronous callback. An async-only provider can reject synchronous logging and
direct callers to ``LogAsync`` instead.

.. code-block:: csharp

   using System;
   using System.Threading.Tasks;
   using VersaTul.Logger;
   using VersaTul.Logger.Contracts;

   public sealed class DatabaseLogger : ILogger
   {
       private readonly ILogParser parser;
       private readonly Action<string> save;
       private readonly Func<string, Task> saveAsync;

       public DatabaseLogger(ILogParser parser, Action<string> save, Func<string, Task> saveAsync)
       {
           ArgumentNullException.ThrowIfNull(parser);
           ArgumentNullException.ThrowIfNull(save);
           ArgumentNullException.ThrowIfNull(saveAsync);
           this.parser = parser;
           this.save = save;
           this.saveAsync = saveAsync;
       }

       public void Log(Exception exception)
       {
           ArgumentNullException.ThrowIfNull(exception);
           Log(new LogInfo(LogLevel.Error, string.Empty, exception.Message), exception);
       }

       public void Log(LogInfo logInfo) => Log(logInfo, null);

       public void Log(LogInfo logInfo, Exception? exception)
       {
           ArgumentNullException.ThrowIfNull(logInfo);
           save(parser.Parse(logInfo, exception, ParseFormat.Json));
       }

       public Task LogAsync(Exception exception)
       {
           ArgumentNullException.ThrowIfNull(exception);
           return LogAsync(new LogInfo(LogLevel.Error, string.Empty, exception.Message), exception);
       }

       public Task LogAsync(LogInfo logInfo) => LogAsync(logInfo, null);

       public Task LogAsync(LogInfo logInfo, Exception? exception)
       {
           ArgumentNullException.ThrowIfNull(logInfo);
           return saveAsync(parser.Parse(logInfo, exception, ParseFormat.Json));
       }
   }

Parser Example
--------------

.. code-block:: csharp

   var parser = new LogParser();
   var info = new LogInfo(LogLevel.Error, "Orders", "Unable to process order", traceId: "trace-123");

   var html = parser.Parse(info, new InvalidOperationException("Boom"), ParseFormat.Html);
   var json = parser.Parse(info, ParseFormat.Json);

Expected Result
---------------

When this package is doing its job:

1. application code emits one consistent logging payload model,
2. exception formatting is handled centrally, and
3. sink changes do not require broad changes to calling code.

Next Step
---------

1. Read :doc:`scenario-guides/logging-setup` for the quickest path to a useful file-based logger.
2. Read :doc:`logger-file` if disk logging is the first sink.
3. Compare :doc:`logger-mail` and :doc:`logger-web` if the delivery target is operational alerting or remote transport.

Notes
-----

1. ``LogInfo.ToString()`` produces a single-line escaped tab-separated representation, but the parser is the richer integration point.
2. The base package does not write anywhere by itself; sink packages provide the actual transport.
3. If you need a custom sink, implement ``ILogger`` and optionally reuse ``ILogParser``.
