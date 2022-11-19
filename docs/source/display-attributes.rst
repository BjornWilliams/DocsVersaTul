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
**Display(Name = "Newname")** : 
**Display(Decimal = 2)** : 
**Display(DateFormattingString = "D")** : 

Code Examples
-------------