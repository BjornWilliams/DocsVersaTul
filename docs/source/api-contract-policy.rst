API Contract Policy
===================

Nullable Reference Metadata
---------------------------

The audit releases enable C# nullable reference metadata in the library projects.
CLR signatures remain available, but callers compiling with nullable warnings
enabled should review diagnostics when upgrading. Optional inputs and valid
lookup absence are described by nullable annotations and the individual API's
XML documentation. A nullable annotation does not change runtime validation.

Each package's source compatibility impact is reviewed independently. Activating
metadata on a formerly oblivious public API is treated conservatively as a Major
migration. This does not assign one shared version number to all packages.

Keep caller-side null checks where an API can return an absent value. Do not
silence warnings globally when migrating. Refer to the package-specific
documentation for defaults, required settings and missing-key behavior.

Valid Absence
-------------

The annotations preserve the existing runtime outcomes:

* A cache miss, a missing named SQL parameter, a MongoDB ID lookup with no match,
  and an EF Core lookup with no match can return null for reference types.
* Configuration ``Get`` still throws for a missing key. A present setting can
  contain null. ``GetOrDefault`` also returns ``default(T)`` for a missing key.
  ``TryGetValue`` can return true with a null value.
* Conversion of null or ``DBNull`` returns ``default(T)``. A successful
  ``TryTransform`` can therefore produce null. An absent SQL scalar follows the
  same generic default behavior. For a non-nullable value type such as ``int``,
  ``default(T)`` remains zero; annotations do not turn it into ``Nullable<int>``.
* Display attribute lookup returns null when no attribute exists. Display name
  lookup still returns a usable name. Formatting may preserve a null value.
* Mutable descriptors and optional callbacks can be null before configuration;
  nullable metadata does not make incomplete descriptors valid for every operation.

Check the result before dereferencing it. For example:

.. code-block:: csharp

   using System;
   using VersaTul.Utilities;

   object? input = null;
   string? converted = new CommonUtility().Transform<string>(input);
   Console.WriteLine(converted ?? "absent");

Omitted ``CallerMemberName`` configuration names are supplied by the C# compiler.
Passing an explicit null name remains invalid. The default marker used by those
declarations does not relax that input contract.

Collection-backed data readers retain their established null cell values. Their
concrete nullable metadata describes those values, while the BCL ``IDataRecord``
interface has stricter annotations. When using that interface, check ``IsDBNull``
before reading a potentially absent cell. This audit does not silently replace
null cells with ``DBNull``. Remaining lifecycle and BCL interoperability compiler
diagnostics stay visible; nullable activation is not a claim of zero warnings.

Arguments And Unsupported Operations
----------------------------------------

Required dependencies and inputs reject null with ``ArgumentNullException``.
Non-null invalid values, including required strings that are empty or whitespace,
use ``ArgumentException`` or its range-specific subclass. APIs that normalize
optional null input retain their documented defaults; for example, the text case
helpers still return an empty string for null input, and cache options may select
defaults with null.

Unsupported operations use ``NotSupportedException``. In particular, the MongoDB
micron serializer rejects unsupported BSON representations with this exception
rather than ``NotImplementedException``. A missing destination table reported by
SQL bulk schema lookup uses ``InvalidOperationException`` and retains the SQL
exception as its cause.

When upgrading, review handlers that caught ``ArgumentNullException`` for empty
strings or a generic exception for unsupported operations. Check exception type
and ``ParamName`` for argument failures; do not match localized framework message
text. Required dependency guards run during construction or before operation
enumeration, rather than allowing a delayed null-reference failure.

This includes dependencies passed through primary constructors and abstract data
service bases. Supply valid data sources, conversion helpers, configuration and
bulk services during construction, including in test doubles. A later operation
is not the place to discover that one of these required services was null.

Cancellation
------------

Existing signatures remain available. Select the token-aware overload or optional
capability when an operation should observe cancellation:

* ``ICancellableFileLogger`` covers the file path gate and asynchronous append.
  Synchronous rotation is observed at operation boundaries and cannot be
  interrupted after it starts. A cancelled append can leave partial output.
* ``ICancellableMailLogger`` passes tokens to asynchronous dispatch and explicit
  flushing. Unstarted batches stay queued; an interrupted attempted batch is
  retained as a dead letter without retrying with the cancelled token. Once a
  log call queues an event, the logger owns its eventual delivery independently
  of that call's token. Disposing the logger drains accepted work.
* ``ICancellableBulkCopy`` passes tokens through token-aware services, connection
  opening, bulk writes and commit. Cancellation attempts rollback with an
  uncancelled token and still disposes resources. The rethrown cancellation's
  ``Data["BulkCopyResult"]`` contains failure and cleanup diagnostics.
* ``ICancellableQueryRepository<TEntity>`` offers ``GetAllAsync`` and
  ``GetAllNoTrackingAsync``. Distinct names avoid a collision with key lookup when
  a repository's key type is ``CancellationToken``. Existing EF, MongoDB and SQL
  token APIs remain available; derived SQL services also have token overloads
  for reader, nonquery and scalar execution.
* ``ICancellableZipper``, ``ICancellableArchiver`` and ``ICancellableCompressor``
  cover archive chunks and streamer generation. Inputs remain borrowed and
  failed output streams are cleaned up. Callers own successful compressed and
  extracted streams.

For example, the following helper uses the optional file capability:

.. code-block:: csharp

   using System.Threading;
   using System.Threading.Tasks;
   using VersaTul.Logger;
   using VersaTul.Logger.File.Contracts;

   static Task WriteLogAsync(ICancellableFileLogger logger, LogInfo entry,
       CancellationToken cancellationToken)
       => logger.LogAsync(entry, cancellationToken);

Legacy injected services remain usable. When they have no token capability,
cancellation is cooperative between calls; it cannot interrupt their in-flight
synchronous or tokenless work. Cancellation is not a guarantee that a server
did not accept a write or message. Completed in-memory task adapters, including
the cache facade, do not acquire a new asynchronous lifetime merely because
their return type is ``Task``. Framework disposal APIs retain their normal
uncancelled cleanup contract.

The common ``ILogger`` contract requires a log descriptor. ``MailLogger`` retains
its existing null-descriptor rejection. Concrete ``FileLogger`` and ``WebLogger``
helpers additionally retain their null-normalization convenience, and
``LogParser`` can render an absent descriptor. Nullable annotations follow those
individual contracts rather than advertising every sink as accepting null.
