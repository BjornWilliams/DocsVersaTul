.. _logger_label:

Logger
================

Getting Started
----------------
The VersaTul Logger project provides all the common functionality used by all VersaTul loggers. 
This project provides the interfaces used in order to keep consistency across all the different logger apps, 
such as FileLogger, MailLogger, and WebLogger.

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
.. code-block:: c#
    :caption: Implementing a Logger Example

    // Create a project specific interface
    public interface IDatabaseLogger : ILogger 
    {
        // project specific methods can be added here...
    }
    
    // Implementing interface
    public class DatabaseLogger: IDatabaseLogger
    {
        private readonly ILogParser logParser;
       
        public DatabaseLogger(ILogParser logParser)
        {
           this.logParser = logParser;
        }
        
        // interface methods...
        public void Log(LogInfo logInfo) => LogAsync(logInfo)
            .GetAwaiter()
            .GetResult();

        public void Log(Exception exception) => LogAsync(exception)
            .GetAwaiter()
            .GetResult();

        public void Log(LogInfo logInfo, Exception exception) => LogAsync(logInfo, exception)
            .GetAwaiter()
            .GetResult();

        public async Task LogAsync(Exception exception) => await LogAsync(new LogInfo(LogLevel.Error, string.Empty, exception.Message), exception);

        public async Task LogAsync(LogInfo logInfo) => await LogAsync(logInfo, null);

        public async Task LogAsync(LogInfo logInfo, Exception exception)
        {
            var message = logParser.Parse(logInfo, exception, ParseFormat.Tab);

            // send message to database here...
        }
    }

    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
           // Registering logger to container
           builder
             .RegisterType<DatabaseLogger>()
             .As<IDatabaseLogger>()
             .As<ILogger>()
             .SingleInstance();
        }
    }
    
    // Usage catching and logging exceptions...
    public abstract class BaseController : Controller
    {
        private readonly ILogger logger;
       
        protected BaseController(ILogger logger)
        {
            this.logger = logger;
        }

        protected IActionResult FaultHandler(Func<IActionResult> codeToExecute)
        {
            try
            {
                return codeToExecute();
            }
            catch (Exception ex)
            {
                logger.Log(ex);

                return BadRequest();
            }
        }
    }