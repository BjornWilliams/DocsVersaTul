Utilities
=========

Overview
--------

``VersaTul.Utilities`` provides common low-level helpers for conversion, null handling, enum parsing, random value generation, property mapping, CSV-safe encoding, and collection batching.

It is one of the base packages that other VersaTul libraries build on directly or indirectly.

When To Use This Package
------------------------

Use this package when you want to:

1. Convert values safely between runtime types.
2. Centralize null and ``DBNull`` handling.
3. Generate random strings.
4. Parse enum names and numeric values consistently.
5. Split collections into batches.
6. Map properties between objects with similar shapes.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

    dotnet add package VersaTul.Utilities


Related Packages
----------------

1. :doc:`extensions` for extension-method wrappers around several of these helpers.
2. Many data and file-oriented packages that rely on conversion and null-filtering behavior.

Core Types And Concepts
-----------------------

``IUtility`` and ``CommonUtility``
    The general-purpose utility surface, including transformation, null filtering, random generation, property-name access, mapping, and CSV encoding.

``INullFiltering``
    Provides null and ``DBNull`` filtering helpers.

``IGenerator``
    Provides random string generation.

``IMapperUtility``
    Supports property mapping between different object types.

``ICollectionUtility<T>`` and ``CollectionUtility<T>``
    Provide collection batching and random sampling helpers.

``IEnumParser<T>`` and ``EnumParser<T>``
    Provide enum parsing, formatting, and ``TryParse`` support.

Key Capabilities
----------------

1. ``Transform<T>()`` and ``Transform(object, Type)`` convert runtime values into target types.
2. ``TryTransform()`` attempts conversions without throwing.
3. ``NullFilter<T>()`` and ``DBNullFilter<T>()`` normalize missing values.
4. ``RandomString()`` generates a random string using a cryptographically secure generator.
5. ``PropertyMap()`` copies values between objects that share property names.
6. ``MakeBatches()`` groups a collection into smaller slices.
7. ``EnumParser<T>`` handles enum-to-string, string-to-enum, int-to-enum, and ``TryParse`` flows.

Basic Example
-------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

    using VersaTul.Utilities;
    using VersaTul.Utilities.Contracts;

    IUtility utility = new CommonUtility();

    var integerValue = utility.Transform<int>("123");
    var decimalValue = utility.Transform<decimal>("123.45", useInvariantCulture: true);

    var missingString = utility.NullFilter<string>(null);
    var csvValue = utility.EncodeCSV("A value, with commas");
    var token = utility.RandomString(16);

Enum And Collection Example
---------------------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

    using VersaTul.Utilities;

    var enumParser = new EnumParser<Color>();
    var green = enumParser.Parse("Green");
    var blue = enumParser.Parse(3);
    var asText = enumParser.ParseToString(Color.Red);

    var collectionUtility = new CollectionUtility<int>();
    var batches = collectionUtility.MakeBatches(new[] { 1, 2, 3, 4, 5, 6 }, 2);

    public enum Color
    {
         None,
         Red,
         Green,
         Blue
    }

Property Mapping Example
------------------------

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

    using VersaTul.Utilities;

    var utility = new CommonUtility();

    var source = new CustomerRecord
    {
         Id = 25,
         FirstName = "Bjorn",
         LastName = "Williams"
    };

    var destination = new CustomerDto();

    utility.PropertyMap(source, destination);

Batches And Random Sampling
---------------------------

``MakeBatches(source, batchSize)`` requires a strictly positive size, even for an
empty source. Invalid sizes throw ``ArgumentOutOfRangeException`` for batchSize
before input enumeration. Positive sizes preserve ordering and the existing
materialized-source behavior, including one-shot inputs and large batch sizes.

``CollectionUtility<T>.RandomSampler(source)`` uses ``Random.Shared``. Its new
concrete overload accepts a ``Random`` instance for deterministic tests. Empty
lists still return default(T); null sources or random instances are rejected.
Injected random instances must support the caller's concurrency pattern. The
existing ICollectionUtility interface is unchanged.

Enum-Only Contract Migration
----------------------------

``EnumParser<T>`` and ``IEnumParser<T>`` now require ``where T : struct, Enum``.
This requires a Major Utilities release. Existing enum methods and parsing behavior
remain available. Non-enum arguments such as int fail compilation or reflective
generic construction. Use numeric conversion helpers for non-enum values.

Generic wrappers and factories must also carry the Enum constraint:

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

    public static IEnumParser<T> CreateParser<T>() where T : struct, Enum
        => new EnumParser<T>();

Import System, VersaTul.Utilities and VersaTul.Utilities.Contracts. Scheduler's
EventTime callers remain valid because EventTime is an enum; dependent-package
minimum versions still require a separate release/dependency review.

.. _scalar-conversion-matrix:

Scalar Conversion Matrix
-------------------------

Generic Transform, runtime-type Transform, Extensions conversions and configuration
binding use the same scalar parsers before falling back to IConvertible.

.. list-table:: Supported target types
   :header-rows: 1

   * - Target
     - Text conversion
     - Nullable support
     - Conversion to string
   * - Boolean, Char, signed/unsigned 8/16/32/64-bit integers, Single, Double, Decimal, DateTime
     - Existing IConvertible rules
     - All value types
     - Existing culture-sensitive rules
   * - Enum
     - Case-insensitive names or numeric text
     - Yes
     - Existing enum text
   * - Guid
     - Guid.Parse formats
     - Yes
     - D format
   * - Uri
     - Relative or absolute URI
     - Reference type
     - OriginalString
   * - TimeSpan
     - Duration using the selected culture
     - Yes
     - c format
   * - DateOnly, TimeOnly
     - Date/time using the selected culture
     - Yes
     - O format
   * - DateTimeOffset
     - Date/time with offset retained
     - Yes
     - O format with offset

Assignable values pass through. Current culture is the default; the Transform
overloads accepting ``useInvariantCulture: true`` select invariant parsing.
Generic null/DBNull input returns default(T); runtime-type conversion returns null.
Binding uses default(T) for a non-nullable value property and null for a nullable
or reference property. TryTransform returns false for unsupported or malformed
conversions without leaking cast exceptions; generic null/default conversion succeeds.
Arbitrary custom parsers are not inferred.

Notes
-----

1. ``Transform<T>()`` also handles enums and nullable targets.
2. ``RandomString()`` uses ``RandomNumberGenerator`` rather than ``Random``.
3. ``MakeBatches()`` is useful for bulk operations and throttled processing.
4. If you primarily want fluent syntax, use :doc:`extensions`, which builds on several of these helpers.
