Display Attributes
===================

Getting Started
----------------
The VersaTul Display Attributes project enables the ability to provide meta-data to the export engine for outputting collections as files.
This package works with the Collection streamers package.
Attributes can be applied to the properties of a collection data type in order to manipulate the outputted data.

Installation
------------

To use VersaTul Display Attributes, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Display.Attributes -Version latest


Components
-----------
1. ``IFormatter`` : Specifies the functionality provided by a Display formatter.
2. ``IDisplayAnalyzer`` : Specifies the functionality provided by a Display analyzer.
3. ``DisplayAttribute`` : Apply to a property in order to provide meta-data to the export engine for outputting data to files.
4. ``DateFormatter`` : Represents the formatter for formatting dates, this uses the standard date and time format specifiers.
5. ``DecimalFormatter`` : Represents the formatter for formatting decimals.

Functional Summary
------------------
1. **Display(Name = "Newname")** : Apply to property to change property name on export.
2. **Display(Decimal = 2)** : Apply to floating point properties to round property value on export.
3. **Display(DateFormattingString = "D")** : Apply to DateTime properties to format value on export.

Code Examples
-------------

.. code-block:: c#
    :caption: Display Attribute Usage
    :emphasize-lines: 45, 48, 53

    class Order
    {
        public int OrderId { get; set; }

        [Display(Name = "Shipping")] //Rename to Shipping
        public string ShipVia { get; set; }

        [Display(Decimals = 2)] //Round value to 2 decimal places
        public decimal SubTotal { get; set; }

        public IEnumerable<OrderItem> Items { get; set; }

        [Display(DateFormattingString = "D")] //Format to Long date pattern.
        public DateTime OrderDate { get; set; }

        public Customer Customer { get; set; }

        public string OrderNumber { get; set; }

        public bool IsMailSent { get; set; }
    }