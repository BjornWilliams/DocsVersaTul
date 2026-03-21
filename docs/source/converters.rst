Object Converters
=================

Overview
--------

``VersaTul.Object.Converters`` helps you turn object graphs into dictionary-based representations and flattened outputs that are easier to export, inspect, or transform.

This package is particularly useful in reporting, streaming, and metadata-driven formatting workflows.

When To Use This Package
------------------------

Use this package when you want to:

1. Convert an object into a dictionary of property names and values.
2. Flatten nested dictionaries and enumerable structures into a single key/value view.
3. Produce flattened string output from nested values.
4. Respect display metadata while processing object properties for export scenarios.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Object.Converters

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Object.Converters -Version latest

Related Packages
----------------

1. :doc:`streamers` for exporting processed object data.
2. :doc:`display-attributes` for metadata-driven naming, formatting, and ignore rules.
3. :doc:`extensions` for extension methods that build on these converters.

Core Types And Concepts
-----------------------

``IObjectProcessor`` and ``ObjectProcessor``
   Convert an object into a nested ``IDictionary<string, object>`` structure.

``IFlattener`` and ``Flattener``
   Flatten nested structures into either a flat dictionary or a flattened string.

``IPropertyProcessor`` and ``PropertyProcessor``
   Process individual properties with support for nested objects, collections, dictionaries, and display metadata.

``FlattenKeyOptions``
   Controls how flattened keys are formatted.

Key Capabilities
----------------

1. ``ObjectProcessor.ToDictionary()`` serializes an object and rebuilds it as a nested dictionary structure.
2. ``Flattener.AsDictionary()`` flattens nested dictionaries and collections.
3. ``Flattener.AsString()`` turns nested data into a flattened string representation.
4. ``PropertyProcessor`` respects display-analyzer formatting and ignore behavior during traversal.
5. The flattener includes cycle detection so circular references do not recurse forever.

Basic Example
-------------

Convert a simple object into a dictionary and inspect the generated fields.

.. code-block:: csharp

   using VersaTul.Object.Converters;

   var person = new
   {
       Id = 100018,
       FirstName = "Bjorn",
       LastName = "Williams",
       Age = 37
   };

   var processor = new ObjectProcessor();
   var dictionary = processor.ToDictionary(person);

   var firstName = dictionary["FirstName"];
   var age = dictionary["Age"];

Flattening Example
------------------

Use ``Flattener`` when you need a single-level structure for export or diagnostics.

.. code-block:: csharp

   using VersaTul.Object.Converters;

   IDictionary<string, object> source = new Dictionary<string, object>
   {
       {
           "Person",
           new Dictionary<string, object>
           {
               { "Age", 37 },
               { "FirstName", "Bjorn" }
           }
       }
   };

   var flattener = new Flattener();
   var flattened = flattener.AsDictionary(source);

   var age = flattened["[1] Person.Age"];
   var firstName = flattened["[2] Person.FirstName"];

Property Processing And Display Metadata
----------------------------------------

``PropertyProcessor`` is useful when object values need to be formatted or filtered through display metadata before export.

.. code-block:: csharp

   using VersaTul.Display.Attributes;
   using VersaTul.Object.Converters;

   var displayAnalyzer = new DisplayAnalyzer();
   var propertyProcessor = new PropertyProcessor(displayAnalyzer);

   var property = typeof(Person).GetProperty(nameof(Person.Age));
   var person = new Person { Age = 37 };

   var processedValue = propertyProcessor.Process(property, person.Age, person.Age.GetType());

Notes
-----

1. ``ObjectProcessor`` is useful when you want a structured dictionary representation.
2. ``Flattener`` is better when you need a single-level projection for export, tabular output, or logging.
3. This package becomes more valuable when combined with display attributes and collection streamers.