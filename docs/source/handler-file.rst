Handler File
============

Overview
--------

``VersaTul.Handler.File`` wraps common file-system operations and adds typed file models for working with text, CSV, custom extensions, zip content, and raw streams.

The package is useful when you want file operations behind interfaces for easier testing and when higher-level packages need to persist typed file content rather than manually coordinate paths, extensions, and stream writes.

When To Use This Package
------------------------

Use this package when you want to:

1. Read or write files through abstractions instead of calling ``System.IO`` directly.
2. Save typed file content such as text, CSV, custom files, or zip streams.
3. Use native async I/O for common file operations.
4. Reuse path, extension, and directory helpers across the codebase.
5. Support export workflows from :doc:`streamers` and archive workflows from :doc:`compression`.

Installation
------------

Install the package with the .NET CLI:

.. code-block:: console

   dotnet add package VersaTul.Handler.File

Or with the Package Manager Console:

.. code-block:: console

   PM> NuGet\Install-Package VersaTul.Handler.File -Version latest

Related Packages
----------------

1. :doc:`streamers` for export generation that can be saved to disk.
2. :doc:`compression` for zip-based file content.
3. :doc:`file-reader` for the inverse workflow of turning files back into ``IDataReader`` instances.

Core Types And Concepts
-----------------------

``IFileHandler``
   Combines file and directory wrappers plus helper operations such as extension handling, file discovery, and line-by-line reading.

``IFileUtility`` and ``FileUtility``
   Higher-level file service for reading all content, saving typed files, and native async I/O.

``IDirectoryWrapper`` and ``IFileWrapper``
   Thin abstractions over file-system APIs used by the higher-level handlers.

``FileResult``
   Result model returned by reads, including existence and blank-file flags.

``FileInfo`` and typed variants
   File models such as ``TextFileInfo``, ``CsvFileInfo``, ``CustomFileInfo``, ``StreamFileInfo``, and ``ZipFileInfo``.

Key Capabilities
----------------

1. ``ReadAll()`` and ``ReadAllAsync()`` read text files into a ``FileResult``.
2. ``SaveOrUpdate()`` and ``SaveOrUpdateAsync()`` append or create text-based files.
3. ``Save()`` and ``SaveAsync()`` persist stream-based files.
4. Path and extension helpers simplify file naming and discovery.
5. Directory creation is handled automatically before writes.

Save Text Example
-----------------

.. code-block:: csharp

   using VersaTul.Handler.File;
   using VersaTul.Handler.File.Types;

   var directoryWrapper = new DirectoryWrapper();
   var fileUtility = new FileUtility(directoryWrapper, directoryWrapper);

   var file = new TextFileInfo("C:\\exports", "report", "Large amount of text to save");
   fileUtility.SaveOrUpdate(file);

Read Example
------------

.. code-block:: csharp

   var result = fileUtility.ReadAll("C:\\exports\\report.txt");

   if (result.IsExists)
   {
       foreach (var line in result.Content)
       {
           Console.WriteLine(line);
       }
   }

Save Stream Example
-------------------

.. code-block:: csharp

   using var memoryStream = new MemoryStream(System.Text.Encoding.UTF8.GetBytes("hello"));

   var streamFile = new ZipFileInfo("C:\\exports", "archive", memoryStream);
   await fileUtility.SaveAsync(streamFile);

Notes
-----

1. ``FileUtility`` uses a lock to serialize writes from the same process.
2. The async methods use the IAsyncFileWrapper capability for native asynchronous payload I/O.
3. The typed file models are the main value-add over direct ``System.IO`` usage.

Stream ownership
----------------

Save and SaveAsync leave StreamFileInfo.Content open by default and write the entire
MemoryStream, preserving its position. Set ``LeaveOpen = false`` to transfer disposal
responsibility, including write failures. DirectoryWrapper.Write always leaves the
caller stream open. Custom IFileWrapper implementations must honor this contract.
This is a Major ownership change: dispose streams explicitly or opt into disposal.
Do not share or mutate a stream while a write is in progress.

Native asynchronous operations
------------------------------

FileUtility async methods require ``IAsyncFileWrapper``; DirectoryWrapper supplies
native File/FileStream async I/O with cancellation. Synchronous-only custom wrappers
remain usable for sync calls; async calls throw NotSupportedException. Implement the
additive capability when migrating (Major change). Missing files/directories return
an absent FileResult; permission and other errors propagate. Directory creation/open
are synchronous metadata operations; payload I/O is asynchronous. Cancellation of
non-atomic writes can leave partial content. Ownership applies on cancellation too.

Coordinated and atomic writes
-----------------------------

FileUtility writes coordinate by normalized absolute path across instances, using
case-insensitive comparison on Windows and ordinal comparison elsewhere. Idle gates
are removed; cancellation while waiting releases references. Different paths are
independent. Custom wrappers receive absolute write paths. Aliases/links, standalone
wrapper/FileHandler calls, FileLogger's separate gate, and other processes are outside
this coordination boundary; use consistent paths and stable models.

``ReplaceAtomicallyAsync(file, token)`` requires ``IAtomicFileWrapper``. DirectoryWrapper
writes and closes a unique CreateNew temporary sibling, then renames over the target.
On filesystems supporting atomic same-volume rename, readers see old or complete new
content. Cancellation/errors before publication preserve the target and attempt cleanup;
a cancellation racing publication may commit and a crash may leave a temporary file.
No fsync durability, metadata/ACL preservation, cross-volume transaction, or network
filesystem guarantee is promised. Other-process writes are last-writer-wins.

Optional base-directory containment
------------------------------------

Set ``BaseInfo.BaseDirectory`` to an absolute trusted directory. ``Path`` becomes a
relative subdirectory (empty allowed); ``Name`` is a simple filename, and the extension
cannot introduce path components. Rooted/drive/UNC names, either slash style of traversal,
and ambiguous trailing dot/space segments are rejected before FileUtility side effects.
Unset BaseDirectory preserves unrestricted legacy path behavior.

Existing links/reparse points at or below the base are rejected. Protect the base and
its ancestors from concurrent rename/link substitution: validation is not an OS sandbox
against hostile filesystem races or hard-link aliases. Use filesystem permissions or
a sandbox for hostile local users. Do not mutate models during delivery. The policy
applies to typed models, not arbitrary string-path wrapper calls.

.. code-block:: csharp

   var file = new TextFileInfo("reports", "daily", "data") { BaseDirectory = trustedRoot };
   await fileUtility.SaveOrUpdateAsync(file);

Explicit text write modes
--------------------------

``IExplicitFileUtility`` adds named methods without changing the old IFileUtility contract:

* ``AppendAsync`` appends, creating a missing file.
* ``OverwriteAsync`` truncates, creating a missing file.
* ``CreateNewAsync`` fails if the destination exists, leaving existing bytes unchanged.
* ``ReplaceAtomicallyAsync`` publishes a completed replacement, or creates a missing target.

All accept cancellation. DirectoryWrapper implements ``ITextWriteFileWrapper`` for overwrite
and exclusive creation. Append/overwrite may leave partial writes on error/cancellation;
create-new can leave a partial new file, but never truncates an existing destination.
Exclusive creation applies across processes; atomic replacement is last-writer-wins.

Legacy SaveOrUpdate/SaveOrUpdateAsync always append. Save/SaveAsync overwrite stream data
and honor LeaveOpen. New text callers should choose an explicit method. Text writes use
platform newlines and UTF-8 without a BOM.

.. code-block:: csharp

   IExplicitFileUtility files = new FileUtility(directoryWrapper, directoryWrapper);
   await files.ReplaceAtomicallyAsync(new TextFileInfo("reports", "daily", "data")
   {
       BaseDirectory = trustedRoot
   });
