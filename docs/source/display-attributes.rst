Display Attributes
===================

Getting Started
----------------
The VersaTul Display Attributes project provides the ability to provide meta-data to the export engine for outputting collections as files.
This package works in conjunction with the Collection streamers package.
Attributes can be applied to properties of a collection data type.

Installation
------------

To use VersaTul Display Attributes, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Display.Attributes -Version latest


Components
-----------
1. ``IFormatter`` : 
2. ``IDisplayAnalyzer`` : 
3. ``DisplayAttribute`` :
4. ``DateFormatter`` : 
5. ``DecimalFormatter`` : 

Functional Summary
------------------
1. **Display(Name = "Newname")** : Apply to property to change property name on export.
2. **Display(Decimal = 2)** : Apply to floating point properties to round property value on export.
3. **Display(DateFormattingString = "D")** : Apply to DateTime property to format value on export.

Code Examples
-------------

.. code-block:: c#
    :caption: Attribute usage

    internal class Order
    {
        public int OrderId { get; set; }

        [Display(Name = "Shipping")] //Rename to Shipping
        public string ShipVia { get; set; }

        [Display(Decimals = 2)] //Round value to 2 decimal places
        public decimal SubTotal { get; set; }

        public IEnumerable<OrderItem> Items { get; set; }

        [Display(DateFormattingString = "D")] //Format to Date only.
        public DateTime OrderDate { get; set; }

        public Customer Customer { get; set; }

        public string OrderNumber { get; set; }

        public bool IsMailSent { get; set; }
    }