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
3. ``ISmtpClient`` : Represents an implemetation that can be used to send SMTP messages.
4. ``MailConfiguration`` : Default implementation of the ``IMailConfiguration`` interface.
5. ``MailDispatcher`` : Default implementation of the ``IMailDispatcher`` interface.
6. ``SmtpClientWrapper`` : Default implementation of the ``ISmtpClient`` interface.

Functional Summary
------------------
1. **bool SendMail(string fromAddress, string toAddress, string subject, string body)** :   
2. **bool SendMail(string fromAddress, string toAddress, string subject, string body, bool isHtml)** : 
3. **bool SendMail(string fromAddress, string toAddress, string subject, string body, bool isHtml, IEnumerable<Attachment> attachments)** : 
4. **void Send(MailMessage mailMessage)** : 


Code Examples
-------------