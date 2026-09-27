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

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Logger.Mail -Version latest

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

1. ``DeadLetterCount`` for failed deliveries that exhausted retries.
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
``IAsyncMailDispatcher`` to avoid blocked workers. Synchronous ``Log`` calls remain
blocking compatibility wrappers. Keep the dispatcher and transport alive until
logging tasks complete, and serialize calls sharing one SMTP client.

Current limits: logger retries and dispatcher retries are still separate;
``LogAsync`` has no cancellation-token overload. Throttled calls complete after
queueing, not delivery.

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

   await logger.FlushAsync(); // Attempts every queued batch, bypassing throttling.

Use ``await using`` as in the example, or await ``DisposeAsync`` during shutdown
before disposing the externally owned dispatcher/SMTP transport. Disposal rejects
new log/flush calls with ``ObjectDisposedException``, waits for active delivery,
stops the background loop, and drains remaining batches without the throttle.
Repeated disposal awaits the same task. Failed batches become dead-letter entries;
flush/disposal does not throw merely because a delivery exhausted its retries.
Neither operation disposes the dispatcher or transport.

``PendingBatchCount`` excludes a batch already in flight. ``DeadLetterCount`` counts
exhausted deliveries/batches, so one failed batch contributes one entry. Both queues
remain in memory; process termination loses them and dead letters are not persisted
or exported. Shutdown has no separate timeout/cancellation option: an unresponsive
custom transport can delay completion. The built-in wrapper retains its per-attempt
SMTP timeout.

Calls on one logger are serialized. Avoid sharing the transport with other logger
instances unless it supports concurrent sends. Dispatcher callbacks must not
re-enter the same logger while delivery is in progress.
