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
#. ``IFileLogger`` :  Represent functionality need to log to a flat file source E.g text file.
#. ``IArchiver`` : Represent functionality need to maintain the log file. Archiving files and starting new log files.
#. ``ILogFileConfiguration`` : Represents a configuration file that is applicable to the Logger File application.
#. ``FileLogger`` : Default implementation of the File Logger interface.
#. ``Archiver`` : Default implementation of the Archiver interface.
#. ``LogFileConfiguration`` : Default implementation of the Log File Configuration interface.

Functional Summary
------------------
#. **void IArchiver.PerformArchiving()** : Checks if the log file has reached N size, and creates a new log file and save the current file with time-stamp added to the name.
#. **string IArchiver.GenerateFileName()** : Generates a file name with date time stamp for archiving the log file.
#. **string ILogFileConfiguration.FileName** : Property to get the configured file name.
#. **string ILogFileConfiguration.FilePath** :  Property to get the configured file path.
#. **long ILogFileConfiguration.MaxFileSize** :  Property to get the configured max file size.
#. See :doc:`/logger` project for more details.


Code Examples
-------------
.. code-block:: c#
    :caption: Implementing a File Logger Example

    using VersaTul.Logger.File;
    
    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            // File logger configs
            var configSettings = new Builder()
                    .AddOrReplace("MaxFileSize", 10000000)
                    .AddOrReplace("LogFileName", "app_log")
                    .AddOrReplace("FilePath", "c:\logs\")
                    .BuildConfig();

            builder.RegisterInstance(configSettings);

            // Registering logger to container
            builder.RegisterType<FileLogger>().As<IFileLogger>().As<ILogger>().SingleInstance();
            builder.RegisterType<LogParser>().As<ILogParser>().SingleInstance();
            builder.RegisterType<LogFileConfiguration>().As<ILogFileConfiguration>().SingleInstance();
            builder.RegisterType<Archiver>().As<IArchiver>().SingleInstance();

            builder.RegisterType<DirectoryWrapper>().As<IFileWrapper>().As<IDirectoryWrapper>().SingleInstance();
            builder.RegisterType<FileUtility>().As<IFileUtility>().As<IFileHandler>().SingleInstance();
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
    


Changelog
-------------