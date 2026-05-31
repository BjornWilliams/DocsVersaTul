Data Export Workflow
====================

This guide shows how to turn in-memory objects into clean export files with intentional column names, ordering, and formatting.

The main package combination is:

1. ``VersaTul.Collection.Streamers`` for creating the export stream.
2. ``VersaTul.Display.Attributes`` for naming, ordering, and formatting the output.
3. ``VersaTul.Object.Converters`` for flattening and preparing object data for export-friendly processing.

When To Use This Workflow
-------------------------

Use this workflow when you need to:

1. Export collections to CSV, JSON, or tab-delimited output.
2. Control the shape of exported columns without renaming your model properties.
3. Keep export formatting decisions near the model instead of scattering them through file-writing code.

Packages To Install
-------------------

.. code-block:: console

   dotnet add package VersaTul.Collection.Streamers
   dotnet add package VersaTul.Display.Attributes
   dotnet add package VersaTul.Object.Converters

Step 1: Annotate The Export Model
---------------------------------

Use display metadata to control how the export appears.

.. code-block:: csharp

   using VersaTul.Display.Attributes;

   public class OrderExportRow
   {
       [Display(Name = "Order Id", Sequence = 1)]
       public int OrderId { get; set; }

       [Display(Name = "Customer", Sequence = 2)]
       public string CustomerName { get; set; }

       [Display(Name = "Order Total", Decimals = 2, Sequence = 3)]
       public decimal Total { get; set; }

       [Display(DateFormattingString = "yyyy-MM-dd", Sequence = 4)]
       public DateTime OrderedOn { get; set; }

       [Display(Ignore = true)]
       public string InternalNotes { get; set; }
   }

Step 2: Create The Stream
-------------------------

Create a streamer for the target format.

.. code-block:: csharp

   using VersaTul.Collection.Streamers;

   var csvStreamer = new CsvStreamer(utility, fileUtility, flattener);

   using var fileStream = csvStreamer
       .Create(orderRows, "orders-export")
       .GetFileStream();

This is the point where ``Collection.Streamers`` uses the companion packages to turn your object model into exportable output.

Step 3: Save The Export
-----------------------

For large exports, write directly to disk.

.. code-block:: csharp

   using VersaTul.Collection.Streamers.Contracts;

   var filePath = ((IFileWritableStreamer)csvStreamer.Create(orderRows, "orders-export"))
       .WriteToFile("C:\\exports");

Why The Companion Packages Matter
---------------------------------

``Display.Attributes`` lets you control the final output contract.

``Object.Converters`` helps flatten nested values and respects display-driven behavior during processing.

``Collection.Streamers`` provides the reusable export engine.

Together, they give you a path from domain object to export file without hand-writing CSV headers, formatting logic, and flattening rules.

What You Should See
-------------------

When this workflow is working:

1. The output columns reflect display names rather than raw property names.
2. Values such as decimals and dates follow the export formatting rules.
3. Ignored properties do not appear in the final export.

Common Mistakes
---------------

1. Using ``Collection.Streamers`` alone when the export also needs friendly column names and formatting.
2. Encoding formatting rules in ad hoc exporter code instead of display metadata.
3. Forgetting that direct-to-disk writing is often the better choice for large files.

Related Package Pages
---------------------

1. :doc:`/streamers`
2. :doc:`/display-attributes`
3. :doc:`/converters`

What To Read Next
-----------------

1. Read :doc:`/streamers` for format and file-writing options.
2. Read :doc:`/display-attributes` for metadata and custom formatter details.
3. Read :doc:`/converters` if your export input contains nested objects or collections that must be flattened first.