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
#. ``ILogger`` : Represents the functionality provided by a logger.
#. ``ILogParser`` : Represents the parsing functionality to use for parsing logged data. 
#. ``LogInfo`` : Represents information to be sent for logging.

Functional Summary
------------------
#. **void ILogger.Log(** : Overloaded method for logging the given Exception or information to the registered loggers.
#. **string ILogParser.Parse()** : Overloaded method for parsing the given exception and all inner exception into Key/value string format.

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