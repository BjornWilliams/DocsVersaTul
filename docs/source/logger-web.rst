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
#. ``IWebLogger`` : Represent functionality need to log to an API endpoint.
#. ``ILogWebConfiguration`` : Represents functionality needed to get settings for the Web logger.
#. ``WebLogger`` : Default implementation of the Web Logger interface.
#. ``LogWebConfiguration`` : Default implementation of the Web Logger configuration interface.

Functional Summary
------------------
#. **ILogWebConfiguration.BaseUrl** : Property for getting the Base Url of the API E.G http://domain.com.
#. **ILogWebConfiguration.LogEndPoint** : Property for getting the relative end point to send data to.
#. See :doc:`/logger` project for more details.


Code Examples
-------------
.. code-block:: c#
    :caption: Implementing a Web Logger Example

    using VersaTul.Logger.Web;
    
    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            // Web logger configs
            var configSettings = new ConfigSettings
            {
                { "BaseUrl", "https://domain.com" }
                { "LogEndPoint", "/api/logger" }
            };                  

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
    


Changelog
-------------