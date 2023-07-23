Data MsSql
==============

Getting Started
----------------
The VersaTul Data MsSql project provides the ability to quickly create database access objects, usable on Microsoft SQL Server databases. 
This project is built on top of a combination of System.Data.Common & System.Data.SqlClient namespaces.
These are used to provide the functionality to quickly call stored procedures or plain text sql queries, and map the result into data objects using the provided helper methods. 
The project also provides MsSql Bulk Copy functionality, which can be use to bulk insert data into a MsSQL Server databases.

Installation
------------

To use VersaTul Data MsSql, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Data.MsSql -Version latest


Main Components
----------------
#. ``ISqlDataSource`` : Represent funcationality to get connected to a MsSQL Database and perform CRUD operations.
#. ``ISqlParameter`` : Represents a parameter to a SqlCommand object, and optionally, its mapping to DataSet columns; and is implemented by .NET Framework data providers that access data sources.
#. ``SqlDataSource`` : Concrete implementation of ISqlDataSource interface that represent funcationality to get connected to a MsSQL Database and perform CRUD operations.
#. ``SqlParameter`` : Concrete implementation of ISqlParameter interface that represent funcationality to get connected to a MsSQL Database and perform CRUD operations.

Functional Summary
------------------

Code Examples
-------------