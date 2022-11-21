Compression
====================

Getting Started
----------------
The VersaTul Compression project enables the ability to compress and decompress streams.
This project is build using the DotNet ``System.IO.Compression`` namespace. 
It can be used to zip a collection of streams into a zip stream ``MemoryStream``.

Installation
------------

To use VersaTul Compression, first install it using nuget:

.. code-block:: console
    
    PM> NuGet\Install-Package VersaTul.Compression -Version latest


Main Components
----------------
1. ``IArchiver`` : Provides functionality to write ``ZipStream`` to ``ZipArchive`` stream.
2. ``IZipper`` : Provides functionality to zip ``ZipStream`` into zip up ``MemoryStream``.
3. ``Archiver`` : Concrete implementation of the ``IArchiver`` interface.
4. ``Zipper`` : Concrete implementation of the ``IZipper`` interface.
5. ``ZipStream`` : Represents a class containing the ``MemoryStream`` and meta-data to save stream as.

Functional Summary
------------------
1. **MemoryStream Zip(ZipStream zipStream)** : Zips the given ``ZipStream`` into a zipped ``MemoryStream``.
2. **MemoryStream Zip(IEnumerable<ZipStream> zipStreams)** : Zips the given collection of ``ZipStreams`` into a zippped ``MemoryStream``.

Code Examples
--------------

.. code-block:: c#
    :caption: Simple ZipStream Compressing.
    :emphasize-lines: 56

    class Program
    {
        static void Main(string[] args)
        {
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