Compression
====================

Getting Started
----------------
The VersaTul Compression project enables the ability to compress and decompress streams.
This project was build using the DotNet ``System.IO.Compression`` namespace. 
It can be used to zip a collection of streams into a zip folder.

Installation
------------

To use VersaTul Compression, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Compression -Version latest


Main Components
----------------
1. ``IArchiver`` : Provides functionality to write Zip Stream to Zip Archive stream.
2. ``IZipper`` : Provides functionality to zip Zip Stream into Zip folder.
3. ``Archiver`` : Concrete implementation of the IArchiver interface.
4. ``Zipper`` : Concrete implementation of the IZipper interface.
5. ``ZipStream`` : Represents a class containing the Memory Stream and the Filename to save it as.

Functional Summary
------------------
1. **MemoryStream Zip(ZipStream zipStream)** : Zip the given ZipStream into a zip folder.
2. **MemoryStream Zip(IEnumerable<ZipStream> zipStreams)** : Zips the given collection of ZipStreams into a zip folder.

Code Examples
--------------