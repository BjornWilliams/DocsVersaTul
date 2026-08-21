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

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Task.Scheduler -Version latest

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

Use ``ScheduledEventAsyncHandler`` for a ``Task``-returning handler or ``ScheduledEventValueTaskHandler`` for a ``ValueTask``-returning handler. Both handlers receive a ``CancellationToken``. ``DelegateMethodCall`` and ``DynamicMethodCall`` implement ``IAsyncMethodCall``; call ``ExecuteAsync`` and await its result so returned Task and ValueTask failures are observable. Their ``IsAsync`` property identifies the Task/ValueTask path; synchronous delegates remain on the existing ``IMethodCall.Execute`` path. When a ``TimerTask`` executes an async method call, synchronized execution waits for completion and unsynchronized execution dispatches it in the background; either mode routes the original failure to the timer ``Error`` callback.

.. code-block:: csharp

   ScheduledEventAsyncHandler handler = (_, _, cancellationToken) =>
       Task.Delay(TimeSpan.FromSeconds(1), cancellationToken);

   var methodCall = new DelegateMethodCall(handler);
   await ((IAsyncMethodCall)methodCall).ExecuteAsync(stoppingToken);

``TimerTask.OverlapPolicy`` controls asynchronous overlap. ``Allow`` starts every invocation and is the default, ``Skip`` drops an invocation while another is active, ``Queue`` runs invocations in FIFO order, and ``CancelPrevious`` requests cancellation of the active invocation before starting the replacement. ``TimerTask.MaxConcurrency`` is zero by default (unbounded); a positive value caps active ``Allow`` invocations and queues excess arrivals in FIFO order. The other policies already limit active work to one invocation. Synchronized tasks wait for each invocation and therefore do not overlap.

The legacy ``IMethodCall.BeginExecute`` overloads remain available for source and binary compatibility but are obsolete. Migrate to ``IAsyncMethodCall.ExecuteAsync(...)``; the legacy members are retained until the next major version.

Scheduler Time Representation
-----------------------------

Scheduler timestamps use an internal UTC ``DateTimeOffset`` representation. Existing ``DateTime`` values are converted at the public boundary: UTC values are preserved, local values are converted through their local offset, and ``DateTimeKind.Unspecified`` values are explicitly treated as UTC. Storage implementations continue to expose the legacy ``DateTime`` contract, but return and persist UTC values for consistent scheduler comparisons. Event arguments and unbound ``DateTime`` parameters also expose UTC values. Use ``SchedulerTime.ConvertToUtc(localTime, timeZone)`` when a wall-clock value comes from a known ``TimeZoneInfo``: valid values are converted to UTC, spring-forward gaps are rejected, and fall-back ambiguities are rejected until the caller chooses an explicit offset. Pass the resulting UTC value to a schedule.

Scheduled Event Example
-----------------------

.. code-block:: csharp

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
