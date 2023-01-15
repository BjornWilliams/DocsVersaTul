Data Sql
================

Getting Started
----------------
The VersaTul Data Sql project provides the ability to quickly create database access objects, 
usable on any suppporting SQL database. This project is built on top of the System.Data.Common namespace.
It provides the functionality to quickly call stored procedures or plain text sql queries, then map the result into data objects using the provided helper methods.
The project also provides Sql Bulk Copy functionality, which can be use to build insert data into a database.

Installation
------------

To use VersaTul Data Sql, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Data.Sql -Version latest

Main Components
----------------
#. ``IDataSource`` : Represents a composite of the Data role interfaces that provides read and write capabilities.
#. ``IProviderFactory`` : Represents a set of methods for creating instances of a provider's implementation of the data sourece classes.
#. ``IDataConfiguration`` : Represents a set of methods or properties for getting configuration values from setting store.
#. ``IParameter`` : Represents the set of properties and methods that describes a parameter passed into the Sql Command.
#. ``IConnectionInfo`` : Represents a connection string details.
#. ``SqlDbDataSource`` :  Represent a default implementation of the IDataSource interface.
#. ``BaseDataService`` : Provides a starting point for custom data services used in projects. Provides all the basic or general database functionality.
#. ``ConnectionInfo`` : Represents a connection string info.
#. ``Parameter`` : Represents a parameter to a Command and optionally its mapping to DataSet columns.
#. ``ProviderFactory`` : Represents a set of methods for creating instances of a provider's implementation of the data sourece classes.
#. ``DataConfiguration`` : Provides a set of methods or properties for getting configuration values from setting store.
#. ``BulkCopy`` : Represents the functionality needed to efficiently bulk load a SQL Server table with data from another source.

Functional Summary
------------------

Code Examples
-------------