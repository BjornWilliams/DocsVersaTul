Logger
================

Getting Started
----------------
The VersaTul Logger project provides all the common functionality needed by the other logging projects. 
It provides the contractual interface that a logging project must support in order to be consistent across different logging projects.

Installation
------------

To use VersaTul Logger, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Logger -Version latest


Main Components
----------------
1. ``ILogger`` : Represents the functionality provided by a logger.
2. ``ILogParser`` : Represents the parsing functionality to use for parsing logged data. 
3. ``LogInfo`` : Represents information to be sent for logging.

Functional Summary
------------------
1. **void Log(Exception exception)** : Logs the given Exception to the registered loggers. 
2. **void Log(LogInfo logInfo)** : Logs the given logInfo to the registered loggers.
3. **void Log(LogInfo logInfo, Exception exception)** : Logs the given logInfo & Exception to the registered loggers. 
4. **string Parse(Exception exception, ParseFormat parseFormat)** : Parse the given exception and all inner exception into Key/value string format.
5. **string Parse(LogInfo logInfo, ParseFormat parseFormat)** : Parse the given LogInfo into Key/Value string format.

Code Examples
-------------