Logger File
====================

Getting Started
----------------
The VersaTul Logger File project provides the functionality needed to performing logging in a flat file. 
This project implements the ILogger interface from the VersaTul Logger project.

Installation
------------

To use VersaTul Logger File, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Logger.File -Version latest

Main Components
----------------
1. ``IFileLogger`` :  Represent functionality need to log to a flat file source E.g text file.
2. ``IArchiver`` : Represent functionality need to maintain the log file. Archiving files and starting new log files.
3. ``ILogFileConfiguration`` : Represents a configuration file that is applicable to the Logger File application.
4. ``FileLogger`` : Default implementation of the File Logger interface.
5. ``Archiver`` : Default implementation of the Archiver interface.
6. ``LogFileConfiguration`` : Default implementation of the Log File Configuration interface.

Functional Summary
------------------
1. **void PerformArchiving()** : Checks if the log file has reached N size, and creates a new log file and save the current file with time-stamp added to the name.
2. **string GenerateFileName()** : Generates a file name with date time stamp for archiving the log file.
3. **string FileName** : Gets the configured file name.
4. **string FilePath** : Gets the configured file path.
5. **long MaxFileSize** : Gets the configured max file size.
6. See :doc:`/logger` project for more details.


Code Examples
-------------
.. code-block:: c#
    :caption: Implementing a File Logger Example

    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            // File logger configs
            var configSettings = new Builder()
                    .AddOrReplace("MaxFileSize", 10000000)
                    .AddOrReplace("FileName", "app_log")
                    .AddOrReplace("FilePath", "c:\logs\")
                    .BuildConfig();

            builder.RegisterInstance(configSettings);

           // Registering logger to container
           builder
             .RegisterType<FileLogger>()
             .As<IFileLogger>()
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