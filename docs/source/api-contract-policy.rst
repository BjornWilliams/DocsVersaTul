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

File rotation's ``Archiver`` also requires its configuration and file handler at
construction; null dependencies raise ``ArgumentNullException`` with their
parameter names.

Scheduler method-call constructors require their delegate or method metadata and
any supplied parameter setter. Named/order setters require their collection or
array. An empty bound-parameter array uses ``ArgumentException``; select the
action-only overload for no bound parameters. Use an explicit no-op delegate for
a placeholder and assign a non-null ``Action`` when replacing it.

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

Resource Ownership
------------------

Ownership follows the concrete API. Keep borrowed dependencies alive until all
active operations complete; disposing a container of referenced values does not
automatically dispose those values.

Streams and files
~~~~~~~~~~~~~~~~~

* ``VersaTul.Compression``: Zipper borrows ZipStream input streams and returns new compressed or extracted MemoryStreams owned by the caller. Dispose every returned stream. Archiver borrows both the ZipArchive and input stream; the injected archiver is borrowed. Input positions are preserved by archive writes.
* ``VersaTul.Handler.File``: FileUtility borrows injected file and directory wrappers. StreamFileInfo.LeaveOpen defaults to true: the caller retains its Content stream. Set LeaveOpen to false to transfer cleanup to Save/SaveAsync, including failure and cancellation. Returned text/results contain no open file handle.
* ``VersaTul.Collection.Streamers``: BaseStreamer owns its bound reader and backing output stream. Rebinding or disposing it releases those resources; there is no reader leave-open option. GetFileStream returns that shared backing stream, borrowed until reset, rebinding or disposal. Collection elements are borrowed; their enumerator is owned. Compressor borrows inputs and returns a caller-owned compressed stream. StreamContainer only borrows stream references. FileConverter.Save consumes and disposes the supplied streamer after argument validation. Raw attachments returned by CompressTransport are caller-owned until transferred to a MailDispatcher; each attachment owns its content stream.

Readers and database resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``VersaTul.Data.FileReader``: A CSV reader owns its CsvReader and opened StreamReader. Dispose the returned reader. Text readers buffer input and return a caller-owned DataTableReader. A lazy directory read retains cleanup responsibility until enumeration completes: failure or early abandonment closes readers opened so far, including already yielded readers. After successful enumeration the caller owns all returned readers.
* ``VersaTul.Data.EFCore``: BaseUnitOfWork owns its injected DbContext and disposes it. BaseRepository borrows the unit of work and context; it does not dispose either. Keep the unit of work alive while using deferred queries; returned entities are not automatically disposed.
* ``VersaTul.Data.Sql``: SqlDbDataSource borrows its command factory and retry callbacks. A reader it returns owns the created command and non-transaction connection; the caller must dispose the reader. An externally supplied transaction retains its connection ownership. CommandFactory execution borrows supplied commands. BaseDataService transaction callbacks borrow the scoped transaction. ProcessReader closes its reader after successful or failed processing; callers must still scope disposal for arbitrary custom readers.
* ``VersaTul.Data.MsSql``: BulkCopy consumes its service for each started transaction attempt and disposes the service afterward. The default service owns the connection, bulk-copy wrapper, transaction and consumed source reader; its validator is borrowed. The default ValidDataReader owns its wrapped reader. Custom validator wrappers must document whether they own the source. Dispose is an operation-cycle cleanup; default service wrappers can be initialized again with Create for a later copy.
* ``VersaTul.Data.MongoDB``: The repository borrows its configuration and the collection returned by that configuration; it has no Dispose contract. The default configuration creates MongoClient instances using driver-managed client/pool lifetimes. Configuration, class maps and entity values are borrowed. Dispose query enumerators you create and keep their backing driver resources available through enumeration.

Messages and clients
~~~~~~~~~~~~~~~~~~~~

* ``VersaTul.Mailer``: MailDispatcher borrows its SMTP client and template renderer. It owns one MailMessage per logical send; each raw Attachment transfers to that message when added and is disposed with it on success or failure. Retries reuse the same message and attachments. Never-attached attachments remain caller-owned. IMailAttachment payloads are borrowed and mapped to new message-owned attachments. Pre-cancelled async sends do not transfer attachments. SmtpClientWrapper owns its factory-created SmtpClient, borrows the factory and caller MailMessage, and must outlive active sends.
* ``VersaTul.Logger.Web``: WebLogger borrows its factory, parser, configuration and clock callback. Each send owns and disposes its factory-created HttpClient, request and response. Factories must return clients safe for per-operation disposal. Complete active calls before releasing borrowed dependencies.
* ``VersaTul.Logger.File``: FileLogger borrows configuration, parser and file utility. Each append owns its path-gate lease, FileStream and writer and releases them when the operation ends. Keep borrowed dependencies alive through awaited calls.
* ``VersaTul.Logger.Mail``: MailLogger borrows its dispatcher, parser and configuration; it does not dispose the dispatcher or SMTP client. It owns its queue, worker and cancellation state. DisposeAsync drains accepted events before releasing owned worker resources; await it and active operations before disposing borrowed dependencies. Accepted queued events remain the logger responsibility independently of the enqueue call token.

Callbacks and referenced values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``VersaTul.Caching``: MemCacheProvider owns its internal MemoryCache. It borrows configuration, clock, logger factory, removal callbacks and cached values; expiration, removal and provider disposal do not dispose cached values. Await active operations before disposing the provider.
* ``VersaTul.Task.Scheduler``: BaseTimer owns its System.Timers.Timer and subscription. Clock, storage, scheduled task objects and caller delegates are borrowed; disposing the timer does not dispose them. TimerTask owns active cancellation state and borrows its event, method and filter/callback targets. Callers manage their subscriptions and callback-resource lifetimes.
* ``VersaTul.Pipeline.Infrastructure``: Pipeline steps, delegates and their captured values are borrowed and are not disposed by the pipeline. Keep them alive through execution; callers own any subscriptions, resources and concurrency coordination needed by their callbacks.
* ``VersaTul.Display.Attributes``: Registered formatter delegates and objects are borrowed. Registration does not transfer disposal responsibility for a formatter or its captured resources. Keep those resources alive for every formatting call.
* ``VersaTul.Configurations``: Configuration values are borrowed references. Snapshots copy the mapping, not the referenced objects, and do not acquire disposal responsibility for IDisposable values. Factories and callbacks remain caller-owned.
* ``VersaTul.Configuration.Defaults``: Default configuration entries and referenced values are borrowed. Read-only snapshots do not clone or dispose referenced objects. Callers retain ownership of disposable values and resources captured by callbacks.

Core contracts, converters, utilities and extension helpers borrow their inputs
and referenced elements. They do not acquire disposal responsibility for those
objects. Concrete resource implementations and their packed READMEs define any
transfer. Always dispose enumerators and I/O resources you create.

Disposal and Partial Initialization
-----------------------------------

Idempotent disposal means that repeated calls do not repeat owned cleanup. If a
cleanup attempt throws, it is reported once; repeating Dispose does not retry it.
Quiesce active operations before disposing their owner.

* ``VersaTul.Compression``: Failed compression/extraction releases output streams that cannot be returned. Borrowed inputs stay open. Legacy overloads share the token-aware cleanup path with CancellationToken.None; callers still own every successful output.
* ``VersaTul.Mailer``: SmtpClientWrapper attempts client cleanup once, even when cleanup throws, and releases a factory-created client if configuration fails afterward. Partial IMailAttachment mapping releases already-created native attachments. Borrowed clients and payloads retain their existing ownership.
* ``VersaTul.Data.EFCore``: Unit-of-work disposal attempts owned context cleanup once, including when that attempt throws. A cleanup exception does not make the unit of work reusable and does not trigger a second context disposal attempt.
* ``VersaTul.Data.FileReader``: DisposableDataReader shares one release state across Close and Dispose and attempts every distinct owned resource. Dispose retains legacy best-effort exception suppression; Close reports its first failure after cleanup. Partial CSV construction releases the opened file. Abandoned/failing directory enumeration attempts every distinct opened reader; an enumeration failure stays primary and cleanup diagnostics are in ``Exception.Data["ReaderCleanupErrors"]``.
* ``VersaTul.Data.Sql``: Returned owned readers share one release state across Close, Dispose and DisposeAsync. Cleanup attempts the reader, command and owned connection, preserving the first cleanup error and retaining later failures in ``Exception.Data["CleanupErrors"]``. Transaction connections remain borrowed. ProcessReader closes on success and failure and restores the previous callback reader context; scope caller disposal for arbitrary custom readers. A callback failure stays primary with a close failure in ``Exception.Data["ReaderCleanupError"]``.
* ``VersaTul.Data.MsSql``: Service cleanup attempts every owned resource once per Create cycle, including after partial initialization or a cleanup failure. Create releases a preceding cycle before starting another; concurrent Create/use/disposal is unsupported. ISourceReaderOwner optionally identifies a validated wrapper that owns its SourceReader, preventing duplicate source disposal. Default ValidDataReader implements it. Legacy unmarked validators retain separate wrapper and source cleanup; implement the optional capability if your wrapper owns that same source. The first failure stays primary; later failures are retained in ``Exception.Data["CleanupErrors"]``.
* ``VersaTul.Collection.Streamers``: Disposal and rebinding detach owned resources before attempting cleanup and attempt remaining resources after a failure. Failed binding releases readers already transferred to the streamer and internally-created collection enumerators. FileConverter borrows the streamer output until its owner is disposed and scopes temporary compressed output. Failed attachment construction releases completed attachments and compressed output; streams not yet transferred stay borrowed. Failed MailTransporter dispatch releases its created attachments, preserving the dispatch failure and cleanup diagnostics. Successful dispatch retains the dispatcher ownership contract. The first cleanup failure stays primary; later failures appear in Exception.Data.

The optional ``ISourceReaderOwner`` capability adds no obligation to an existing
validator implementation. For an owning wrapper, return its exact wrapped reader
from ``SourceReader`` and implement idempotent disposal. A wrapper that borrows a
source should keep the existing unmarked contract.

Paths, Identifiers and Time Boundaries
--------------------------------------

Use platform path composition and ordinal comparison for machine identifiers.
Human input/display culture is a separate contract from persisted formats.
Legacy DateTime APIs remain available; an offset-bearing instant is supplied at
the scheduler callback boundary when the unbound parameter is DateTimeOffset.

* ``VersaTul.Handler.File``: File extensions are machine identifiers and use ordinal case-insensitive matching, including under Turkish culture. Paths continue to use platform path APIs and the existing contained-path rules.
* ``VersaTul.Utilities``: PropertyMap exclusions use ordinal case-insensitive identifier matching. Human text conversion and explicitly culture-selectable scalar conversion keep their existing culture contracts.
* ``VersaTul.Logger.File``: Archive names use one DateTimeOffset sample and invariant Gregorian yyyy_MM_dd-HH_mm_ss_fff formatting. Local daily rolling and local retention dates remain unchanged. Existing archives remain discoverable; new names no longer use a culture-specific calendar year.
* ``VersaTul.Task.Scheduler``: Unbound DateTimeOffset callback parameters receive the normalized UTC event instant. Framework parameters use exact type identity; a user type with the same short name is not a framework parameter. Existing DateTime APIs, unspecified-as-UTC boundary policy, local input parsing and calendar behavior remain unchanged. Scheduler persistence already writes invariant round-trip timestamps and accepts its documented legacy read formats.
* ``VersaTul.Data.MsSql``: SQL identifier hints use ordinal case-insensitive matching while exact destination lookup remains ordinal and case sensitive. SQL error 208 identifies a missing table across server languages; the legacy English prefix remains an ordinal fallback. Command elapsed diagnostics use a monotonic stopwatch rather than wall-clock subtraction.
* ``VersaTul.Collection.Streamers``: Compressed attachment labels retain their existing local date/time name shape. A DateTimeOffset sample and invariant numeric formatting define that label independently of culture. Output paths retain platform Path.Combine behavior; display formatting remains explicitly culture-selectable.

SQL DateOnly values
~~~~~~~~~~~~~~~~~~~

``ParameterRules.DateOnly`` retains a string ``Value`` and now writes invariant
Gregorian ``yyyy-MM-dd``. The SQL Server ``SqlParameter`` inherits the same rule.
For example:

.. code-block:: csharp

   using System;
   using System.Data;
   using VersaTul.Data.Sql;

   var parameter = new Parameter("when", new DateTime(2031, 4, 5),
       DbType.Date, 0, ParameterDirection.Input, ParameterRules.DateOnly);
   // parameter.Value is the string "2031-04-05" under every culture.

Update exact-format comparisons and parsers that expected the former
``ToShortDateString`` output. Read old persisted strings using their original
culture; read new output using ``yyyy-MM-dd`` and invariant culture. Typed
``DateTime`` input bypasses the display calendar. Legacy string input still parses
with the current culture. This rule strips time without converting time zones.
The output-format migration requires the Major compatibility review for
``VersaTul.Data.Sql`` and independently for ``VersaTul.Data.MsSql``.
