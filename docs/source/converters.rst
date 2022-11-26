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
#. ``IFlattener`` : Describes the contract needed to successfully convert from multi-demensional objects to one demension with flattened keys.
#. ``IObjectProcessor`` : Represent functionality that can convert an object into dictionary of string, object.
#. ``IPropertyProcessor`` : Describes the contract needed to successfully process the properties of object instances.
#. ``Flattener`` : Represents a convert for a dictionary of multi-dimensional to one dimension with flattened keys.
#. ``ObjectProcessor`` : Represent functionality that can convert an object into dictionary of string, object.
#. ``PropertyProcessor`` : A class that analyzes a given property and its value and creates a Dictionary or List of the values of the property or simple returns the value of the property.

Functional Summary
------------------
#. **IDictionary<string, object> AsDictionary(IDictionary<string, object> source)** :  Converts the given dictionary of string, objects with differernt level to one level.
#. **string AsString(object source)** : Converts the given object from a multi-demensional object to one demension string.
#. **IDictionary<string, object> ToDictionary(object source)** : Converts the given object into a dictionary of String,Object
#. **object Process(PropertyInfo propertyInfo, object propertyValue, Type propertyType)** : Analyze the given property and its value to see if further processing is needed in order to flatten a given object. 
#. **object Process(PropertyInfo propertyInfo, object propertyValue, IDictionary<string, object> dictionary)** : Analyze the given property and its value to see if further processing is needed in order to flatten a given object. 

Code Examples
-------------

.. code-block:: c#
    :caption: Display Attribute Usage