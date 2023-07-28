Logger Mail
====================

Getting Started
----------------
The VersaTul Logger Mail project provides the functionality needed to performing logging to a email address or addresses. 
This project implements the ILogger interface from the VersaTul Logger project.
There is also a dependency on the VersaTul Mailer project, which is used to send emails.

Installation
------------

To use VersaTul Logger Mail, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Logger.Mail -Version latest

Main Components
----------------
#. ``IMailLogger`` : Represent functionality need to log to a email source E.g errors@domain.com.
#. ``MailLogger`` : Default implementation of the Mail Logger interface.

Functional Summary
------------------
#. See :doc:`/logger` project for more details.
#. See :doc:`/mailer` project for more details.

Code Examples
-------------
.. code-block:: c#
    :caption: Implementing a Mail Logger Example

    using VersaTul.Logger.Mail;
    
    // Configure the container using AutoFac Module
    public class AppModule : Module
    {
        protected override void Load(ContainerBuilder builder)
        {
            // Mail logger configs
            var configSettings = new Builder()
                    .AddOrReplace("FromAddress", "noreply@domain.com")
                    .AddOrReplace("ToAddress", "errors@domain.com")
                    .BuildConfig();

            builder.RegisterInstance(configSettings);

           // Registering logger to container
           builder
             .RegisterType<MailLogger>()
             .As<IMailLogger>()
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