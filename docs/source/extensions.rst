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
    Includes conversion helpers such as ``To<T>()``, collection conversion overloads, ``AsDictionary()``, ``AsDictionaries()``, and ``AsFlattened()``.

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

Collection Dictionaries And Migration
-------------------------------------

``AsDictionary()`` accepts a single non-null object. All enumerable sources,
including empty and primitive collections, throw ``NotSupportedException`` with
guidance to use ``AsDictionaries()``. The single-object method retains its
``class, new()`` generic constraint and its property-processing behavior.

For a collection of reference-type object rows, use ``AsDictionaries()``. It
enumerates the source once and eagerly returns a read-only list of dictionaries
in source order. Each dictionary remains mutable. Repeated reads of the returned
list do not read the source again. The collection method has a ``class``
constraint, so it also supports anonymous rows.

.. code-block:: csharp

    using VersaTul.Extensions;

    var people = new[]
    {
        new { Name = "Ada", Age = 37 },
        new { Name = "Grace", Age = 42 }
    };

    var rows = people.AsDictionaries();
    var firstName = rows[0]["Name"]; // "Ada"

An empty source returns an empty list. A null source throws
``ArgumentNullException``; a null element throws ``ArgumentException``. An element
that is itself enumerable throws ``NotSupportedException``. Primitive sequences
are not object rows; use the scalar conversion methods for them.

Both methods use each object's runtime type with default property flags
``DeclaredOnly | Public | Instance``. Pass ``BindingFlags.Public |
BindingFlags.Instance`` to include inherited properties. Nested property values
retain the existing object processor behavior.

This is a major-release migration: replace collection calls such as
``people.AsDictionary()`` with ``people.AsDictionaries()`` and consume one
dictionary per row. Previously, empty and primitive collections returned an empty
dictionary while ordinary object collections could fail during reflection.
Collection input is now rejected consistently. A null single-object source now
throws ``ArgumentNullException`` rather than an accidental null-reference failure.

Random Selection
----------------

``Pick(amount)`` uses ``Random.Shared``. Null input and negative amounts are
rejected; amounts above the source count are capped. A zero amount does not
enumerate the source. Other selections materialize the source once without
modifying it. Positions are selected without replacement; duplicate input values
can still appear in the result.

Use ``source.Pick(amount, new Random(seed))`` for repeatable tests. An injected
random instance must support the caller's concurrency pattern.

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
