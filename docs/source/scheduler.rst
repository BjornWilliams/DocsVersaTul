Scheduler
==================

Getting Started
----------------
The VersaTul Task Scheduler project provides functionality to schedule events then listen to and react to those events. 
This is ideal for windows service type applications that may run tasks based on certain time or day. 
Events can be scheduled from seconds, minutes, hours, days and many more combinations.

Installation
------------

To use VersaTul Task Scheduler, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Task.Scheduler -Version latest

Main Components
----------------
#. ``BaseTimer`` : Abstract class that represents a timer that fires on a more human friendly schedule. For example it is easy to set it to fire every day at 6:00PM. It is useful for batch jobs or alarms that might be difficult to schedule with the native DOTNET timers. It is also similar to the DOTNET timer in that it has start and stop methods functioning similarly. The main difference is that the event uses a different delegate and argument since the DOTNET timer argument class is not create-able.
#. ``ScheduleTimer`` : Implements BaseTimer and provides the ability to schedule events.
#. ``ReportTimer`` : Implements BaseTimer and provides the ability to schedule events that are reporting specific. Provides the ability to pass a Report Identifier to run a specified report.
#. ``BlockEvent`` : Represents a class that can filter events so they are only enabled at a certain window of activity. For example if an event should only run every 15 minutes between 6:00 AM and 5:00 PM. Or just on weekdays or weekends.
#. ``IntervalEvent`` : Represents the simple scheduling that DOTNET supports natively. It consists of a start absolute time and an interval that is counted off from the start time.
#. ``QueuedEvent`` : Represents a collection of scheduled events. This is useful for events that occur every 10 minutes or at multiple intervals not covered by the simple scheduled items.
#. ``ScheduledEvent`` : Represents a simple schedule. It can also represent a repeating event that occurs anywhere from every second to once a month. For example ``new ScheduledEvent(Hourly, new TimeSpan(0, 15, 0))`` would represent an event that fired 15 minutes after the hour every hour.
#. ``SingleEvent`` : Represents an event which only fires once.

Functional Summary
------------------
#. **Void BaseTimer.Add()** : An Overloaded method for adding timer tasks.
#. **Void BaseTimer.AddSyncronized(IEvent scheduledItem, Delegate @delegate, params object[] parameters)** : Adds a timer task to the timer to operate asynchronously.
#. **Void BaseTimer.Clear()** : Clears out all scheduled tasks..
#. **Void BaseTimer.Start()** : Begins executing all assigned tasks at the scheduled times..
#. **Void BaseTimer.Stop()** : Stops the execution of all jobs.
#. **Void ScheduleTimer.AddEvent(IEvent scheduledItem)** : Adds an event to be used.
#. **Void BlockEvent.AddEvent(DateTime begin, DateTime end, IEnumerable<DateTime> intervals)** : Adds the time of the events that occur in the given time interval.
#. **DateTime BlockEvent.NextEvent()** : Overloaded method that returns the next run time of the scheduled event.
#. **Void IntervalEvent.AddEvent(DateTime begin, DateTime end, IEnumerable<DateTime> intervals)** : Adds the time of the events that occur in the given time interval.
#. **Void QueuedEvent.Add(IEvent scheduledEvent)** : Adds a Scheduled Item to the queue.
#. **Void QueuedEvent.Clear()** : Clears the list of scheduled times.
#. **Void QueuedEvent.AddEvent(DateTime begin, DateTime end, IEnumerable<DateTime> intervals)** : Adds the time of the events that occur in the given time interval.
#. **Void ScheduledEvent.AddEvent(DateTime begin, DateTime end, IEnumerable<DateTime> intervals)** : Adds the time of the events that occur in the given time interval.
#. **DateTime ScheduledEvent.NextEvent(DateTime time, bool includeStartTime)** : Returns the next run time of the scheduled event.
#. **Void SingleEvent.AddEvent(DateTime begin, DateTime end, IEnumerable<DateTime> intervals)** : Adds the time of the events that occur in the given time interval.
#. **DateTime SingleEvent.NextEvent(DateTime time, bool includeStartTime)** : Returns the next run time of the scheduled item. Optionally excludes the starting time.

Code Examples
-------------
.. code-block:: c#
    :caption: Simple Example Using ScheduleTimer in a BackgroundService.
    :emphasize-lines: 31, 76, 84, 87

    using Autofac;
    using MongoDB.Driver;
    using Technojam.Data.Syncer.Data.EFCore.Models;
    using Technojam.Data.Syncer.Data.EFCore.Repository.Contracts;
    using Technojam.Data.Syncer.Data.Mongod.Repositories.Contracts;
    using Technojam.Data.Syncer.Models;
    using VersaTul.Data.EFCore.Contracts;
    using VersaTul.Task.Scheduler.Events;
    using VersaTul.Task.Scheduler.Timers;

    namespace Technojam.Data.Syncer
    {
        public class Worker : BackgroundService
        {
            private readonly ILogger<Worker> _logger;
            private readonly ScheduleTimer _scheduleTimer;
            private readonly ILifetimeScope _lifetimeScope;

            public Worker(ILogger<Worker> logger, ScheduleTimer scheduleTimer, ILifetimeScope lifetimeScope)
            {
                _logger = logger;
                _scheduleTimer = scheduleTimer;
                _lifetimeScope = lifetimeScope;
            }

            protected override async Task ExecuteAsync(CancellationToken stoppingToken)
            {
                _logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);

                // Need to add the timer code here 
                _scheduleTimer.Elapsed += async (sender, args) =>
                {
                    using var scope = _lifetimeScope.BeginLifetimeScope();
                    IDatumRepository _repository = scope.Resolve<IDatumRepository>();
                    ICategoryRepository _categoryRepository = scope.Resolve<ICategoryRepository>();
                    IUnitOfWork _unitOfWork = scope.Resolve<IUnitOfWork>();

                    _logger.LogInformation("Find any records not synced as yet: {time}", DateTimeOffset.Now);

                    // Find any records not synced as yet 
                    var asyncCursor = await _repository.Collection
                        .Find(Builders<DatumModel>.Filter.Exists(m => m.IsSynced, false))
                        .Limit(1000)
                        .ToCursorAsync(stoppingToken);

                    var datumModels = asyncCursor
                            .ToList(cancellationToken: stoppingToken);

                    _logger.LogInformation("Bulk Insert records at: {time}", DateTimeOffset.Now);

                    // Add the EFCore code to sync 
                    var categories = datumModels.Select(model => new CategoryData
                    {
                        Category = model.Category,
                        CreatedOn = model.CreatedOn,
                        Text = model.Text
                    });

                    await _categoryRepository.AddRangeAsync(categories, stoppingToken);

                    await _unitOfWork.CommitAsync();

                    _logger.LogInformation("Update MongoDb Database at: {time}", DateTimeOffset.Now);

                    // Code to update Mongo DB
                    foreach (var data in datumModels)
                    {
                        data.IsSynced = true;
                    }

                    await _repository.UpdateAsync(datumModels);

                    _logger.LogInformation("Work Completed at: {time}", DateTimeOffset.Now);
                };

                _scheduleTimer.Error += (sender, args) =>
                {
                    _logger.LogError("There was an error working");

                    _logger.LogError(args.Exception.Message, args.Exception.StackTrace);
                };

                // Wire up timer with an IntervalEvent.
                _scheduleTimer.AddEvent(new IntervalEvent(DateTime.Now.AddSeconds(10), new TimeSpan(0, 0, 120)));

                // starting the timer.
                await Task.Run(() => _scheduleTimer.Start(), stoppingToken);

                _logger.LogInformation("Timer Setup at: {time}", DateTimeOffset.Now);
            }
        }
    }


Changelog
-------------