File Import Workflow
====================

This guide shows a practical import path for taking delimited data from disk and preparing it for database upload.

The main value of this workflow is that the packages line up cleanly:

1. ``VersaTul.Data.FileReader`` reads the file into ``IDataReader`` form.
2. ``VersaTul.Data.Bulk`` gives you the transport-neutral bulk-copy contract and mapping model.
3. ``VersaTul.Data.MsSql`` becomes the concrete upload step if SQL Server is the destination.

When To Use This Workflow
-------------------------

Use this workflow when you need to:

1. Import CSV or text files into a relational table.
2. Reuse the same import approach for one file or many files.
3. Keep parsing concerns separate from database upload concerns.

Packages To Install
-------------------

.. code-block:: console

   dotnet add package VersaTul.Data.FileReader
   dotnet add package VersaTul.Data.Bulk
   dotnet add package VersaTul.Data.MsSql

Why These Packages Together
---------------------------

``Data.FileReader`` solves file parsing.

``Data.Bulk`` solves copy-detail and column-mapping structure.

``Data.MsSql`` solves the actual SQL Server bulk upload.

That split is useful because you can reason about input parsing, mapping, and upload as separate concerns.

Step 1: Read The File
---------------------

Start by turning the CSV file into an ``IDataReader``.

.. code-block:: csharp

   using VersaTul.Data.FileReader;

   var options = new FileOptions { HasHeader = true };
   using var reader = fileReader.Read("C:\\imports", "people.csv", options);

   if (reader == null)
   {
       throw new InvalidOperationException("The import file could not be opened.");
   }

At this point the workflow is already in the right shape for bulk upload because the downstream packages operate on ``IDataReader``.

Step 2: Define Column Mappings
------------------------------

Map the incoming columns to the destination table.

.. code-block:: csharp

   using VersaTul.Data.Bulk;

   var copyDetail = new CopyDetail(
       destinationName: "Persons",
       reader: reader,
       columnMappings: new[]
       {
           new BulkCopyColumnMapping<Person, Person>(model => model.Name, model => model.Name),
           new BulkCopyColumnMapping<Person, Person>(model => model.Age, model => model.Age)
       });

The mapping step is where you make schema intent explicit instead of burying it inside a larger import routine.

Step 3: Execute The Upload
--------------------------

If the destination is SQL Server, hand the prepared copy detail to the ``VersaTul.Data.MsSql`` bulk uploader.

.. code-block:: csharp

   using VersaTul.Data.MsSql.Bulk;

   var result = await bulkCopy.DoCopyAsync(
       new[] { copyDetail },
       dBConnectionName: "AdventureWorks2019",
       progressCallback: progress =>
       {
           Console.WriteLine($"Processed {progress.ProcessedItems} items");
       });

What You Should See
-------------------

When this workflow is wired correctly:

1. The file-reader step opens the file without custom parsing code in your service layer.
2. The bulk-copy step validates the mapping shape before upload.
3. The SQL Server upload reports progress and completes as one deliberate import operation.

Why This Workflow Helps Adoption
--------------------------------

This is one of the clearest examples of VersaTul package composition providing real value.

You avoid writing:

1. a custom CSV parser,
2. a custom tabular-to-database mapper, and
3. a custom SQL Server bulk import wrapper.

Common Mistakes
---------------

1. Starting with ``VersaTul.Data.Bulk`` when you still need a file parser.
2. Starting with ``VersaTul.Data.FileReader`` but not planning the upload target.
3. Choosing ``VersaTul.Data.Sql`` instead of ``VersaTul.Data.MsSql`` when SQL Server bulk upload is the real requirement.

Related Package Pages
---------------------

1. :doc:`/file-reader`
2. :doc:`/bulk`
3. :doc:`/mssql`

What To Read Next
-----------------

1. Read :doc:`/file-reader` if you need more detail on file options and directory reads.
2. Read :doc:`/bulk` if you want deeper mapping and result-model detail.
3. Read :doc:`sql-data-access` if your next step is building a reusable relational data-service layer around the import workflow.