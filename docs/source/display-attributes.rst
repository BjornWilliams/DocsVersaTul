Display Attributes
==================

.. BEGIN VERSATUL GENERATED PACKAGE BADGES

.. image:: https://img.shields.io/nuget/v/VersaTul.Display.Attributes?logo=nuget&label=NuGet%20version
   :target: https://www.nuget.org/packages/VersaTul.Display.Attributes
   :alt: Latest NuGet version

.. image:: https://img.shields.io/nuget/dt/VersaTul.Display.Attributes?logo=nuget&label=NuGet%20downloads
   :target: https://www.nuget.org/packages/VersaTul.Display.Attributes
   :alt: Total NuGet downloads

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://www.nuget.org/packages/VersaTul.Display.Attributes
   :alt: MIT license

.. END VERSATUL GENERATED PACKAGE BADGES

.. BEGIN VERSATUL GENERATED PACKAGE STATUS

**Maintenance:** Community maintained; support is best-effort with no published response SLA.

**Last verified published version:** `1.0.12` on `2026-10-31` (NuGet Gallery).

`NuGet version details <https://www.nuget.org/packages/VersaTul.Display.Attributes/1.0.12>`_.

.. END VERSATUL GENERATED PACKAGE STATUS

Overview
--------

``VersaTul.Display.Attributes`` lets you annotate model properties with export metadata such as display name, ordering, numeric precision, date formatting, and ignore rules.

The package is most useful when paired with :doc:`streamers`, where those annotations influence the shape and formatting of exported output.

When To Use This Package
------------------------

Use this package when you want to:

1. Rename columns during export without renaming your model properties.
2. Control export column order.
3. Round decimal values during output generation.
4. Format date values with a display-specific format string.
5. Exclude properties from exported output.

Package And Change History
--------------------------

`VersaTul.Display.Attributes on NuGet <https://www.nuget.org/packages/VersaTul.Display.Attributes>`_
`VersaTul.Display.Attributes versions and release notes <https://www.nuget.org/packages/VersaTul.Display.Attributes#versions-body-tab>`_

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Display.Attributes


Related Packages
----------------

1. :doc:`streamers` for export generation.
2. :doc:`pipeline-infrastructure` because the built-in formatters run through a formatting pipeline.
3. :doc:`scenario-guides/data-export` for a realistic export workflow.

Core Types And Concepts
-----------------------

``DisplayAttribute``
   Attribute used to control exported name, sequence, decimal precision, date formatting, culture, and ignore behavior.

``IDisplayAnalyzer`` and ``DisplayAnalyzer``
   Read display metadata from reflected properties and format values using registered formatters.

``IFormatter``
   Formatter contract used by the display pipeline.

``DateFormatter`` and ``DecimalFormatter``
   Built-in formatters for date and numeric output.

Key Capabilities
----------------

1. Override the exported property name with ``Name``.
2. Control output order with ``Sequence``.
3. Round numeric values with ``Decimals``.
4. Format ``DateTime`` values with ``DateFormattingString`` and optional ``CultureName``.
5. Exclude members from output with ``Ignore``.
6. Register additional custom formatters through ``DisplayAnalyzer.RegisterFormatter()``.

Attribute Example
-----------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using VersaTul.Display.Attributes;

   public class Order
   {
       public int OrderId { get; set; }

       [Display(Name = "Shipping Method", Sequence = 1)]
       public string ShipVia { get; set; }

       [Display(Decimals = 2, Sequence = 2)]
       public decimal SubTotal { get; set; }

       [Display(DateFormattingString = "D", Sequence = 3)]
       public DateTime OrderDate { get; set; }

       [Display(Ignore = true)]
       public bool InternalFlag { get; set; }
   }

Analyzer Example
----------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   var analyzer = new DisplayAnalyzer();

   var property = typeof(Order).GetProperty(nameof(Order.OrderDate));
   var display = analyzer.GetAttribute(property);
   var formatted = analyzer.FormatValue(display, DateTime.UtcNow);

Member Identity And Concurrent Use
----------------------------------

Metadata is cached by declaring type, module and member token. Inherited views
reuse the declaring member, while constructed generic declaring types remain
distinct. All display settings, including date format and culture, are preserved.
Formatting receives a copy of cached settings so a custom formatter cannot alter
metadata used by later calls.

Use the concrete analyzer's member-aware method for precise formatting:

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   var property = typeof(Order).GetProperty(nameof(Order.SubTotal));
   var formatted = analyzer.FormatPropertyValue(property, 12.345m);

The existing ``FormatValue(value, propertyName)`` method remains valid for a unique
registered member name. If different declaring members share that name, it now
throws ``InvalidOperationException`` instead of silently reusing the first
member's metadata. Unknown names still throw ``KeyNotFoundException``. This is a
Major release migration: use ``FormatPropertyValue(property, value)`` when member
names can be ambiguous. Existing IDisplayAnalyzer implementations do not need a
new member; interface callers can use
``FormatValue(analyzer.GetAttribute(property), value)``.

Metadata caching, heading snapshots and formatter registration support concurrent
use. Each operation captures a stable formatter snapshot, so registration during
execution affects subsequent snapshots. Registered formatter instances may run
concurrently and must synchronize their own mutable state. Built-in formatters
keep per-operation state in PropertyData rather than on the formatter instance.

Notes
-----

1. ``DisplayAnalyzer.PropertyNames`` returns resolved export names ordered by sequence and then name.
2. The analyzer caches resolved property metadata internally as names are requested.
3. Custom formatters are the extension point when you need export-specific formatting beyond the built-ins.

.. BEGIN VERSATUL GENERATED PACKAGE QUICKSTART

Canonical package quickstart
----------------------------

Control exported property names, order, precision, date formats, culture, and ignored fields with attributes and configurable formatters.

Install the package in your application with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Display.Attributes

Minimal package example
^^^^^^^^^^^^^^^^^^^^^^^

This compiler-verified example is also used by the packed package README.

.. literalinclude:: ../samples/Packages/VersaTul.Display.Attributes/Program.cs
   :language: csharp
   :caption: VersaTul.Display.Attributes minimal package example

Expected output
^^^^^^^^^^^^^^^

.. literalinclude:: ../samples/Packages/VersaTul.Display.Attributes/ExpectedOutput.txt
   :language: text
   :caption: Expected output

Support
^^^^^^^

Support and feedback matrix <https://docsversatul.readthedocs.io/en/latest/support.html>_.

.. END VERSATUL GENERATED PACKAGE QUICKSTART

.. include:: _generated_api_links/display-attributes.rst
