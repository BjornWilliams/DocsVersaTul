Logger Web
====================

Getting Started
----------------
The VersaTul Logger Web project provides the functionality needed to performing logging to a web address or end point. 
This project implements the ILogger interface from the VersaTul Logger project.

Installation
------------

To use VersaTul Logger Web, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Logger.Web -Version latest

Main Components
----------------
1. ``IWebLogger`` : Represent functionality need to log to an API endpoint.
2. ``ILogWebConfiguration`` : Represents functionality needed to get settings for the Web logger.
3. ``WebLogger`` : Default implementation of the Web Logger interface.
4. ``LogWebConfiguration`` : Default implementation of the Web Logger configuration interface.

Functional Summary
------------------
1. See :doc:`/logger` project for more details.


Code Examples
-------------
.. code-block:: c#
    :caption: Implementing a Web Logger Example

    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            // Mail logger configs
            var configSettings = new Builder()
                    .AddOrReplace("BaseUrl", "https://domain.com")
                    .AddOrReplace("LogEndPoint", "/api/logger")
                    .BuildConfig();

            builder.RegisterInstance(configSettings);

           // Registering logger to container
           builder
             .RegisterType<WebLogger>()
             .As<IWebLogger>()
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