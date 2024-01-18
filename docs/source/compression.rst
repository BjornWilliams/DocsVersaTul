Compression
====================

Getting Started
----------------
The VersaTul Compression project enables the ability to compress and decompress streams.
This project is built around the DotNet ``System.IO.Compression`` classes. 
Using its inbuilt ``ZipStream`` class ``MemoryStreams`` can be quickly compressed into Archive Streams.

Installation
------------

To use VersaTul Compression, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Compression -Version latest


Main Components
----------------
#. ``IArchiver`` : Provides functionality to write ``ZipStream`` to ``ZipArchive`` stream.
#. ``IZipper`` : Provides functionality to zip ``ZipStream`` into zip up ``MemoryStream``.
#. ``Archiver`` : Concrete implementation of the ``IArchiver`` interface.
#. ``Zipper`` : Concrete implementation of the ``IZipper`` interface.
#. ``ZipStream`` : Represents a class containing the ``MemoryStream`` and meta-data to save stream as.

Functional Summary
------------------
#. **MemoryStream IZipper.Zip(ZipStream zipStream)** : Overloaded method for zipping the given ``ZipStream`` into a zipped ``MemoryStream``.
#. **void IArchiver.Archive(ZipArchive zipArchive, ZipStream zipStream)** : Method for writing the entire contents of a memory stream to a zipArchive stream.

Code Examples
--------------

.. code-block:: c#
    :caption: Simple ZipStream Compressing.
    :emphasize-lines: 57

    class Program
    {
        static void Main(string[] args)
        {
            //Contains the ZipArchive to zip given streams.
            IArchiver archiver = new Archiver();

            IZipper zipper = new Zipper(archiver);

            var zipStream = new ZipStream
            {
                ContentType = "text/csv",
                Filename = "Bjorn.csv",
                Stream = GenerateStreamFromString("This is test stream I want to zip up in a folder.")
            }

            //create MemoryStream (archive) to be written out to Storage.
            var archive = zipper.Zip(zipStream);

            //archive can then be written to disk..
        }

        public static Stream GenerateStreamFromString(string s)
        {
            var stream = new MemoryStream();
            var writer = new StreamWriter(stream);
            writer.Write(s);
            writer.Flush();
            stream.Position = 0;
            return stream;
        }
    }



Changelog
-------------

V1.0.8

* Dependent package updates
* Minor fixes

V1.0.7

* Dependent package updates
* Minor fixes

V1.0.6

* Minor fixes

V1.0.5

* Code ported to dotnet core
* Documentaion completed