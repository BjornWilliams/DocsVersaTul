Display Attributes
===================

Getting Started
----------------
The VersaTul Display Attributes project enables the ability to provide meta-data to the export engine for outputting collections as files.
This package works with the :doc:`streamers` package.
Attributes can be applied to the properties of a collection data type in order to manipulate the outputted data.

Installation
------------

To use VersaTul Display Attributes, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Display.Attributes -Version latest


Main Components
---------------
#. ``IFormatter`` : Specifies the functionality provided by a Display formatter.
#. ``IDisplayAnalyzer`` : Specifies the functionality provided by a Display analyzer.
#. ``DisplayAttribute`` : Apply to a property in order to provide meta-data to the export engine for outputting data to files.
#. ``DateFormatter`` : Represents the formatter for formatting dates, this uses the standard date and time format specifiers.
#. ``DecimalFormatter`` : Represents the formatter for formatting decimals.

Functional Summary
------------------
#. **DisplayAttribute.Display(Name = "New-Display-Name")** : Apply to property to change property name on export.
#. **DisplayAttribute.Display(Decimal = 2)** : Apply to floating point properties to round property value on export.
#. **DisplayAttribute.Display(DateFormattingString = "D")** : Apply to DateTime properties to format value on export.
#. **object IDisplayAnalyzer.FormatValue()** : Overloaded method for formatting a given property value base on the Display setting.
#. **DisplayAttribute IDisplayAnalyzer.GetAttribute(PropertyInfo propertyInfo)** : Gets the DisplayAttribute value added to a given Property.
#. **string IDisplayAnalyzer.GetName(PropertyInfo propertyInfo)** : Returns the name of the property wither the name of the current member or the overridden name by the Display Attribute.

Code Examples
-------------

.. code-block:: c#
    :caption: Display Attribute Usage
    :emphasize-lines: 48, 51, 56

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