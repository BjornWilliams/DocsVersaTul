Collection Streamers
====================

Getting Started
----------------
The VersaTul Collection Streamers provides functionality that enables developers to quickly convert a collection of objects in memory into a data-reader that can be used for Bulk inserting data into a SQL Database, or be used to generate flat files.
Developers can use the streamers to: 
#. Convert a Collection to a Data-Reader.
#. Convert from a Data-Reader to other file formats such as CSV, TAB or Json.
#. Compress converted data into Zip files.
#. Transport the converted data via mail.
The Streamers project also works with :doc:`display-attributes` which is used to manipulate the properties on the objects in the collection such as formatting the data or renaming the property with a desired display name.

Installation
------------

To use VersaTul Collection Streamers, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Collection.Streamers -Version latest



Main Components
----------------

Functional Summary
------------------

Code Examples
-------------
