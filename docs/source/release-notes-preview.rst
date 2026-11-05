Unreleased Package Change Preview
=================================

.. warning::

   These notes describe changes on the VersaTul source development branch.
   They are not included in the currently published NuGet package versions,
   and no NuGet version has been assigned. Use each package's exact NuGet
   version page for released behavior and release notes. The notes may change
   before a package is published.

The proposed SemVer impact is shown for release planning only. Each package
continues to receive its own version from its Azure Pipeline. This source audit
does not change package projects, central package versions, dependencies, or
target frameworks. For later package work, record any exact dependency or
framework change and its migration guidance in the affected package's notes.

Breaking changes
----------------

``VersaTul.Collection.Streamers`` (proposed **Major**): ``CollectionReader``
keeps its nullable convenience members, while its ``IDataRecord`` adapters now
follow standard non-null record behavior. A null object field is returned as
``DBNull.Value``; invalid ``GetData`` or ``GetString`` conversions throw
``InvalidCastException``. Public methods that previously implemented the
interface directly are now separate adapters.

Migration:

.. code-block:: csharp
   :caption: Pseudocode: illustrative migration fragment, not a standalone sample.

   using System.Data;

   IDataRecord record = reader;
   object value = record.GetValue(ordinal);
   if (value is DBNull)
   {
       // Handle a database null.
   }

See :doc:`streamers` and the exact `NuGet version history
<https://www.nuget.org/packages/VersaTul.Collection.Streamers#versions-body-tab>`_.

``VersaTul.Data.MsSql`` (proposed **Major**): ``CommandDiagnostics`` now marks
the connection name and exception parameters nullable because callbacks can
receive a null name for the default connection and a null exception after a
successful command. The callback CLR type is unchanged.

Migration:

.. code-block:: csharp
   :caption: Pseudocode: illustrative callback fragment, not a standalone sample.

   source.CommandDiagnostics = (_, connectionName, _, succeeded, exception) =>
   {
       var displayName = connectionName ?? "(default)";
       if (succeeded && exception is null)
       {
           // Record a successful command.
       }
   };

See :doc:`mssql` and the exact `NuGet version history
<https://www.nuget.org/packages/VersaTul.Data.MsSql#versions-body-tab>`_.

``VersaTul.Data.Sql`` (proposed **Major**): generated nullable-context metadata
for ``DataConfiguration`` is attached at the type boundary instead of being
repeated on members. Effective source nullability and CLR call shapes do not
change. Reflection code that reads only method-level
``NullableContextAttribute`` metadata must also inspect the declaring type.

Migration:

.. code-block:: csharp
   :caption: Pseudocode: illustrative reflection fragment, not a standalone sample.

   using System.Linq;
   using System.Reflection;

   var nullableContext = method.GetCustomAttributesData()
       .Concat(method.DeclaringType!.GetCustomAttributesData())
       .FirstOrDefault(attribute =>
           attribute.AttributeType.FullName ==
           "System.Runtime.CompilerServices.NullableContextAttribute");

See :doc:`sql` and the exact `NuGet version history
<https://www.nuget.org/packages/VersaTul.Data.Sql#versions-body-tab>`_.

Feature
-------

``VersaTul.Logger.Web`` (proposed **Minor**) adds ``IDisposable`` to
``WebLogger`` so callers can release its request-serialization gate after
active logging calls complete. See :doc:`logger-web` and the exact `NuGet
version history <https://www.nuget.org/packages/VersaTul.Logger.Web#versions-body-tab>`_.

Fixes
-----

The following proposed **Patch** notes describe corrections that preserve each
package's documented public contract:

* :doc:`caching` — use an explicit clock and null-flow guards so cache
  operations remain deterministic under nullable analysis.
* :doc:`compression` — reject incomplete ZIP stream and file descriptors with
  parameter-specific argument errors; archive output and ownership stay the
  same.
* :doc:`configuration-defaults` — validate required configuration builder
  inputs and report missing values with clear argument errors.
* :doc:`configuration` — make null flow explicit and reject invalid inputs
  with parameter-specific errors.
* :doc:`bulk` — correct malformed generated XML documentation for bulk-copy
  members and parameters.
* :doc:`data-contracts` — align repository-interface XML documentation with
  its actual nullability contract.
* :doc:`efcore` — guard missing EF configuration and repository values before
  provider operations.
* :doc:`file-reader` — validate reader options and filters before opening
  files while preserving supported format routing.
* :doc:`mongodb` — validate map, repository, and serializer inputs before
  MongoDB operations.
* :doc:`display-attributes` — reject missing pipeline delegates and declaring
  types explicitly, and format display numbers invariantly.
* :doc:`extensions` — validate extension arguments and use the documented
  culture for formatting and conversion.
* :doc:`handler-file` — validate file descriptors and paths before I/O, and
  preserve asynchronous cleanup and existing ``LeaveOpen`` defaults.
* :doc:`logger-file` — validate the executing file path before archive and
  logging operations.
* :doc:`logger-mail` — validate logger inputs and document callback and
  exception contracts.
* :doc:`logger` — escape XML-sensitive schema content and make log parsing and
  output encoding null-safe.
* :doc:`mailer` — reject invalid mail configuration and message arguments
  before SMTP operations.
* :doc:`converters` — validate converter inputs, handle absent reflection
  values explicitly, and use invariant formatting.
* :doc:`pipeline-infrastructure` — document the public pipeline extension
  contract so generated package documentation is complete.
* :doc:`scheduler` — validate scheduler state and storage values while
  preserving the published ``NextRunTime`` parameter name and scheduling
  defaults.
* :doc:`utilities` — use invariant conversion policies and validate collection
  and enum inputs before processing.

