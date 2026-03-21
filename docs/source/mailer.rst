Mailer
======

Overview
--------

``VersaTul.Mailer`` provides SMTP-based email delivery behind a small abstraction layer.

It supports plain text and HTML messages, multiple attachment styles, and token-based templated mail while keeping SMTP configuration separate from dispatch code.

When To Use This Package
------------------------

Use this package when you want to:

1. Send SMTP email without binding application code directly to ``SmtpClient``.
2. Send HTML or plain-text messages.
3. Attach files using either ``Attachment`` or abstract mail attachment models.
4. Generate outbound mail from a tokenized template.
5. Reuse one dispatcher across notifications, export delivery, and alerting flows.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Mailer

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Mailer -Version latest

Related Packages
----------------

1. :doc:`logger-mail` for email-backed logging.
2. :doc:`streamers` for generating attachment content.
3. :doc:`configuration-defaults` for baseline mailer settings.

Core Types And Concepts
-----------------------

``IMailDispatcher`` and ``MailDispatcher``
   Main delivery abstraction and implementation.

``IMailConfiguration`` and ``MailConfiguration``
   Expose SMTP host, credentials, sender/recipient, attachment size, timeout, and retry settings.

``ISmtpClient`` and ``SmtpClientWrapper``
   Wrapper abstraction around SMTP transport.

Key Capabilities
----------------

1. Send plain text messages.
2. Send HTML messages.
3. Send messages with ``Attachment`` collections.
4. Send messages with abstract ``IMailAttachment`` payloads.
5. Send tokenized template messages through ``SendTemplatedMail()``.

Basic Example
-------------

.. code-block:: csharp

   using VersaTul.Configurations;
   using VersaTul.Mailer;
   using VersaTul.Mailer.Configurations;
   using VersaTul.Mailer.SmtpClients;

   var configSettings = new ConfigSettings
   {
       { "FromAddress", "alerts@domain.com" },
       { "ToAddress", "ops@domain.com" },
       { "SmtpServer", "127.0.0.1" },
       { "SmtpPort", 25 },
       { "SmtpUserName", "smtp-user" },
       { "SmtpPassword", "smtp-password" },
       { "MaxAttachmentSize", 10000000 }
   };

   var configuration = new MailConfiguration(configSettings);
   var smtpClient = new SmtpClientWrapper(configuration);
   var dispatcher = new MailDispatcher(smtpClient);

   dispatcher.SendMail(configuration.FromAddress, configuration.ToAddress, "Subject", "Body", isHtml: false);

Template Example
----------------

.. code-block:: csharp

   dispatcher.SendTemplatedMail(
       configuration.FromAddress,
       configuration.ToAddress,
       "Welcome",
       "<p>Hello {{FirstName}}, your order {{OrderNumber}} is ready.</p>",
       new Dictionary<string, string>
       {
           ["FirstName"] = "Jane",
           ["OrderNumber"] = "ORD-1001"
       });

Notes
-----

1. ``MailConfiguration`` also exposes ``SmtpTimeoutMilliseconds``, ``RetryCount``, and ``RetryDelayMilliseconds``.
2. The package focuses on delivery, not mail-template storage or rendering engines.
3. This package is the transport layer used by :doc:`logger-mail` and mail-based export workflows.
