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
1. **bool SendMail()** : Overloaded method for sending SMTP e-mails to receiver as Raw text or HTML with or without attachments.
2. **void Send(MailMessage mailMessage)** : Sends the specified message to an SMTP server for delivery.
3. See :doc:`configuration-defaults` for more Mailer configuration settings.


Code Examples
-------------
.. code-block:: c#
    :caption: Setting up Mailer Example
    