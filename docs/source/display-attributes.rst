Display Attributes
==================

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

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Display.Attributes

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Display.Attributes -Version latest

Related Packages
----------------

1. :doc:`streamers` for export generation.
2. :doc:`pipeline-infrastructure` because the built-in formatters run through a formatting pipeline.

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

   var analyzer = new DisplayAnalyzer();

   var property = typeof(Order).GetProperty(nameof(Order.OrderDate));
   var display = analyzer.GetAttribute(property);
   var formatted = analyzer.FormatValue(display, DateTime.UtcNow);

Notes
-----

1. ``DisplayAnalyzer.PropertyNames`` returns resolved export names ordered by sequence and then name.
2. The analyzer caches resolved property metadata internally as names are requested.
3. Custom formatters are the extension point when you need export-specific formatting beyond the built-ins.
