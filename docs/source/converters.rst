Converters
===================

Getting Started
----------------
The VersaTul Object Converters project provides the ability to convert objects into name value pairs.
For example, converters can be used to convert instance of classes into a dictionary representation of the data from the class.
This package works with the Collection streamers package.

Installation
------------

To use VersaTul Converters, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Object.Converters -Version latest


Main Components
----------------
#. ``IFlattener`` : 
#. ``IObjectProcessor`` : 
#. ``IPropertyProcessor`` : 
#. ``Flattener`` : 
#. ``ObjectProcessor`` : 
#. ``PropertyProcessor`` : 

Functional Summary
------------------
#. **IDictionary<string, object> AsDictionary(IDictionary<string, object> source)** : 
#. **string AsString(object source)** : 
#. **IDictionary<string, object> ToDictionary(object source)** : 
#. **object Process(PropertyInfo propertyInfo, object propertyValue, Type propertyType)** : 
#. **object Process(PropertyInfo propertyInfo, object propertyValue, IDictionary<string, object> dictionary)** : 

Code Examples
-------------