Getting Started
===============

This guide is for developers who want a fast first success with VersaTul instead of reading the full package reference up front.

The goal is to get one useful package working in a small, realistic example, then show the next most sensible step.

What VersaTul Gives You
-----------------------

VersaTul is not a single framework. It is a set of focused packages that help with common application concerns such as configuration, data access, file handling, export workflows, logging, and scheduling.

That packaging model matters because it lets you adopt only the parts you need.

Typical ways teams start with VersaTul include:

1. Adding a foundational package such as ``VersaTul.Configurations`` or ``VersaTul.Extensions``.
2. Adding a data package such as ``VersaTul.Data.Sql`` or ``VersaTul.Data.MongoDB``.
3. Combining support packages such as ``VersaTul.Logger`` with one of the concrete logger implementations.

Quickstart Outcome
------------------

In this quickstart you will:

1. Create a small console app.
2. Install ``VersaTul.Configurations``.
3. Load strongly typed settings from a simple key/value source.
4. Verify the configuration values in running code.

If this works, you will have a concrete starting point for adding defaults, data access, logging, or other package families.

Prerequisites
-------------

1. .NET SDK installed.
2. A terminal in an empty or disposable working folder.
3. A basic C# console app is sufficient for this first pass.

Create A Sample App
-------------------

Create a console application:

.. code-block:: console

   dotnet new console -n VersaTulQuickstart
   cd VersaTulQuickstart

Recommended First Path
----------------------

If you are evaluating the libraries for the first time, use this order:

1. Review :doc:`package-selection` to decide which package family fits your use case.
2. Start with one package, not many.
3. Use the package page to install it and follow the basic example.
4. Add related packages only after the first package is working in your application.

Install A Package
-----------------

VersaTul libraries are consumed as separate NuGet packages.

Example using the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Configurations

Example using the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Configurations -Version latest

Paste This Example
------------------

Replace the generated program with the following example:

.. code-block:: csharp

   using VersaTul.Configurations;

   var settings = new ConfigSettings
   {
       { "ConnectionString", "Server=.;Database=Demo;Trusted_Connection=True;" },
       { "TimeoutSeconds", 30 },
       { "ArchiveDirectory", "C:\\Exports" }
   };

   var configuration = new StorageConfiguration(settings);

   Console.WriteLine($"Connection: {configuration.ConnectionString}");
   Console.WriteLine($"Timeout: {configuration.TimeoutSeconds}");
   Console.WriteLine($"Archive: {configuration.ArchivePath}");

   public class StorageConfiguration : Configuration
   {
       public StorageConfiguration(ConfigSettings settings) : base(settings)
       {
       }

       public string ConnectionString => Get<string>();

       public int TimeoutSeconds => GetOrDefault<int>();

       public string ArchivePath => Get<string>("ArchiveDirectory");
   }

Run The App
-----------

.. code-block:: console

   dotnet run

What You Should See
-------------------

You should see output shaped like this:

.. code-block:: text

   Connection: Server=.;Database=Demo;Trusted_Connection=True;
   Timeout: 30
   Archive: C:\Exports

If you see those values, the key VersaTul behavior is already working: your code is reading strongly typed settings from a simple settings store with almost no wiring.

Why This Is A Good First Step
-----------------------------

This quickstart demonstrates several things quickly:

1. VersaTul can be adopted one package at a time.
2. The configuration surface is simple enough to understand in a few minutes.
3. The pattern scales into other packages that rely on explicit settings and reusable configuration models.

Common Mistakes
---------------

1. Using a missing key with ``Get<T>()`` and expecting it to behave like an optional value.
2. Expecting VersaTul to require a full framework bootstrap before a package becomes useful.
3. Pulling in several packages before the first example is working.

How To Choose A First Package
-----------------------------

Use the package family that matches the immediate problem you are solving.

+------------------------------+-----------------------------------------------------------+
| If you need to...            | Start here                                                |
+==============================+===========================================================+
| Read application settings    | ``VersaTul.Configurations``                               |
+------------------------------+-----------------------------------------------------------+
| Bootstrap default settings   | ``VersaTul.Configuration.Defaults``                       |
+------------------------------+-----------------------------------------------------------+
| Add generic helper methods   | ``VersaTul.Extensions`` or ``VersaTul.Utilities``         |
+------------------------------+-----------------------------------------------------------+
| Query relational databases   | ``VersaTul.Data.Sql`` or ``VersaTul.Data.MsSql``          |
+------------------------------+-----------------------------------------------------------+
| Work with MongoDB            | ``VersaTul.Data.MongoDB``                                 |
+------------------------------+-----------------------------------------------------------+
| Use EF Core repositories     | ``VersaTul.Data.EFCore``                                  |
+------------------------------+-----------------------------------------------------------+
| Read CSV or text files       | ``VersaTul.Data.FileReader``                              |
+------------------------------+-----------------------------------------------------------+
| Stream collections to output | ``VersaTul.Collection.Streamers``                         |
+------------------------------+-----------------------------------------------------------+
| Add logging                  | ``VersaTul.Logger`` plus a concrete logger implementation |
+------------------------------+-----------------------------------------------------------+
| Send email                   | ``VersaTul.Mailer``                                       |
+------------------------------+-----------------------------------------------------------+
| Schedule recurring work      | ``VersaTul.Task.Scheduler``                               |
+------------------------------+-----------------------------------------------------------+

Beginner Guidance
-----------------

When starting out:

1. Prefer package pages with simple examples over copying patterns from multiple packages at once.
2. Add dependencies through dependency injection where the package supports it.
3. Keep configuration explicit so you can see what each package requires.
4. Use the related-package sections in each page before adding another package to your project.

What This Documentation Does Not Cover
--------------------------------------

1. Host application projects from the main VersaTul repository.
2. Test projects and test-only setup.
3. One fixed architecture that every project should follow.

What To Read Next
-----------------

1. Read :doc:`package-selection` for a package-by-problem guide with clearer decision help.
2. If this quickstart was useful, continue with :doc:`configuration-defaults` to layer in default settings.
3. Read :doc:`recommended-paths` if you want a starting set based on your application type.
4. If your next need is operational support, jump to :doc:`scenario-guides/logging-setup`.
5. If your next need is data access, jump to :doc:`scenario-guides/sql-data-access`.
6. Use :doc:`package-catalog` only after you know the problem area you want to expand into.