Getting Started
===============

This guide is for users who are new to the VersaTul libraries and want a practical starting point.

What VersaTul Gives You
-----------------------

VersaTul is not a single framework. It is a set of focused packages that help with common application concerns such as configuration, data access, file handling, export workflows, logging, and scheduling.

That packaging model matters because it lets you adopt only the parts you need.

Typical ways teams start with VersaTul include:

1. Adding a foundational package such as ``VersaTul.Configurations`` or ``VersaTul.Extensions``.
2. Adding a data package such as ``VersaTul.Data.Sql`` or ``VersaTul.Data.MongoDB``.
3. Combining support packages such as ``VersaTul.Logger`` with one of the concrete logger implementations.

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

What To Read Next
-----------------

1. Read :doc:`package-selection` for a package-by-problem guide.
2. Read :doc:`package-catalog` for the full package map.
3. Move into the specific package page that matches your first use case.