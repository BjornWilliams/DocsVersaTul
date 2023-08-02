Handler File
==================

Getting Started
----------------
The VersaTul Handler File project provides the functionality needed to work with files on hard-disks. 
Most notable functionalities are the creating, reading, and deleting of custom file types found in the project. 
This project, however is simply a wrapper project around the **System.IO.File** namespace and was design to make working with the VersaTul custom FileInfo class much easier.

Installation
------------

To use VersaTul Handler File, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Handler.File -Version latest

Main Components
----------------
#. ``IDirectoryIO`` : Interface used to expose System.IO.File methods pertaining to Directory manipulation.
#. ``IFileHandler`` : Interface used for providing the general File manipulation functionalities.
#. ``IFileIO`` : Interface used to expose System.IO.File methods pertaining to File manipulation.
#. ``IFileUtility`` :  Interface used to provide a File read and Write functionalities.
#. ``FileHandler`` : The concrete implementation of IFileHandler Interface.
#. ``FileUtility`` : The concrete implementation of the IFileUtility Interface.
#. ``IOWrapper`` : The concrete implementation of IDirectoryIO and IFileIO Interfaces.
#. ``BaseInfo`` : An abstract base class that represent the basic information provided by a FileInfo class.
#. ``FileInfo`` : A custom VersaTul class used to represent a file details and its contents.
#. ``CsvFileInfo`` : Class that represent a csv file details and its contents.
#. ``TextFileInfo`` : Class that represent a text file details and its contents.
#. ``ZipFileInfo`` : Class that represent a zip file details and its contents as a stream.
#. ``StreamFileInfo`` : Class that represent a file details and its contents as a stream.
#. ``CustomFileInfo`` : Class used to represent a custom file (maybe a project specific file with its own extension) details and its contents.

Functional Summary
------------------
#. **DirectoryInfo IDirectoryIO.CreateDirectory(string path)** : 
#. **bool IDirectoryIO.Exists(string path)** : 
#. **string[] IDirectoryIO.GetFiles(string path, string searchPattern)** : 
#. **void IFileIO.AppendAllLines(string path, IEnumerable<string> contents)** : 
#. **void IFileIO.Delete(string path)** : 
#. **bool IFileIO.Exists(string path)** : 
#. **string[] IFileIO.ReadAllLines(string path)** : 
#. **void IFileIO.WriteAllLines(string path, IEnumerable<string> contents)** : 
#. **void IFileIO.Write(string filePath, MemoryStream content)** : 
#. **interface.method** : 
#. **interface.method** : 
#. **interface.method** : 
#. **interface.method** : 
#. **interface.method** : 
#. **interface.method** : 
#. **interface.method** : 

Code Examples
-------------