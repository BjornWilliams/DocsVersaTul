Configuration Defaults
======================

Overview
--------

``VersaTul.Configuration.Defaults`` provides prebuilt configuration builders for common VersaTul packages.

It is designed to reduce setup time by giving you sensible baseline keys and values that you can extend or override before producing a ``ConfigSettings`` instance.

When To Use This Package
------------------------

Use this package when you want to:

1. Bootstrap a VersaTul package quickly with known configuration keys.
2. Keep default values in one place and override only what is environment-specific.
3. Build configuration dictionaries fluently in code.
4. Standardize configuration setup across multiple services or projects.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Configuration.Defaults

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Configuration.Defaults -Version latest

Related Packages
----------------

1. :doc:`configuration` for consuming the ``ConfigSettings`` values you build here.
2. :doc:`caching`, :doc:`sql`, :doc:`mssql`, :doc:`mongodb`, :doc:`mailer`, and the logger packages that rely on these keys.

Core Types And Concepts
-----------------------

``ConfigurationBuilder``
   Abstract base builder that supports fluent ``AddOrReplace()`` calls and produces ``ConfigSettings``.

``ConfigurationEnvironment``
   Environment enum used to add common environment markers such as development, test, and production.

Namespace-specific ``Builder`` classes
   Each supported package area provides its own builder with package-specific defaults.

Supported Builder Namespaces
----------------------------

1. ``VersaTul.Configuration.Defaults.Caching``
2. ``VersaTul.Configuration.Defaults.EntityFrameworkCore``
3. ``VersaTul.Configuration.Defaults.Logger``
4. ``VersaTul.Configuration.Defaults.Mailer``
5. ``VersaTul.Configuration.Defaults.MongoDB``
6. ``VersaTul.Configuration.Defaults.MsSql``
7. ``VersaTul.Configuration.Defaults.Sql``

Key Builder Features
--------------------

1. ``AddOrReplace(string key, object value)`` updates a single setting.
2. ``AddOrReplace(IEnumerable<KeyValuePair<string, object>> valuePairs)`` updates many settings at once.
3. ``AddOrReplace(IDictionary<string, object> keyValuePairs)`` merges an existing dictionary into the builder.
4. ``AddDevelopmentPreset()``, ``AddTestPreset()``, and ``AddProductionPreset()`` add standard environment markers.
5. ``BuildConfig()`` returns a ``ConfigSettings`` instance.
6. ``BuildSnapshot()`` returns a read-only view of the accumulated configuration.

Basic Example
-------------

This example starts with the MongoDB defaults and overrides the connection string.

.. code-block:: csharp

   using VersaTul.Configuration.Defaults.MongoDB;

   var configSettings = new Builder()
       .AddOrReplace("MongoDb", "mongodb://root:password123@127.0.0.1:27017/DemoDb")
       .BuildConfig();

The MongoDB builder already includes defaults such as:

1. ``MongoDbConnectionName``
2. ``SocketTimeout``
3. ``ConnectTimeout``
4. ``MaxConnectionIdleTime``
5. ``EnabledSslProtocols``

Composed Example
----------------

You can combine package defaults with environment metadata and project-specific overrides.

.. code-block:: csharp

   using VersaTul.Configuration.Defaults;
   using VersaTul.Configuration.Defaults.Sql;

   var builder = new Builder()
       .AddProductionPreset()
       .AddOrReplace("DBCon", "Server=.;Database=MainDb;Trusted_Connection=True;")
       .AddOrReplace("CommandTimeout", 900);

   var settings = builder.BuildConfig();
   var snapshot = builder.BuildSnapshot();

Typical Default Keys
--------------------

Some of the most commonly used defaults include:

1. SQL: ``CommandTimeout`` and ``SqlDbConnectionName``.
2. MS SQL: ``BulkCopyTimeout``.
3. MongoDB: ``MongoDbConnectionName``, ``SocketTimeout``, ``ConnectTimeout``, and ``MaxConnectionIdleTime``.
4. Mailer: ``SmtpServer``, ``SmtpPort``, ``FromAddress``, ``ToAddress``, and ``MaxAttachmentSize``.
5. Logger builders: keys such as file path, file name, endpoint, or base URL depending on the logger implementation.

Notes
-----

1. Start with the closest builder to your target package instead of building settings entirely by hand.
2. Override only the values that differ for your environment or application.
3. Feed the resulting ``ConfigSettings`` directly into your configuration class from :doc:`configuration`.
4. If you need to audit what a builder produced before runtime wiring, use ``BuildSnapshot()``.