Converters
===================

Getting Started
----------------
The VersaTul Object Converters project provides the ability to convert objects into key/value pairs dictionary stores.
For example, converters can be used to convert instance of classes into a dictionary representation of the data from the class.
This package works with the Collection streamers package.

Installation
------------

To use VersaTul Converters, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Object.Converters -Version latest


Main Components
----------------
#. ``IFlattener`` : Describes the functionality needed to successfully convert from a multi-dimensional object to a one-dimensional key/value pair dictionary with flattened keys.
#. ``IObjectProcessor`` : Represent functionality that can convert an object into a dictionary of string keys and object values.
#. ``IPropertyProcessor`` : Describes the functionality needed to successfully process the properties of object instances.
#. ``Flattener`` : The concrete implementation of ``IFlattener``.
#. ``ObjectProcessor`` : The concrete implementation of ``IObjectProcessor``.
#. ``PropertyProcessor`` : The concrete implementation of ``IPropertyProcessor``.

Functional Summary
------------------
#. **IDictionary<string, object> AsDictionary(IDictionary<string, object> source)** : Converts the given dictionary of string, objects with different levels of object depts into one level. Essentially create a dictionary flatter dictionary with keys/values.
#. **string AsString(object source)** : Converts the given object from a multi-dimensional object to one-dimensional string.
#. **IDictionary<string, object> ToDictionary(object source)** : Converts the given object into a dictionary of String keys and value objects.
#. **object Process(PropertyInfo propertyInfo, object propertyValue, Type propertyType)** : Analyze the given property of an object and its value to see if further processing is needed in order to flatten the given object. 
#. **object Process(PropertyInfo propertyInfo, object propertyValue, IDictionary<string, object> dictionary)** : Analyze the given property of an object and its value to see if further processing is needed in order to flatten the given object.  

Code Examples
-------------

.. code-block:: c#
    :caption: Flattening multilevel dictionary.

    class Program
    {
        static void Main(string[] args)
        {
            IDictionary<string, object> innerDictionary = new Dictionary<string, object>()
            {
                { "Age" , 37 },
                { "FirstName", "Bjorn" },
            };

            IDictionary<string, object> source = new Dictionary<string, object>()
            {
               { "Person", innerDictionary }
            };

            var flattener = new Flattener();

            var returnedSource = flattener.AsDictionary(source);

            //keys are now flattened.
            var age = returnedSource["[1] Person.Age"];
            var firstName = returnedSource["[2] Person.FirstName"];
        }       
    }

.. code-block:: c#
    :caption: Flattening a list of intergers.

    class Program
    {
        static void Main(string[] args)
        {
            List<int> integers = new() { 1, 2, 3, 4, 5 };

            var flattener = new Flattener();
            
            //result is now flattened.
            string result = flattener.AsString(integers);

            //outputs: 1||2||3||4||5
        }       
    }

.. code-block:: c#
    :caption: Converting object to dictionary.

    class Program
    {
        static void Main(string[] args)
        {
            var person = new Person
            {
                Age = 37,
                FirstName = "Bjorn",
                ID = 100018,
                LastName = "Williams"
            }

            var processor = new ObjectProcessor();

            var result = processor.ToDictionary(person);

            //accessing age 
            var age = result["Age"];
        }       
    }