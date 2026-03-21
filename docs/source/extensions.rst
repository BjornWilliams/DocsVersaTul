Extensions
==========

Overview
--------

``VersaTul.Extensions`` provides reusable extension methods for common collection, string, conversion, dictionary, and currency-related operations.

It acts as a convenience layer over other VersaTul packages, especially ``VersaTul.Utilities`` and ``VersaTul.Object.Converters``.

When To Use This Package
------------------------

Use this package when you want to:

1. Convert values and collections with concise extension syntax.
2. Normalize strings for naming or display.
3. Pick random items from a collection.
4. Convert objects into dictionaries or flattened representations.
5. Perform small currency-related transformations.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

    dotnet add package VersaTul.Extensions

Or with the Package Manager Console:

.. code-block:: console

    PM> NuGet\Install-Package VersaTul.Extensions -Version latest

Related Packages
----------------

1. :doc:`utilities` for the underlying conversion and mapping helpers used by this package.
2. :doc:`converters` for dictionary and flattening behaviors surfaced through some extension methods.
3. :doc:`display-attributes` when using ``AsDictionary()`` for metadata-driven exports.

Core Types And Concepts
-----------------------

``ArrayExtensions``
    Includes helpers such as ``GetValue<T>()`` and ``Pick<T>()``.

``CommonExtensions``
    Includes string helpers such as ``ToCamelCase()``, ``ToCamelCaseSpan()``, ``ToTitleCase()``, and ``ToTitleCaseSpan()``.

``ConvertExtensions``
    Includes conversion helpers such as ``To<T>()``, collection conversion overloads, ``AsDictionary()``, and ``AsFlattened()``.

``CurrencyExtensions``
    Includes ``RoundTo()``, ``ToCurrency()``, ``ToMicron()``, and ``FromMicron()``.

Basic Example
-------------

These helpers are designed for direct, low-friction use in application code.

.. code-block:: csharp

    using VersaTul.Extensions;

    var values = new List<string> { "1", "2", "3", "4" };

    var integerValue = "123".To<int>();
    var decimalValue = "123.22".To<decimal>();
    var convertedValues = values.To<string, int>().ToList();

    var picks = values.Pick(2).ToList();
    var camel = "FirstName".ToCamelCase();
    var title = "sample phrase".ToTitleCase();

Dictionary And Flattening Example
---------------------------------

``ConvertExtensions`` can project objects into dictionaries and flatten those dictionaries for export-style scenarios.

.. code-block:: csharp

    using VersaTul.Extensions;

    var person = new Person
    {
         FirstName = "Bjorn",
         LastName = "Williams",
         Age = 37
    };

    var dictionary = person.AsDictionary();
    var flattened = dictionary.AsFlattened();

Currency Example
----------------

.. code-block:: csharp

    using VersaTul.Extensions;

    decimal amount = 123.4567m;

    var rounded = amount.RoundTo(2);
    var currency = amount.ToCurrency();
    var micros = amount.ToMicron();

Notes
-----

1. ``To<T>()`` and related conversion helpers delegate to ``CommonUtility`` under the hood.
2. ``AsDictionary()`` and ``AsFlattened()`` are especially useful with export, reporting, and logging workflows.
3. The span-based string helpers provide alternate implementations for text normalization scenarios.