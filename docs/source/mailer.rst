Mailer
======

Overview
--------

``VersaTul.Mailer`` provides SMTP-based email delivery behind a small abstraction layer.

It supports plain text and HTML messages, multiple attachment styles, and token-based templated mail while keeping SMTP configuration separate from dispatch code.

Why Use This Package
--------------------

Use this package when email delivery is becoming a reusable application capability instead of an isolated SMTP call.

Its main value is separating SMTP settings, dispatch concerns, and attachment handling from the calling workflow.

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

Start Here If
-------------

1. You need to send operational notifications, reports, or export files through SMTP.
2. You want calling code to avoid direct dependency on ``SmtpClient``.
3. Message templates or attachment payloads are part of the workflow.

Not The Right First Package If
------------------------------

1. You only need local file logging rather than outbound delivery.
2. You are generating export files but do not yet need to send them.
3. Your team needs a full email-template management system rather than an SMTP delivery layer.

Works Well With
---------------

1. :doc:`streamers` when attachments are generated from collections or readers.
2. :doc:`logger-mail` when operational alerts should be delivered through email.
3. :doc:`configuration` and :doc:`configuration-defaults` when mail settings need to stay explicit and reusable.

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

Expected Result
---------------

When this package is working well:

1. SMTP configuration stays outside the delivery call site,
2. the same dispatcher can send plain text, HTML, and attachment-based messages, and
3. workflows such as reporting, alerts, and notifications can reuse one transport abstraction.

Next Step
---------

1. Read :doc:`streamers` if the next requirement is generating attachment content.
2. Read :doc:`logger-mail` if the next requirement is email-backed logging.
3. Read :doc:`configuration` if you want to centralize the mail settings model more explicitly.

Notes
-----

1. ``MailConfiguration`` also exposes ``SmtpTimeoutMilliseconds``, ``RetryCount``, and ``RetryDelayMilliseconds``.
2. The package focuses on delivery, not mail-template storage or rendering engines.
3. This package is the transport layer used by :doc:`logger-mail` and mail-based export workflows.
