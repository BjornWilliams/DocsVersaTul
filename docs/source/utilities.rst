Utilities
==================

Getting Started
----------------
The VersaTul Utilities project provides a variety of commonly used helper methods to help with the rapid development process.

Installation
------------

To use VersaTul Utilities, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Utilities -Version latest



Main Components
----------------
#. ``ICollectionUtility<T>`` : Represent a set of functionality that can operate on collections.
#. ``IEnumParser<T>`` : Represents utility methods that can be use for quickly operating on Enums.
#. ``IGenerator`` : Represents a set of methods that can be used to produces a sequence of numbers or letters that meet certain statistical requirements for randomness.
#. ``INullFiltering`` : Represents utility methods that can be use for operating on fillering ``Null`` values.
#. ``IUtility`` : Represent a set of generic functionality.
#. ``CommonUtility`` : Concrete implementation of the above interfaces.

Functional Summary
------------------
#. **IEnumerable<IEnumerable<T>> ICollectionUtility<T>.MakeBatches(IEnumerable<T> entities, int batchSize)** : Distributes the given collection and arrange the set into sets or groups..
#. **T IEnumParser<T>.Parse(int value)** : Converts the numeric value of one or more enumerated constants to an equivalent enumerated object..
#. **T IEnumParser<T>.Parse(string value)** : Converts the string representation of the name or numeric value of one or more enumerated constants to an equivalent enumerated object.
#. **int IEnumParser<T>.Parse(T value)** : Returns a integer of the specified type and whose value is equivalent to the specified enumType..
#. **string IEnumParser<T>.ParseToString(T value)** : Returns a string of the specified type and whose value is equivalent to the specified enumType..
#. **string IGenerator.RandomString(int length, string allowedChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");** : Returns a non-negative random string for the given length for the allowed characters.
#. **T INullFiltering.DBNullFilter<T>(object value)** : Checks for DBNull value then returns an object of a specified type whose value is equivalent to a specified object..
#. **T INullFiltering.NullFilter<T>(object value)** : Checks for Null value then returns an object of a specified type whose value is equivalent to a specified object.
#. **T INullFiltering.NullOrEmptyFilter<T>(string value)** : Checks for Null or and Empty string then returns an object of a specified type whose value is equivalent to a specified object.

Code Examples
-------------
.. code-block:: c#
    :caption: Random Generator Example

    using VersaTul.Utilities;
    using VersaTul.Utilities.Contracts;

    IGenerator generator = new CommonUtility();

    // variable length strings
    Console.WriteLine(generator.RandomString(10));
    Console.WriteLine(generator.RandomString(20));
    Console.WriteLine(generator.RandomString(40));
    Console.WriteLine(generator.RandomString(5));
    Console.WriteLine(generator.RandomString(3));
    Console.WriteLine(generator.RandomString(6));
    Console.WriteLine(generator.RandomString(80));

.. code-block:: c#
    :caption: Null Filtering Examples

    using VersaTul.Utilities;
    using VersaTul.Utilities.Contracts;

    INullFiltering nullFiltering = new CommonUtility();

    Console.WriteLine(nullFiltering.NullFilter<int>(1)); //output 1 
    Console.WriteLine(nullFiltering.NullFilter<string>("This is my string")); //output "This is my string"


    Console.WriteLine(nullFiltering.NullFilter<int>(null)); // output 0
    Console.WriteLine(nullFiltering.NullFilter<string>(null)); // output empty


.. code-block:: c#
    :caption: Enum Parser Examples

    using VersaTul.Utilities;
    using VersaTul.Utilities.Contracts;   

    IEnumParser<Color> enumParser = new EnumParser<Color>();

    Console.WriteLine(enumParser.Parse(Color.Red)); //output value 1
    Console.WriteLine(enumParser.ParseToString(Color.Red)); //output string "Red"
    Console.WriteLine(enumParser.Parse("Green")); //output Color.Green
    Console.WriteLine(enumParser.Parse(3)); //output Color.Blue
    Console.WriteLine(enumParser.Parse("Green") == Color.Green); //output true
    Console.WriteLine(enumParser.Parse(3) == Color.Blue); //output  true
    
    public enum Color
    {
        None, Red, Green, Blue
    } 