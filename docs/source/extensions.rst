Extensions
===================

Getting Started
----------------
The VersaTul Extensions project provides a wide variety of methods for manipulating arrays, performing conversions and many other common functionalities.

Installation
------------

To use VersaTul Extensions, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Extensions -Version latest


Main Components
----------------
1. ``ArrayExtensions`` : Static class containing all methods for extending array functionality.
2. ``CommonExtensions`` : Static class containing all methods for extending common functionality.
3. ``ConvertExtensions`` : Static class containing all methods for extending object conversion functionality.
4. ``CurrencyExtensions`` : Static class containing all methods for extending currency manipulation functionality.

Functional Summary
------------------
1. **IEnumerable<T> Pick<T>(this IEnumerable<T> source, int amount)** : Randomly select the given amount of items from a collection.
2. **string ToCamelCase(this string phrase)** : Convert the first letter of the first word to lower case.
3. **T To<T>(this object value)** : Returns an object of the specified type and whose value is equivalent to the specified object.
4. **long ToMicron(this decimal amount)** : Converts the given amount to micros. Multiple the value by one million.

Code Examples
-------------
.. code-block:: c#
    :caption: Randomly Selected Example

    class Program
    {
        static void Main(string[] args)
        {
            var array = new List<string> { "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" };

            // Value will be a new IEnumerable containing 5 randomly selected strings.
            var value = array.Pick(5);
        }
        Console.ReadLine();
    }