Contribute to VersaTul
======================

VersaTul uses two repositories. The public
`DocsVersaTul repository <https://github.com/BjornWilliams/DocsVersaTul>`_
contains the documentation, issue forms, and runnable documentation samples.
The `library source repository
<https://technojam.visualstudio.com/VersaTul/_git/VersaTul>`_ is hosted in
Azure Repos and may require sign-in; see :doc:`repository-access` before
planning a source-code contribution.

Where changes belong
--------------------

The **Edit this page on GitHub** link opens the maintained ``main`` branch.
Propose documentation corrections there; dated documentation tags preserve
their published snapshots.

* Propose documentation corrections through the `GitHub issue chooser
  <https://github.com/BjornWilliams/DocsVersaTul/issues/new/choose>`_ and
  select **Documentation help**, or use the page's **Edit this page on GitHub**
  link.
* Report package bugs, usage questions, or feature ideas through the public
  forms described on :doc:`support`.
* Package source, tests, and release-policy changes belong in the VersaTul
  Azure Repos repository. Follow its ``CONTRIBUTING.md``,
  ``Agent.md``, and package versioning policy.
* Do not post vulnerability details publicly. Follow :doc:`security` and the
  repository's ``SECURITY.md`` instructions for a private route.

Package architecture
--------------------

The source repository contains 25 independently versioned ``VersaTul.*``
NuGet library packages. They are organized into seven dependency layers. A
package in a later layer may consume packages from earlier layers; use the
complete `dependency graph
<https://technojam.visualstudio.com/VersaTul/_git/VersaTul?path=/LIBRARY_DEPENDENCY_GRAPH.md>`_
when reviewing a change that affects package dependencies.

.. list-table:: Package groups by dependency layer
   :header-rows: 1
   :widths: 10 90

   * - Layer
     - Packages
   * - 0
     - ``VersaTul.Compression``, ``VersaTul.Contracts``, ``VersaTul.Data.Bulk``, ``VersaTul.Data.Contracts``, ``VersaTul.Handler.File``, ``VersaTul.Logger``, ``VersaTul.Pipeline.Infrastructure``, ``VersaTul.Utilities``
   * - 1
     - ``VersaTul.Display.Attributes``
   * - 2
     - ``VersaTul.Object.Converters``
   * - 3
     - ``VersaTul.Extensions``
   * - 4
     - ``VersaTul.Configurations``
   * - 5
     - ``VersaTul.Caching``, ``VersaTul.Configuration.Defaults``, ``VersaTul.Mailer``, ``VersaTul.Data.EFCore``, ``VersaTul.Data.FileReader``, ``VersaTul.Data.MongoDB``, ``VersaTul.Data.Sql``, ``VersaTul.Logger.Web``, ``VersaTul.Logger.File``, ``VersaTul.Task.Scheduler``
   * - 6
     - ``VersaTul.Logger.Mail``, ``VersaTul.Data.MsSql``, ``VersaTul.Collection.Streamers``

The layers describe the internal library dependency graph, not a promise that
every package must be installed or released together. Packages remain
independently versioned. When an upstream package changes, inspect the graph
and the actual project references to find the downstream packages that need
validation.

Test one package
----------------

The source repository has xUnit test projects under
``VersaTul.Test.Library.*``. Start with the test project matching the package
suffix, then run it on each framework the test project directly targets. The
current source matrix is ``net8.0``, ``net9.0``, and ``net10.0``; check the
source repository's ``DOTNET_FRAMEWORK_SUPPORT_POLICY.md`` for current policy.

From the source repository root, this runs the Compression package tests on all
three targets:

.. code-block:: console
   :caption: Run the Compression test project on each directly targeted framework.

   dotnet test VersaTul.Test.Library.Compression/VersaTul.Test.Library.Compression.csproj --framework net8.0
   dotnet test VersaTul.Test.Library.Compression/VersaTul.Test.Library.Compression.csproj --framework net9.0
   dotnet test VersaTul.Test.Library.Compression/VersaTul.Test.Library.Compression.csproj --framework net10.0

Replace ``Compression`` with the corresponding package suffix. If a package's
test project uses a different name or its tests share a project with a related
package, follow the project references in that test project and use the full
repository validation pipeline for the broader dependency graph. Some
provider/integration tests need local services; review that project's
integration instructions before running them.

For a documentation-only change, install ``docs/requirements.txt`` and follow
the strict build and post-build checks in the DocsVersaTul
``DOCUMENTATION_VALIDATION.md``. Documentation examples shown as runnable are
checked by the repository's pull-request workflow.
