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

Scheduled Event Example
-----------------------

.. code-block:: csharp

   var hourlyQuarterPast = new ScheduledEvent(EventTime.Hourly, new TimeSpan(0, 15, 0));
   var nextRun = hourlyQuarterPast.NextEvent(DateTime.Now, includeStartTime: true);

Notes
-----

1. ``BaseTimer`` uses a non-autoresetting internal timer and continually queues the next interval itself.
2. ``Storage`` defaults to ``LocalEventStorage`` but can be replaced.
3. The scheduler is a good fit for service-style orchestration, not full workflow persistence.
