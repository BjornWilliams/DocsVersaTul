Mailer
================

Getting Started
----------------
The VersaTul Mailer project provides the functionality to send emails messages. 
This project uses the SMTP protocol to transmit e-mail to a mail receiver.

Installation
------------

To use VersaTul Mailer, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Mailer -Version latest


Main Components
----------------
#. ``IMailConfiguration`` : Represents a configuration file that is applicable to the mailing application.
#. ``IMailDispatcher`` : Represents the functionality to send emails messages.
#. ``ISmtpClient`` : Represents an implementation that can be used to send SMTP messages.
#. ``MailConfiguration`` : Default implementation of the ``IMailConfiguration`` interface.
#. ``MailDispatcher`` : Default implementation of the ``IMailDispatcher`` interface.
#. ``SmtpClientWrapper`` : Default implementation of the ``ISmtpClient`` interface.

Functional Summary
------------------
#. **bool IMailDispatcher.SendMail()** : Overloaded method for sending SMTP e-mails to receiver as Raw text or HTML with or without attachments.
#. **void ISmtpClient.Send(MailMessage mailMessage)** : Sends the specified message to an SMTP server for delivery.
#. See :doc:`configuration-defaults` for more configuration settings.


Code Examples
-------------
.. code-block:: c#
    :caption: Setting up Mailer Example
        
    using VersaTul.Configurations;
    using VersaTul.Mailer;
    using VersaTul.Mailer.Configurations;
    using VersaTul.Mailer.SmtpClients;

    namespace VersaTulMailer
    {
        public class Program
        {
            static void Main(string[] args)
            {
                // Setup mailer configuration without the use of default builder
                var configSettings = new ConfigSettings()
                {
                    { "FromAddress", "sally@customerservice.com" },
                    { "ToAddress", "mygoodcustomer@domain.com" },
                    { "SmtpServer", "120.0.0.1" },
                    { "SmtpPort", 25 },
                    { "SmtpUserName", "bjorn@versatul.com" },
                    { "SmtpPassword", "Some super secret password" },
                    { "MaxAttachmentSize", 10000000 }
                };

                // Setup needed class instances
                var configuration = new MailConfiguration(configSettings);
                var smtpClient = new SmtpClientWrapper(configuration);
                var mailDispatcher = new MailDispatcher(smtpClient);
                
                // Send email here..
                mailDispatcher.SendMail(configuration.FromAddress, configuration.ToAddress, "your subject line", "your mail body here");
            }
        }
    }


Changelog
-------------