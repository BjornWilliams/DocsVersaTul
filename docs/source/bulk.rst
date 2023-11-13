Data Bulk
==============

Getting Started
----------------
The VersaTul Data Bulk project provides the ability to setup bulk coping functionality for copying data to and from different data sources. 
This project is designed to provide a set of common interfaces as well as implementation that can be used to build database or data source specific copiers.

Installation
------------

To use VersaTul Data Bulk, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Data.Bulk -Version latest

Main Components
----------------
#. ``IBulkCopy`` : Represents functionality for bulk uploading data from data source to another.
#. ``IBulkCopyColumnMapping`` : Defines the mapping between a column in a Bulk Copy instance data source and a column in the instance's destination source.
#. ``CopyDetail`` : Represents the details that will be used by the BulkCopy implementation.
#. ``BulkCopyColumnMapping`` : implementation of the IBulkCopyColumnMapping interface.

Functional Summary
------------------
#. **void IBulkCopy.DoCopy()** : Overloaded method for bulk inserting a given collection of CopyDetail objects.
#. **bool IBulkCopy.IsAllUploaded** : Get a value indicating if all files are inserted successfully.
#. **int IBulkCopy.BatchSize** : Gets or Sets the number of rows in each batch.
#. **bool IBulkCopy.EnableStreaming** : Gets or Sets a value enabling or disabling streaming data from an IDataReader object.
#. **string SourceColumn** : Gets or Sets the string value of the SourceColumn property.
#. **string DestinationColumn** : Gets or Sets the string value of the DestinationColumn property.
#. **int SourceOrdinal** : Gets or Sets the integer value of the SourceOrdinal property, or -1 if the property has not been set.
#. **int DestinationOrdinal** : Gets or Sets the integer value of the DestinationOrdinal property, or -1 if the property has not been set.

Code Examples
-------------

.. code-block:: c#
    :caption: Simple Example of CopyDetail & BulkCopyColumnMapping setup.

    // Bulk Copy people.csv file to database table Persons
    var copyDetail = new CopyDetail(destinationName: "Persons", sourceFilePath: @"path\to\csv\people.csv", new[]
    {
        // This example showcases using the Source Type to Destination Type support in mapping BulkCopyColumnMapping<Person, Person>
        // however this could also be achieved with simple typing the string column names.
        new BulkCopyColumnMapping<Person, Person>(model => model.AccountBalance, model => model.AccountBalance),
        new BulkCopyColumnMapping<Person, Person>(model => model.Age, model => model.Age),
        new BulkCopyColumnMapping<Person, Person>(model => model.BestFriend, model => model.BestFriend),
        new BulkCopyColumnMapping<Person, Person>(model => model.Friends, model => model.Friends),
        new BulkCopyColumnMapping<Person, Person>(model => model.Name, model => model.Name)
    });

    // pulling BulkCopy object from container.
    var copy = appContainer.Resolve<BulkCopy>();

    // Optionally set properties
    copy.BatchSize = 200;
    copy.EnableStreaming = true;

    // perform bulk uploading.. 
    copy.DoCopy(new[] { copyDetail });