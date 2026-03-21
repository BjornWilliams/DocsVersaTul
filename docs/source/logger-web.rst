Logger Web
==========

Overview
--------

``VersaTul.Logger.Web`` implements the shared logger contract by POSTing log payloads to an HTTP endpoint.

It is useful when you want centralized logging through an internal API, webhook, or remote collector while keeping application code dependent only on the common ``ILogger`` abstraction.

When To Use This Package
------------------------

Use this package when you want to:

1. Send logs to a remote HTTP endpoint.
2. Emit structured JSON payloads instead of flat text.
3. Add authentication or payload signing headers.
4. Prevent repeated failing calls through a simple circuit breaker.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Logger.Web

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Logger.Web -Version latest

Related Packages
----------------

1. :doc:`logger` for the shared logger abstractions and parser.
2. :doc:`configuration-defaults` for default web-logger settings.

Core Types And Concepts
-----------------------

``IWebLogger`` and ``WebLogger``
   HTTP-backed logger implementation.

``ILogWebConfiguration`` and ``LogWebConfiguration``
   Expose endpoint, authentication, signing, and circuit-breaker settings.

``ILogParser``
   Produces JSON payloads for outbound requests.

Key Capabilities
----------------

1. Sends log data as JSON over HTTP POST.
2. Supports optional custom auth headers and tokens.
3. Supports HMAC-based payload signing through ``WebhookSigningSecret``.
4. Tracks consecutive failures and opens a circuit breaker temporarily when the threshold is exceeded.

Basic Example
-------------

.. code-block:: csharp

   using VersaTul.Logger;
   using VersaTul.Logger.Contracts;
   using VersaTul.Logger.Web;

   ILogger logger = new WebLogger(httpClientFactory, webLogConfiguration, new LogParser());

   await logger.LogAsync(new LogInfo(LogLevel.Warning, "Imports", "Remote sink latency detected"));

Configuration Notes
-------------------

``ILogWebConfiguration`` includes:

1. ``BaseUrl``
2. ``LogEndPoint``
3. ``WebhookAuthHeader``
4. ``WebhookAuthToken``
5. ``WebhookSigningSecret``
6. ``CircuitBreakerFailureThreshold``
7. ``CircuitBreakerCooldownSeconds``

Notes
-----

1. ``WebLogger`` throws when the circuit breaker is open, so callers should decide whether to swallow or surface sink failures.
2. Signing is added through an ``X-Webhook-Signature`` header computed from the JSON payload.
3. This package fits centralized operational logging better than local diagnostics.
