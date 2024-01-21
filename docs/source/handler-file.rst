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
#. ``IDirectoryWrapper`` : Interface used to expose **System.IO.File** methods pertaining to Directory manipulation.
#. ``IFileHandler`` : Interface used for providing the general File manipulation functionalities.
#. ``IFileWrapper`` : Interface used to expose **System.IO.File** methods pertaining to File manipulation.
#. ``IFileUtility`` :  Interface used to provide File and Directory read and Write functionalities. Iherits the ``IFileHandler`` interface. 
#. ``FileHandler`` : An abstract class that implements the ``IFileHandler`` Interface.
#. ``FileUtility`` : The concrete implementation of the ``IFileUtility`` Interface.
#. ``DirectoryWrapper`` : The concrete implementation of ``IDirectoryWrapper`` and ``IFileWrapper`` Interfaces.
#. ``BaseInfo`` : An abstract base class that represent the basic information provided by a FileInfo class.
#. ``FileInfo`` : A custom VersaTul class used to represent a file details and its contents.
#. ``CsvFileInfo`` : Class that represent a csv file details and its contents.
#. ``TextFileInfo`` : Class that represent a text file details and its contents.
#. ``ZipFileInfo`` : Class that represent a zip file details and its contents as a stream.
#. ``StreamFileInfo`` : Class that represent a file details and its contents as a stream.
#. ``CustomFileInfo`` : Class used to represent a custom file (maybe a project specific file with its own extension) details and its contents.

Functional Summary
------------------
#. **DirectoryInfo IDirectoryWrapper.CreateDirectory(string path)** : Creates all directories and subdirectories in the specified path unless they already exist.
#. **bool IDirectoryWrapper.Exists(string path)** : Determines whether the given path refers to an existing directory on disk.
#. **string[] IDirectoryWrapper.GetFiles(string path, string searchPattern)** : Returns the names of files (including their paths) that match the specified search pattern in the specified directory.
#. **void IFileWrapper.AppendAllLines(string path, IEnumerable<string> contents)** : Appends lines to a file, and then closes the file. If the specified file does not exist, this method creates a file, writes the specified lines to the file, and then closes the file.
#. **void IFileWrapper.Delete(string path)** : Deletes the specified file.
#. **bool IFileWrapper.Exists(string path)** : Determines whether the specified file exists.
#. **string[] IFileWrapper.ReadAllLines(string path)** : Opens a text file, reads all lines of the file into a string array, and then closes the file.
#. **void IFileWrapper.WriteAllLines(string path, IEnumerable<string> contents)** : Creates a new file, write the specified string array to the file, and then closes the file.
#. **void IFileWrapper.Write(string filePath, MemoryStream content)** : Writes the given memory stream to physical file on disk at the specified path.
#. **FileResult IFileUtility.ReadAllLines(string path)** : Opens a text file, reads all lines of the file, and then closes the file.
#. **void IFileUtility.SaveOrUpdate(FileInfo file)** : Appends lines to a file, and then closes the file. If the specified file does not exist, this method creates a file, writes the specified lines to the file, and then closes the file.
#. **void IFileUtility.Save(StreamFileInfo file)** : Writes the given stream to a file. If the specified file does not exist, this method creates the file, writes the specified stream to the file, and then closes the file.
#. **string IFileHandler.GetFileName(string path)** : Returns the Filename only from a given file path.
#. **string IFileHandler.GetFileNameWithOutExtension(string path)** : Returns the Filename only from a given file path with the file extension removed.
#. **void IFileHandler.RemoveFile(string sourceFile)** : Deletes the given file from the hard disc.
#. **string IFileHandler.GetExtension(string fileName)** : Returns the extension of the given file without the (dot) notation.
#. **bool IFileHandler.CheckFileExtensionMatch(string fileName, string extension)** : Checks if the given filename and file extension are the same.
#. **IEnumerable<string> IFileHandler.FindFilesWithExtension(string path, string extension)** : Returns the names of files (including their paths) that match the specified extension in the specified directory.
#. **void IFileHandler.CreateDirectoryIfNotExists(string path)** : Determines whether the given path refers to an existing directory on disk and if not creates all the directories in a specified path.
#. **IEnumerable<string> IFileHandler.FindFiles()** : Overloaded method that returns the names of files (including their paths) that match the specified search pattern in the specified directory or subdirectories.
#. **string IFileHandler.EnsureExtension(string fileName, string extension)** : Checks the give fileName contains the given extension, if not then the fileName is updated to match.
#. **void IFileHandler.ReadLine(string path, Action<string> action)** : Opens the given file and reads the content line by line as string passed into the given action.

Code Examples
-------------
.. code-block:: c#
    :caption: File Utility Save Or Update Example

    using VersaTul.Handler.File.Contracts;
    using VersaTul.Handler.File.Types;
    using VersaTul.Utilities.Contracts;

    class Program
    {
        static void Main(string[] args)
        {
            // Create instances 
            var directoryWrapper = new DirectoryWrapper();
            var fileUtility = new FileUtility(directoryWrapper, directoryWrapper);

            // Text File Info to save 
            var textFileData = "Large amount of text to save to file";
            var fileData = new TextFileInfo("c:\some\path\on\disk","data", textFileData);

            //Save or Update 
            fileUtility.SaveOrUpdate(fileData);
        }
        Console.ReadLine();
    }

.. code-block:: c#
    :caption: File Utility Read data Example

    using VersaTul.Handler.File.Contracts;
    using VersaTul.Handler.File.Types;
    using VersaTul.Utilities.Contracts;

    class Program
    {
        static void Main(string[] args)
        {
            // Create instances 
            var directoryWrapper = new DirectoryWrapper();
            var fileUtility = new FileUtility(directoryWrapper, directoryWrapper);

            // file to read 
            var fullFilePath = "c:\some\path\filename.txt";

            // Open and read data from file.
            FileResult data = fileUtility.ReadAllLines(fullFilePath);

            if (data.IsExists)
            {
                Print("Here is your file data");
                Print("=========================");
                data.Content.ToList().ForEach(val => Print(val));
            }
            else
            {
                Print($"No file @:'{fullFilePath}'");
            }
        }
        Console.ReadLine();
    }

.. code-block:: c#
    :caption: File Utility Remove Example

    using VersaTul.Handler.File.Contracts;
    using VersaTul.Handler.File.Types;
    using VersaTul.Utilities.Contracts;

    class Program
    {
        static void Main(string[] args)
        {
            // Create instances 
            var directoryWrapper = new DirectoryWrapper();
            var fileUtility = new FileUtility(directoryWrapper, directoryWrapper);

            // file to read 
            var fullFilePath = "c:\some\path\filename.txt";

            // delete file
            fileUtility.RemoveFile(fullFilePath);
        }
        Console.ReadLine();
    }

.. code-block:: c#
    :caption: File Utility Save Or Update IoC Example

    using VersaTul.Handler.File.Contracts;
    using VersaTul.Handler.File.Types;
    using VersaTul.Utilities.Contracts;

    public class AppModule : Module
    {
        // Setup AutoFac container
        protected override void Load(ContainerBuilder builder)
        {
            builder.RegisterType<CommonUtility>().As<IUtility>();

            builder.RegisterType<DirectoryWrapper>().As<IFileWrapper>().As<IDirectoryWrapper>().SingleInstance();
            builder.RegisterType<FileUtility>().As<IFileHandler>().As<IFileUtility>().SingleInstance(); 
        }
    }

    public class FileManager
    {
        // injecting container for simplicity
        public void Execute(AppContainer appContainer)
        { 
            fileUtility = appContainer.Resolve<FileUtility>();

            // Text File Info to save 
            var textFileData = "Large amount of text to save to file";
            var fileData = new TextFileInfo("c:\some\path\on\disk","data", textFileData);

            //Save or Update 
            fileUtility.SaveOrUpdate(fileData);
        }
    }



Changelog
-------------

V1.0.12

* File manipulation improvements 
* Streamline interfaces 
* Minor fixes 
* Dependent package updates

V1.0.11

* Minor fixes

V1.0.10

* Interface refactoring
* Added more custom user file types
* Minor fixes
* Dependent package updates

V1.0.9

* Minor fixes
* Dependent package updates

V1.0.8

* Code ported to dotnet core
* Documentation completed