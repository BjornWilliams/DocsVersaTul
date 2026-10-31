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
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

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

Cancellation, Ownership, and Circuit Concurrency
------------------------------------------------------------

``WebLogger`` implements the additive ``ICancellableWebLogger`` interface. Existing
``IWebLogger`` members remain supported; overloads accept cancellation with log
information, an exception, or both.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   var cancellableLogger = new WebLogger(httpClientFactory, webLogConfiguration, new LogParser());
   using var cancellation = new System.Threading.CancellationTokenSource(TimeSpan.FromSeconds(10));
   await cancellableLogger.LogAsync(
       new LogInfo(LogLevel.Warning, "Imports", "Remote sink latency"), cancellation.Token);

Cancellation covers waiting for the per-instance request gate and HTTP delivery,
including response buffering. Caller cancellation does not count as an endpoint
failure. Timeouts without caller cancellation and unsuccessful HTTP responses do.
Cancellation cannot guarantee the remote endpoint has not accepted the payload.

Requests are serialized per logger, including in the closed state. Circuit checks,
window transitions, and result updates share the gate. After cooldown only one
request probes recovery: success closes the circuit; failure immediately reopens
it for another cooldown. A canceled probe leaves the previous open state and
allows a later probe. Defaults remain three failures and 30 seconds of cooldown.
Different instances have independent circuit state. Cancel waiting callers to
bound their wait behind a slow request; custom handlers must cooperate with
cancellation. Do not re-enter a logger from its own delivery callbacks.

Every call disposes its request/content, response/content, and factory-created
client, including failure/cancellation paths. The factory owns pooled handler
lifetimes. Custom factories must return clients suitable for per-call disposal.
Synchronous Log requires ISynchronousHttpClientFactory.CreateSynchronousClient
and uses native HttpClient.Send. Ordinary IHttpClientFactory implementations remain
supported by LogAsync. Unsupported synchronous factories raise NotSupportedException
before creating a client, parsing or sending; no blocking fallback is used. Both
paths share the request gate, signing/authentication and circuit-breaker state.

Major migration: use LogAsync for async-only handler chains, or implement the new
capability only after every handler supports native synchronous Send with equivalent
authentication and policy behavior. Do not merely wrap an existing async-only
factory: synchronous forwarding can bypass an async-only delegating handler.
The logger owns each returned client, request and response. Single-Exception
overloads reject null with ArgumentNullException instead of NullReferenceException.

Endpoint URI Rules
------------------

``BaseUrl`` must be absolute HTTP(S) without a query or fragment. ``LogEndPoint``
is relative; a single leading slash appends to the base path rather than replacing
it. ``https://host/api`` plus either ``events`` or ``/events`` produces
``https://host/api/events``. Boundary slashes are normalized; ordinary URI escaping
and dot-segment normalization apply. Query parameters belong in the endpoint.
Absolute endpoints, network authorities, backslashes, and fragments are rejected
before client creation with ``ArgumentException``.

Review configurations that relied on concatenated missing/duplicate slashes or
query/fragment-bearing base URLs. Configuration remains trusted input: this is
not an SSRF destination allowlist, and redirects follow the factory handler's
policy. See the signing and replay validation guidance below.

Webhook signatures and replay validation
==================================================

Current sender contract
------------------------------

When ``WebhookSigningSecret`` is nonblank, ``X-Webhook-Signature`` contains 64 lowercase
hexadecimal characters: HMAC-SHA256 over the UTF-8 JSON payload, using the UTF-8
secret text as the key (no Base64 decoding). Blank secrets disable signing.
Verify the exact raw request-body bytes before deserializing; reformatting JSON,
changing whitespace, or re-encoding it changes the signature. Reject missing,
duplicate, malformed, or incorrect signature headers when signing is required.
Decode the hex and compare the 32-byte MAC with a constant-time comparison such as
``CryptographicOperations.FixedTimeEquals``. Bound the request size before buffering.
Use HTTPS, protect/rotate secrets, and avoid logging secrets or authentication headers.

The current sender emits no signed timestamp or nonce. Its body-only signature
provides integrity/authentication for a shared-secret holder, but no replay protection:
a captured body and signature can be sent again. The log event's timestamp is not
a delivery timestamp or a unique request identifier. Adding unsigned timestamp/nonce
headers does not fix this limitation. Receivers requiring replay resistance must use
a separately implemented sender/receiver protocol; no configuration switch enables it
in this package.

Requirements for a versioned replay-resistant protocol
------------------------------------------------------------

The following is integration guidance, not a protocol implemented by WebLogger.
Deploy and test both ends together; do not make existing receivers require new headers
until their senders support them. Select an explicit protocol version and never silently
fall back to body-only verification when the stronger protocol is required.

1. Generate a UTC delivery timestamp and a cryptographically random nonce (at least
   128 bits) for each delivery attempt. Define exact timestamp units/format, nonce
   encoding, header names, and key identifiers. Use a separate stable event ID for
   application deduplication across retries.
2. Authenticate the timestamp, nonce, version, intended destination/audience, and
   exact payload bytes together with HMAC-SHA256. Define unambiguous framing, such
   as length-prefixed fields, including byte encoding and field order. Authenticate
   any key identifier used for key selection. A bare payload MAC plus unsigned
   freshness headers permits an attacker to substitute fresh values.
3. At the receiver, reject missing/duplicate/oversized fields, invalid encodings,
   unknown versions/keys, and invalid MACs. Use constant-time MAC comparison. Accept
   a signed timestamp only inside a documented past-age and future-clock-skew window;
   for example, at most five minutes old and at most 30 seconds ahead. These are
   application policy examples, not package defaults. Monitor clock synchronization.
4. After authentication and freshness checks, atomically reserve the nonce before
   side effects. Scope it to the authenticated sender/key and protocol, and share
   the replay store across receiver instances. An atomic insert-if-absent must allow
   only one of simultaneous duplicate requests to proceed. Retain the reservation
   until the timestamp can no longer be accepted, including allowed clock skew;
   a future timestamp can require longer retention than the nominal past-age window.
5. Bound replay-store capacity without evicting still-valid reservations; fail closed
   if the store is unavailable or full. Preserve reservations across restarts, or
   reject traffic for the remaining acceptance window after losing state. Reserve
   only after successful authentication to limit cache poisoning. Rate-limit abuse.
6. A reservation followed by a processing failure can prevent retry of that same
   request. Define retry responses and use durable event-ID idempotency or transactional
   processing where needed. Fresh attempt nonces alone do not provide exactly-once
   delivery. During key rotation, allow a bounded overlap and retain old-key replay
   records until their acceptance windows expire.

Validate both ends with valid requests, payload/timestamp/nonce tampering, missing or
duplicate headers, stale and future timestamps at window boundaries, concurrent replays
across receiver instances, store exhaustion/outage/restart, key rotation, and a lost
response followed by retry. A repeated valid current-format body still verifies;
receivers must not mistake that for replay resistance.

Native synchronous factory example
----------------------------------

This minimal factory creates a native handler per call. Production factories can
manage pooling while honoring per-client disposal and the complete handler policy.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using System.Net.Http;
   using VersaTul.Logger.Web.Contracts;

   public sealed class NativeLogClientFactory : ISynchronousHttpClientFactory
   {
       public HttpClient CreateClient(string name) => new HttpClient();
       public HttpClient CreateSynchronousClient(string name)
           => new HttpClient(new SocketsHttpHandler());
   }
