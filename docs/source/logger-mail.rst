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

   ILogger logger = new MailLogger(dispatcher, mailConfiguration, new LogParser());

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
queueing, not delivery. A later logging call after the throttle window rotates
triggers batching. There is not yet a background timer or shutdown flush, so a
final partial batch can remain queued. These are separate stabilization Tasks.
