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
1. ``IMailConfiguration`` : Represents a configuration file that is applicable to the mailing application.
2. ``IMailDispatcher`` : Represents the functionality to send emails messages.
3. ``ISmtpClient`` : Represents an implementation that can be used to send SMTP messages.
4. ``MailConfiguration`` : Default implementation of the ``IMailConfiguration`` interface.
5. ``MailDispatcher`` : Default implementation of the ``IMailDispatcher`` interface.
6. ``SmtpClientWrapper`` : Default implementation of the ``ISmtpClient`` interface.

Functional Summary
------------------
1. **IMailDispatcher.SendMail()** : Overloaded method for sending SMTP e-mails to receiver as Raw text or HTML with or without attachments.
2. **ISmtpClient.Send(MailMessage mailMessage)** : Sends the specified message to an SMTP server for delivery.
3. See :doc:`configuration-defaults` for more configuration settings.


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