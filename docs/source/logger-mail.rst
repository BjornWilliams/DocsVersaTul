Logger Mail
===========

Overview
--------

``VersaTul.Logger.Mail`` implements the shared logger contract by sending log events as email.

It builds on the base logger package and the mailer package, adding throttling, batching, retry behavior, and a dead-letter queue for failed deliveries.

When To Use This Package
------------------------

Use this package when you want to:

1. Send important operational events directly to an inbox.
2. Deliver HTML-formatted exception details.
3. Throttle bursts of log traffic instead of flooding recipients.
4. Batch excess messages during a throttle window.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Logger.Mail


Related Packages
----------------

1. :doc:`logger` for the shared logger contract and parser.
2. :doc:`mailer` for SMTP delivery.

Core Types And Concepts
-----------------------

``IMailLogger`` and ``MailLogger``
   Email-backed logger implementation.

``IMailConfiguration``
   Supplies sender, recipient, SMTP, attachment, and retry-related settings.

``ILogParser``
   Produces the HTML body sent for logged events.

Key Capabilities
----------------

1. Supports all ``ILogger`` sync and async overloads.
2. Formats mail bodies as HTML through ``ILogParser``.
3. Retries transient delivery failures.
4. Throttles sends within a moving time window.
5. Batches overflow items and tracks failed sends in a dead-letter queue.

Basic Example
-------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using VersaTul.Logger;
   using VersaTul.Logger.Contracts;
   using VersaTul.Logger.Mail;

   await using var logger = new MailLogger(dispatcher, mailConfiguration, new LogParser());

   await logger.LogAsync(
       new LogInfo(LogLevel.Error, "Payments", "Payment gateway timeout", traceId: "trace-456"),
       new TimeoutException("Gateway timeout"));

Operational Notes
-----------------

``MailLogger`` exposes two useful counters:

1. ``DeadLetterCount`` for currently retained failed deliveries.
2. ``PendingBatchCount`` for throttled items waiting to be batched.

Notes
-----

1. Throttling and batching are built into the logger implementation, not delegated to the mailer package.
2. This sink is best for high-value alerts, not high-volume debug traffic.
3. If send volume exceeds the configured window, messages are queued and later combined into a batched message.

Asynchronous Delivery
---------------------

``LogAsync`` awaits ``IAsyncMailDispatcher.SendMailAsync`` when supported. The
built-in ``MailDispatcher`` and ``SmtpClientWrapper`` perform native asynchronous
SMTP with nonblocking retry delays. Legacy custom ``IMailDispatcher`` instances
remain supported through a worker-thread fallback; implement
``IAsyncMailDispatcher`` to avoid blocked workers. Synchronous ``Log`` calls use the
required ``IMailDispatcher.SendMail`` directly, including on async-capable dispatchers.
Both paths share serialization, throttling, retry ownership and dead-letter retention.
Keep the dispatcher and transport alive until
logging tasks complete, and serialize calls sharing one SMTP client.

Migration: dual-capability dispatchers must support their required native
``SendMail`` implementation for synchronous logging. Use ``LogAsync`` for
async-only delivery. Single-Exception overloads now reject null with
``ArgumentNullException`` instead of ``NullReferenceException``. These changes
require Major compatibility review.

Retry ownership is described below. Use ``ICancellableMailLogger`` for token-aware
calls. Throttled calls complete after queueing, not delivery; cancelling an enqueue
call does not cancel accepted work.

Background Flush and Shutdown
-----------------------------

The first throttled event starts a background loop that checks once per throttle
window (one minute by default). It rotates the window and sends batches within
the remaining budget, including a final partial batch without another log call.
The loop exits when the queue empties and restarts when needed. Defaults are 25
successful sends per window and at most ten events per batch. Slow delivery may
delay subsequent checks; one logger never overlaps its own sends.

``MailLogger`` implements the additive ``IFlushableMailLogger`` interface, extending
``IMailLogger`` and ``IAsyncDisposable``. Resolve the new interface or the concrete
class to access lifecycle methods. Existing ``IMailLogger`` implementers do not
need new members.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   await logger.FlushAsync(); // Attempts every queued batch, bypassing throttling.

Use ``await using`` as in the example, or await ``DisposeAsync`` during shutdown
before disposing the externally owned dispatcher/SMTP transport. Disposal rejects
new log/flush calls with ``ObjectDisposedException``, waits for active delivery,
stops the background loop, and drains remaining batches without the throttle.
Repeated disposal awaits the same task. Failed batches become dead-letter entries;
flush/disposal does not throw merely because a delivery exhausted its retries.
Neither operation disposes the dispatcher or transport.

``PendingBatchCount`` excludes a batch already in flight. ``DeadLetterCount`` counts
retained failed deliveries/batches, so one failed batch contributes one entry. Both queues
remain in memory; process termination loses them and dead letters are not automatically persisted
or exported. Shutdown has no separate timeout/cancellation option: an unresponsive
custom transport can delay completion. The built-in wrapper retains its per-attempt
SMTP timeout.

Calls on one logger are serialized. Avoid sharing the transport with other logger
instances unless it supports concurrent sends. Dispatcher callbacks must not
re-enter the same logger while delivery is in progress.

Retry Ownership and Window Accounting
-------------------------------------

``IRetryingMailDispatcher`` identifies dispatchers that own their complete retry
policy. The built-in ``MailDispatcher`` implements it. Logger.Mail invokes these
dispatchers once per message or batch; a final false result or exception becomes
a dead letter without another logger retry loop. Custom dispatchers without the
capability retain the legacy three-attempt fallback. Retrying custom dispatchers
and decorators should implement the capability to prevent attempt multiplication.

A configured Mailer ``RetryCount`` of three permits at most three transient SMTP
attempts per logical delivery; authentication failures receive one attempt.
Throttling counts successful logical deliveries, including one per batch, rather
than individual SMTP attempts. Failures do not consume this success budget, so it
is not a failure-rate limiter. Window checks, rotation, sends, and counter updates
share one per-logger async lock. Explicit flush/shutdown bypasses the throttle.

Dead-Letter Inspection and Retention
----------------------------------------

**Major-version behavior change:** bounded retention replaces the previous unbounded default.

``MailLogger`` implements ``IMailDeadLetterSource``. The default capacity is 1,000
entries, retaining the newest failed logical deliveries. A constructor overload
accepts a positive ``deadLetterCapacity``. When full, the oldest entry is evicted
and ``DroppedDeadLetterCount`` increases. Logging, timer, and shutdown failures
all use this bound; one failed batch is one entry.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   await using var boundedLogger = new MailLogger(
       dispatcher, mailConfiguration, new LogParser(), deadLetterCapacity: 200);
   await boundedLogger.LogAsync(new LogInfo(LogLevel.Error, "Payments", "Failure"));
   await boundedLogger.DisposeAsync(); // Finish shutdown before retrieving final failures.
   foreach (var entry in boundedLogger.GetDeadLetters())
       Console.WriteLine(entry.Subject);
   while (boundedLogger.TryDequeueDeadLetter(out var entry))
   {
       // Persist/inspect according to your application's failure-handling policy.
   }

``GetDeadLetters`` returns a read-only FIFO snapshot without removal.
``TryDequeueDeadLetter`` atomically removes the oldest entry without resending it;
when empty it returns false with a null out value. Both operations remain available
after disposal. Entry properties include subject, rendered body, original log
information, logged exception, and the last thrown delivery exception (null for
false-only failures). Batches retain their combined body, batch subject, synthetic
log information, and no individual exception objects. Referenced objects are not
deep-cloned even though entry properties and snapshot collections are read-only.

``DeadLetterCount`` means retained entries, not lifetime failures; it decreases on
retrieval and is capped by ``DeadLetterCapacity``. ``DroppedDeadLetterCount`` counts
only capacity evictions. Update monitoring that previously expected an ever-growing
count, and retrieve regularly if failure history must be preserved.

Retention is bounded by entry count, not bytes; bodies, exception graphs, and
caller-held snapshots may still be large. Storage and replay are application
responsibilities. Payloads can include secrets or personal data; apply the same
access and storage controls as for the underlying logs.

.. BEGIN VERSATUL GENERATED PACKAGE QUICKSTART

Canonical package quickstart
----------------------------

Send HTML log events by email through VersaTul.Mailer, with cancellable logging, flush support, and dead-letter inspection.

Install the package in your application with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Logger.Mail

Minimal package example
^^^^^^^^^^^^^^^^^^^^^^^

This compiler-verified example is also used by the packed package README.

.. literalinclude:: ../samples/Packages/VersaTul.Logger.Mail/Program.cs
   :language: csharp
   :caption: VersaTul.Logger.Mail minimal package example

Expected output
^^^^^^^^^^^^^^^

.. literalinclude:: ../samples/Packages/VersaTul.Logger.Mail/ExpectedOutput.txt
   :language: text
   :caption: Expected output

Support
^^^^^^^

Documentation FAQ <https://docsversatul.readthedocs.io/en/latest/faq.html>_.

.. END VERSATUL GENERATED PACKAGE QUICKSTART
