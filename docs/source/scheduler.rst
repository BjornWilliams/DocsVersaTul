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

Code Examples
-------------