Extensions
===================

Getting Started
----------------
The VersaTul Extensions project provides a variety of methods for manipulating arrays, performing conversions and other common functionalities.

Installation
------------

To use VersaTul Extensions, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Extensions -Version latest


Main Components
----------------
#. ``ArrayExtensions`` : Class containing all methods for extending arrays.
#. ``CommonExtensions`` : Class containing all methods for common functionality.
#. ``ConvertExtensions`` : Class containing all methods for extending object conversions.
#. ``CurrencyExtensions`` : Class containing all methods for extending currency manipulations.

Functional Summary
------------------
#. **IEnumerable<T> ArrayExtensions.Pick<T>(this IEnumerable<T> source, int amount)** : Randomly selects the given amount of items from a collection.
#. **string CommonExtensions.ToCamelCase(this string phrase)** : Converts the first letter of the first word to lower case.
#. **T ConvertExtensions.To<T>(this object value)** : Returns an object of the specified type and whose value is equivalent to the specified object.
#. **long CurrencyExtensions.ToMicron(this decimal amount)** : Converts the given amount to micros. It Multiplies the value by one million.

Code Examples
-------------
.. code-block:: c#
    :caption: Random Selection Example

    using VersaTul.Extensions;

    class Program
    {
        static void Main(string[] args)
        {
            var array = new List<string> { "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" };

            // Value will be a new array containing 5 
            // randomly selected strings from the given array.
            var value = array.Pick(5);
        }
        Console.ReadLine();
    }

.. code-block:: c#
    :caption: Different Conversion Examples

    using VersaTul.Extensions;
    
    class Program
    {
        static void Main(string[] args)
        {
            var intVal = "123";

            var newIntVal = intVal.To<int>(); //To Int

            var decimalVal = "123.22";

            var newDecimalVal = decimalVal.To<decimal>(); //To decimal

            // Array Type conversion 
            var list = new List<string> { "1", "2", "3", "4" };

            // convert from string to int
            var newList = list.To<string, int>().ToList(); //To array of int
        }
        Console.ReadLine();
    }    
    


Changelog
-------------

V1.0.8

* Minor fixes
* Dependent package updates

V1.0.7

* Minor fixes
* Dependent package updates

V1.0.6

* Code ported to dotnet core
* Documentation completed