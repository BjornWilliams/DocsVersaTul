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

Prerequisites and Tested Versions
---------------------------------

- Install a .NET SDK that supports the target framework. The sample projects target ``net8.0``, ``net9.0``, and ``net10.0``; the documentation workflow validates all three.
- The runnable sample writes files under a unique temporary directory and removes it when finished. It needs no external service or credentials.

The runnable sample's direct package dependencies use these released versions:

.. list-table:: Tested data-export sample packages
   :header-rows: 1

   * - Package
     - Version
     - Role
   * - ``VersaTul.Collection.Streamers``
     - ``1.0.36``
     - CSV streaming and file creation
   * - ``VersaTul.Display.Attributes``
     - ``1.0.12``
     - Export column names, ordering, formatting, and ignored fields
   * - ``VersaTul.Object.Converters``
     - ``1.0.15``
     - Object flattening and display-aware conversion
   * - ``VersaTul.Handler.File``
     - ``1.0.21``
     - File utilities used by the streamer
   * - ``VersaTul.Utilities``
     - ``1.0.16``
     - Shared escaping and formatting utilities

Step 1: Annotate The Export Model
---------------------------------

Use display metadata to control the CSV headings, column order, decimal and date formats, and ignored fields.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

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
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using VersaTul.Collection.Streamers;

   using var csvStreamer = new CsvStreamer(utility, fileUtility, flattener);

   var fileStream = csvStreamer
       .Create(orderRows, "orders-export")
       .GetFileStream();

This is the point where ``Collection.Streamers`` uses the companion packages to turn your object model into exportable output.

Step 3: Save The Export
-----------------------

For large exports, write directly to disk.

.. code-block:: csharp
   :caption: Pseudocode: illustrative fragment, not a copy-paste quickstart.

   using VersaTul.Collection.Streamers.Contracts;

   var filePath = ((IFileWritableStreamer)csvStreamer.Create(orderRows, "orders-export"))
       .WriteToFile("C:\\exports");

Why This Package Combination
----------------------------

``VersaTul.Collection.Streamers`` writes the collection as CSV and owns the output stream. ``VersaTul.Display.Attributes`` supplies the CSV names, order, formats, and exclusion rule. ``VersaTul.Object.Converters`` provides the ``Flattener`` required by the streamer and turns the nested location into a readable field. ``VersaTul.Handler.File`` and ``VersaTul.Utilities`` provide the file and CSV escaping helpers used to construct the sample streamer.

The sample also writes JSON with ``System.Text.Json`` to show a second file format. VersaTul display metadata applies to the CSV output; JSON uses camel-case names and its own ``JsonIgnore`` attribute.

What You Should See
-------------------

When this workflow is working:

1. The output columns reflect display names rather than raw property names.
2. Values such as decimals and dates follow the export formatting rules.
3. Ignored properties do not appear in the final export.

Runnable Sample
---------------

The complete `DataExport project <https://github.com/BjornWilliams/DocsVersaTul/tree/main/docs/samples/DataExport>`_ creates CSV and JSON files from a sample object. Clone the repository and run it from the repository root:

.. code-block:: console

   git clone https://github.com/BjornWilliams/DocsVersaTul.git
   cd DocsVersaTul
   dotnet run --project docs/samples/DataExport/DataExport.csproj --framework net8.0

The project also targets ``net9.0`` and ``net10.0``; substitute either framework in the command to run those targets. The sample source is included below for reference.

The deterministic input is one person object:

.. code-block:: csharp

   new Person
   {
       Name = "Ada",
       CreditLimit = 1250.456m,
       Age = 37,
       RegisteredOn = new DateTime(2024, 1, 15),
       Location = new Location { City = "London" },
       InternalNotes = "Do not include in either export"
   }

.. literalinclude:: ../../samples/DataExport/Program.cs
   :language: csharp
   :caption: Program.cs

The exact expected console output, including both generated-file contents, is:

.. literalinclude:: ../../samples/DataExport/ExpectedOutput.txt
   :language: text
   :caption: Expected output

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
