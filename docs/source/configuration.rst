Configuration
=============

Overview
--------

``VersaTul.Configurations`` provides a lightweight, strongly typed way to work with application settings stored in a simple key/value dictionary.

It is especially useful when you want configuration access that is explicit, easy to test, and simple to pass through your application without taking a dependency on the full .NET configuration stack.

Why Use This Package
--------------------

Use this package when configuration should stay obvious and portable instead of disappearing behind a larger application framework.

It is a strong fit when you want to:

1. keep settings access testable,
2. centralize required and optional configuration values in one type, and
3. reuse the same configuration model across multiple VersaTul packages.

It is less attractive when your team wants every configuration concern to be driven exclusively by the full ASP.NET Core configuration stack and its conventions.

When To Use This Package
------------------------

Use this package when you want to:

1. Wrap application settings in strongly typed configuration classes.
2. Resolve values by property name with minimal boilerplate.
3. Bind a key/value store into a plain object.
4. Share one configuration model across multiple VersaTul packages.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Configurations

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Configurations -Version latest

Related Packages
----------------

1. :doc:`configuration-defaults` for prebuilt default settings.
2. :doc:`contracts` for reusable abstractions used elsewhere in the ecosystem.
3. Data and logging packages that consume configuration values from ``ConfigSettings``.

Start Here If
-------------

1. You want the fastest path from raw settings to a strongly typed configuration class.
2. You want a simple first VersaTul package that can be evaluated in a console app or service.
3. You are preparing to add packages such as SQL access, logging, or mail delivery that need explicit settings.

Not The Right First Package If
------------------------------

1. You are looking for logging, file import, or data access behavior rather than settings access.
2. You already know you only need built-in framework configuration binding and do not need a reusable VersaTul configuration model.

Works Well With
---------------

1. :doc:`configuration-defaults` when you want baseline keys and defaults before applying overrides.
2. :doc:`sql` and :doc:`mssql` when connection metadata needs to stay explicit.
3. :doc:`logger`, :doc:`logger-file`, and :doc:`mailer` when operational packages need shared settings.

Core Types And Concepts
-----------------------

``IConfiguration``
   Defines the main configuration API, including ``Get<T>()``, ``GetOrDefault<T>()``, ``TryGetValue()``, and ``Bind<T>()``.

``IAppConfiguration``
   Extends the base configuration abstraction for application-level configuration types.

``Configuration``
   Abstract base class that implements ``IConfiguration``. You inherit from this type to create your own strongly typed configuration class.

``AppConfiguration``
   Abstract application-oriented configuration base type.

``ConfigSettings``
   A dictionary-based settings store used as the source for configuration lookups.

Key Behaviors
-------------

1. ``Get<T>()`` uses the calling member name by default, so property-based configuration reads are concise.
2. ``GetOrDefault<T>()`` returns the default value for ``T`` when a key is missing.
3. ``TryGetValue()`` lets you inspect presence without throwing.
4. ``Bind<T>()`` maps matching keys onto a plain object with writable public properties.
5. The ``Configuration`` base class supports optional case-insensitive key lookup through its constructor.

Basic Example
-------------

The most common usage pattern is to inherit from ``Configuration`` and expose strongly typed properties.

.. code-block:: csharp

   using VersaTul.Configurations;

   public class StorageConfiguration : Configuration
   {
       public StorageConfiguration(ConfigSettings settings) : base(settings)
       {
       }

       public string ConnectionString => Get<string>();

       public int TimeoutSeconds => GetOrDefault<int>();

       public string ArchivePath => Get<string>("ArchiveDirectory");
   }

   var settings = new ConfigSettings
   {
       { "ConnectionString", "Server=.;Database=Demo;Trusted_Connection=True;" },
       { "TimeoutSeconds", 60 },
       { "ArchiveDirectory", "C:\\Exports" }
   };

   var configuration = new StorageConfiguration(settings);

   var connectionString = configuration.ConnectionString;
   var timeout = configuration.TimeoutSeconds;
   var archivePath = configuration.ArchivePath;

Binding Example
---------------

``Bind<T>()`` is useful when you want to project settings into a plain model instead of exposing them through an inherited configuration class.

.. code-block:: csharp

   using VersaTul.Configurations;

   public class MailOptions
   {
       public string SmtpServer { get; set; }
       public int SmtpPort { get; set; }
       public string FromAddress { get; set; }
   }

   public class MailConfiguration : Configuration
   {
       public MailConfiguration(ConfigSettings settings) : base(settings, useCaseInsensitiveKeys: true)
       {
       }
   }

   var settings = new ConfigSettings
   {
       { "smtpserver", "127.0.0.1" },
       { "smtpport", 25 },
       { "fromaddress", "no-reply@example.com" }
   };

   var configuration = new MailConfiguration(settings);
   var options = configuration.Bind<MailOptions>();

Expected Result
---------------

When this package is working well:

1. required values are obvious because they use ``Get<T>()``,
2. optional values are obvious because they use ``GetOrDefault<T>()``, and
3. downstream packages receive a clear configuration object instead of a loosely structured settings bag.

Next Step
---------

1. Read :doc:`configuration-defaults` if you want reusable defaults layered onto your settings model.
2. Read :doc:`sql` if your next package needs database configuration.
3. Read :doc:`mailer` or :doc:`logger-file` if your next concern is outbound mail or operational logging.

Notes
-----

1. ``Get<T>()`` throws when a key is missing, which is useful for required settings.
2. ``GetOrDefault<T>()`` is better suited to optional values.
3. ``ConfigSettings`` is intentionally simple, so it can be populated from JSON, environment variables, a database, or any custom source.
4. If you need ready-made defaults for VersaTul packages, start with :doc:`configuration-defaults` and then override values as needed.