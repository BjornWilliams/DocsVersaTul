Data Bulk
=========

Overview
--------

``VersaTul.Data.Bulk`` defines the contracts and common models for bulk-copy operations that move tabular data from one source into another destination.

It is the abstraction layer behind concrete implementations such as the SQL Server bulk-copy package.

When To Use This Package
------------------------

Use this package when you want to:

1. Describe a bulk import in a transport-neutral way.
2. Define reusable source-to-destination column mappings.
3. Work with bulk-copy results and error reporting consistently.
4. Build data-loading workflows that can be backed by a specific implementation such as :doc:`mssql`.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

    dotnet add package VersaTul.Data.Bulk

Or with the Package Manager Console:

.. code-block:: console

    PM> NuGet\Install-Package VersaTul.Data.Bulk -Version latest

Related Packages
----------------

1. :doc:`mssql` for a concrete ``IBulkCopy`` implementation backed by SQL Server.
2. :doc:`file-reader` for producing ``IDataReader`` sources from CSV and text files.
3. :doc:`streamers` and other reader-producing workflows that can feed bulk operations.

Core Types And Concepts
-----------------------

``IBulkCopy``
    Defines synchronous and asynchronous bulk-copy operations plus options such as batch size and streaming.

``CopyDetail``
    Describes a single bulk-copy unit: destination name, source ``IDataReader``, and column mappings.

``IBulkCopyColumnMapping`` and ``BulkCopyColumnMapping``
    Define how source columns map to destination columns by name or ordinal.

``BulkCopyColumnMapping<TSource, TDestination>``
    Strongly typed mapping helper that extracts property names from expressions.

``BulkCopyResult`` and ``CopyResult``
    Capture the overall result and per-item outcomes of a bulk operation.

``BulkCopyProgress``
    Progress payload for async operations that report incremental status.

``BulkCopyException``
    Wrapper exception used when a copy step fails.

Key Capabilities
----------------

1. ``IBulkCopy`` supports one or many ``CopyDetail`` items per operation.
2. Both synchronous and asynchronous APIs are available.
3. Async overloads can report progress with ``BulkCopyProgress``.
4. Mappings can be defined by column name, ordinal, or strongly typed expressions.
5. ``CopyDetail`` validates mappings before execution.

Basic Example
-------------

The abstraction assumes your source data is already available as an ``IDataReader``.

.. code-block:: csharp

    using VersaTul.Data.Bulk;

    var copyDetail = new CopyDetail(
         destinationName: "Persons",
         reader: peopleReader,
         columnMappings: new[]
         {
              new BulkCopyColumnMapping<Person, Person>(model => model.Name, model => model.Name),
              new BulkCopyColumnMapping<Person, Person>(model => model.Age, model => model.Age)
         });

    bulkCopy.BatchSize = 200;
    bulkCopy.EnableStreaming = true;

    var result = bulkCopy.DoCopy(copyDetail);

Async Progress Example
----------------------

.. code-block:: csharp

    var result = await bulkCopy.DoCopyAsync(
         new[] { copyDetail },
         dBConnectionName: "ImportDb",
         progressCallback: progress =>
         {
              Console.WriteLine($"Processed {progress.ProcessedItems} of {progress.TotalItems}");
         });

Mapping Options
---------------

``BulkCopyColumnMapping`` supports multiple styles:

1. Source name to destination name.
2. Source ordinal to destination ordinal.
3. Source ordinal to destination name.
4. Source name to destination ordinal.
5. Strongly typed expression-to-expression mapping.

Notes
-----

1. ``VersaTul.Data.Bulk`` defines the bulk-copy vocabulary; it does not by itself implement a database-specific uploader.
2. The source side is ``IDataReader``-based, which makes the package fit naturally with :doc:`file-reader` and stream-based workflows.
3. Use the concrete implementation from :doc:`mssql` when targeting SQL Server bulk import.


