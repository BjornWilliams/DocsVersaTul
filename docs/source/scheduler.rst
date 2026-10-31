Scheduler
=========

Overview
--------

``VersaTul.Task.Scheduler`` provides timer and event primitives for scheduling work on human-friendly intervals.

It is designed for long-running processes such as services, workers, and background jobs where you need explicit control over recurring and one-off execution schedules beyond a simple fixed interval.

When To Use This Package
------------------------

Use this package when you want to:

1. Schedule jobs at second, minute, hourly, daily, weekly, or monthly offsets.
2. Combine multiple schedules into a queue.
3. Restrict schedules to a time window.
4. Run background work through a timer abstraction that tracks missed time through stored state.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Task.Scheduler


Core Types And Concepts
-----------------------

``BaseTimer``
   Core timer abstraction that queues and executes scheduled tasks, records last-run state, and raises error events.

``ScheduleTimer`` and ``ReportTimer``
   Concrete timer implementations for general and report-oriented scheduling.

``ScheduledEvent``
   Repeating schedule built from an ``EventTime`` base and an offset.

``IntervalEvent``
   Fixed interval schedule beginning from an absolute start time.

``SingleEvent``
   One-time event.

``QueuedEvent``
   Collection of schedules treated as one event source.

``BlockEvent``
   Event wrapper that limits execution to a defined activity window.

Key Capabilities
----------------

1. Add scheduled tasks through ``Add()`` or delegate-based overloads.
2. Start and stop timers explicitly.
3. Persist and reuse the last processed time through ``Storage``.
4. Receive errors through the timer ``Error`` event.
5. Compose schedules from multiple event types.

Basic Example
-------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using VersaTul.Task.Scheduler.Events;
   using VersaTul.Task.Scheduler.Timers;

   var timer = new ScheduleTimer();

   timer.Error += (sender, args) =>
   {
       Console.WriteLine(args.Exception.Message);
   };

   timer.Add(
       new IntervalEvent(DateTime.Now.AddSeconds(10), TimeSpan.FromMinutes(2)),
       (Action)(() => Console.WriteLine($"Executed at {DateTime.Now}")));

   timer.Start();

Task-based Handler Contracts
----------------------------

Use ``ScheduledEventAsyncHandler`` for a ``Task``-returning handler or ``ScheduledEventValueTaskHandler`` for a ``ValueTask``-returning handler. Both handlers receive a ``CancellationToken``. ``DelegateMethodCall`` and ``DynamicMethodCall`` implement ``IAsyncMethodCall``; call ``ExecuteAsync`` and await its result so returned Task and ValueTask failures are observable. Their ``IsAsync`` property identifies the Task/ValueTask path; synchronous delegates remain on the existing ``IMethodCall.Execute`` path. TimerTask synchronized execution (SyncronizedEvent = true, the default) now
requires ISynchronousMethodCall and invokes native synchronous work on the caller
thread. Unsupported handlers report NotSupportedException through the existing
isolated Error callback before invocation. DelegateMethodCall and DynamicMethodCall
provide this capability for concrete non-awaitable return declarations. Task,
ValueTask, async-void, object, ValueType and interface-returning handlers are rejected
on this path because they cannot guarantee native synchronous completion.

Major migration: set SyncronizedEvent = false for scheduled async/opaque-return
handlers, or await TimerTask.ExecuteInternalAsync directly. It awaits returned Task
and ValueTask completion and reports failures/cancellation through the supplied
isolated error callback. Custom synchronous IMethodCall implementations must opt into
ISynchronousMethodCall and guarantee native completion without starting hidden
async work. Use Task/ValueTask signatures instead of async void, whose completion
cannot be awaited. Existing IMethodCall.Execute APIs retain their raw return values.
The legacy AddSyncronized spelling still selects the asynchronous scheduling path;
its name and the default SyncronizedEvent value are retained.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   ScheduledEventAsyncHandler handler = (_, _, cancellationToken) =>
       Task.Delay(TimeSpan.FromSeconds(1), cancellationToken);

   var methodCall = new DelegateMethodCall(handler);
   await ((IAsyncMethodCall)methodCall).ExecuteAsync(stoppingToken);

``TimerTask.OverlapPolicy`` controls asynchronous overlap. ``Allow`` starts every invocation and is the default, ``Skip`` drops an invocation while another is active, ``Queue`` runs invocations in FIFO order, and ``CancelPrevious`` requests cancellation of the active invocation before starting the replacement. ``TimerTask.MaxConcurrency`` is zero by default (unbounded); a positive value caps active ``Allow`` invocations and queues excess arrivals in FIFO order. The other policies already limit active work to one invocation. Synchronized tasks wait for each invocation and therefore do not overlap.

The legacy ``IMethodCall.BeginExecute`` overloads remain available for source and binary compatibility but are obsolete. Migrate to ``IAsyncMethodCall.ExecuteAsync(...)``; the legacy members are retained until the next major version.

Scheduler Time Representation
-----------------------------

Scheduler timestamps use an internal UTC ``DateTimeOffset`` representation. Existing ``DateTime`` values are converted at the public boundary: UTC values are preserved, local values are converted through their local offset, and ``DateTimeKind.Unspecified`` values are explicitly treated as UTC. Storage implementations continue to expose the legacy ``DateTime`` contract, but return and persist UTC values for consistent scheduler comparisons. Event arguments and unbound ``DateTime`` parameters also expose UTC values. Use ``SchedulerTime.ConvertToUtc(localTime, timeZone)`` when a wall-clock value comes from a known ``TimeZoneInfo``: valid values are converted to UTC, spring-forward gaps are rejected, and fall-back ambiguities are rejected until the caller chooses an explicit offset. Pass the resulting UTC value to a schedule.

``IntervalEvent`` validates its schedule at construction: intervals and finite counts must be greater than zero, an explicit end must be after the start, and the resulting schedule must remain within the supported ``DateTime`` range.

``CronEvent`` uses a five-field cron dialect, in this order: minute ``0-59``, hour ``0-23``, day-of-month ``1-31``, month ``1-12``, and day-of-week ``0-7``. Fields support ``*`` wildcards, comma-separated values, ascending ranges, and positive ``/step`` values such as ``*/5`` or ``1-10/2``. Seconds, named months, and named weekdays are not supported. Sunday is ``0`` and the alias ``7`` also means Sunday; ranges containing ``7`` are inclusive (``0-7`` matches every day and ``5-7`` matches Friday through Sunday). If both day-of-month and day-of-week are restricted, they use OR semantics: either field may match.

``CronEvent`` has no time-zone setting and evaluates UTC schedule instants. UTC ``DateTime`` inputs stay UTC, local inputs are converted using the machine's local zone, and ``DateTimeKind.Unspecified`` inputs are treated as UTC. Convert a known wall-clock value with ``SchedulerTime.ConvertToUtc(localTime, timeZone)`` before passing it to the scheduler; invalid daylight-saving times and ambiguous repeated times are rejected.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using System;
   using System.Globalization;
   using VersaTul.Task.Scheduler.Events;

   var weekdaysAtNineUtc = new CronEvent("0 9 * * 1-5");
   var nextRunUtc = weekdaysAtNineUtc.NextEvent(
       new DateTime(2026, 10, 26, 8, 59, 0, DateTimeKind.Utc),
       includeStartTime: false);

   Console.WriteLine(nextRunUtc.ToString("O", CultureInfo.InvariantCulture));

Expected output:

.. code-block:: text

   2026-10-26T09:00:00.0000000Z

Cron next-event searches are bounded to five years of minute-by-minute candidates and return ``DateTime.MaxValue`` when no match or later representable time exists. Cron and interval event-list expansion is bounded to 100,000 occurrences; exceeding that limit raises ``InvalidOperationException`` instead of allowing an unbounded catch-up loop. The timer expands scheduled occurrences from its last checkpoint through the current signal time; there is no separate configurable misfire policy that coalesces or drops that interval. ``LocalEventStorage`` is the default and keeps its checkpoint only in memory, so it cannot recover missed events after the process exits. Use durable ``FileEventStorage`` when restart catch-up is required; if its checkpoint is missing or invalid, it starts from the current UTC time rather than replaying older occurrences.

When ``TimerTask.SyncronizedEvent`` is ``true`` (the default), a timer waits for each handler and invocations do not overlap. For asynchronous scheduling with ``SyncronizedEvent = false``, ``OverlapPolicy`` defaults to ``Allow``; ``Skip`` drops arrivals while work is active, ``Queue`` runs them in FIFO order, and ``CancelPrevious`` requests cancellation from the active handler and starts the replacement without waiting for that handler to finish. Cancellation is cooperative, so the handler must observe its token to stop promptly. ``MaxConcurrency`` can cap ``Allow`` and queue excess arrivals. These options control concurrent handler execution, not cron matching or which occurrences are generated.

Built-in events implement ``IEventCollection.AddEvent(..., IList[DateTime])`` for mutable event output. The legacy ``IEvent.AddEvent(..., IEnumerable[DateTime])`` contract remains for compatibility; passing a non-list enumerable to that legacy overload produces a clear ``ArgumentException``, while scheduler execution uses the list-based contract.

Scheduled Event Example
-----------------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   var hourlyQuarterPast = new ScheduledEvent(EventTime.Hourly, new TimeSpan(0, 15, 0));
   var nextRun = hourlyQuarterPast.NextEvent(DateTime.Now, includeStartTime: true);

File-backed Checkpoints
-----------------------

When a file-backed event storage is used, each checkpoint replaces the previous checkpoint value instead of appending another line. The checkpoint file therefore contains one current value and does not grow on every scheduler save. The stored value is UTC serialized with the invariant round-trip (``O``) format. Legacy files are scanned for the last valid timestamp and rewritten in the normalized format. Saves write a temporary file in the checkpoint directory and replace the target atomically where the file system supports it; the documented fallback is an overwrite move. A deterministic sidecar lock prevents concurrent writers from overlapping; a writer that cannot acquire it receives an ``IOException`` identifying the competing scheduler instance. Missing, empty, corrupt, or only partially written files return the ``DateTime.MaxValue`` sentinel and remain unchanged until a successful save; ``FileEventStorage`` uses the current UTC time as its recovery baseline.

Notes
-----

1. ``BaseTimer`` uses a non-autoresetting internal timer and continually queues the next interval itself.
2. ``Storage`` defaults to ``LocalEventStorage`` but can be replaced.
3. The scheduler is a good fit for service-style orchestration, not full workflow persistence.

.. BEGIN VERSATUL GENERATED PACKAGE QUICKSTART

Canonical package quickstart
----------------------------

Schedule and execute tasks at configured times or intervals, with event metadata and overlap policies.

Install the package in your application with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Task.Scheduler

Minimal package example
^^^^^^^^^^^^^^^^^^^^^^^

This compiler-verified example is also used by the packed package README.

.. literalinclude:: ../samples/Packages/VersaTul.Task.Scheduler/Program.cs
   :language: csharp
   :caption: VersaTul.Task.Scheduler minimal package example

Expected output
^^^^^^^^^^^^^^^

.. literalinclude:: ../samples/Packages/VersaTul.Task.Scheduler/ExpectedOutput.txt
   :language: text
   :caption: Expected output

Support
^^^^^^^

Documentation FAQ <https://docsversatul.readthedocs.io/en/latest/faq.html>_.

.. END VERSATUL GENERATED PACKAGE QUICKSTART
