.NET 10 Upgrade Guide
=====================

Use this guide to move an application from ``net8.0`` or ``net9.0`` to
``net10.0``. Microsoft's support for .NET 8 and .NET 9 ends on 2026-11-10.
See :doc:`compatibility` for the dated runtime table, package asset exceptions,
and VersaTul's transition validation window.

Before you start
----------------

Inventory the application's target frameworks, pinned SDK in ``global.json``,
Entity Framework Core and provider versions, VersaTul package versions, and
deployment runtime or container image. Check the included target frameworks of
the exact package versions you use; a NuGet computed-compatible result is not
proof of a direct ``net10.0`` asset.

1. Install a serviced .NET 10 SDK and the runtime required by the application
   from the `official .NET 10 download page
   <https://dotnet.microsoft.com/en-us/download/dotnet/10.0>`_. If the
   repository pins the SDK in ``global.json``, update that pin to an installed
   .NET 10 SDK. Confirm the installation with:

   .. code-block:: console

      dotnet --list-sdks
      dotnet --list-runtimes

2. Update application and test project files to target ``net10.0``:

   .. code-block:: xml

      <TargetFramework>net10.0</TargetFramework>

   If a shared library intentionally keeps multiple target frameworks during
   the transition, add ``net10.0`` and retain older TFMs only under the
   repository's support policy. Removing ``net8.0`` or ``net9.0`` from a
   NuGet package is a breaking change and requires a separately approved
   major release.

3. Align framework-specific dependencies. EF Core 10 requires the .NET 10 SDK
   to build and the .NET 10 runtime to run. Upgrade all EF Core packages,
   design-time tooling, and database providers together to the 10.x line; do
   not mix EF Core major versions. Update central package management files and
   review the `EF Core 10 changes
   <https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-10.0/whatsnew>`_
   and `EF Core 10 breaking changes
   <https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-10.0/breaking-changes>`_.
   Align other Microsoft.Extensions packages and provider dependencies with
   the .NET 10 target where their package requirements call for it.

4. Select VersaTul package versions with an included ``net10.0`` asset when
   you need direct targeting and test coverage for .NET 10. Open each exact
   NuGet version's ``Included target framework(s)`` list. A package page that
   reports ``net10.0`` as computed-compatible is showing a lower-TFM asset,
   not a native ``net10.0`` asset. For example,
   :doc:`compatibility` documents the ``VersaTul.Data.FileReader`` 1.0.9
   exception.

5. Restore, build, and test the application. For a single-target application:

   .. code-block:: console

      dotnet restore
      dotnet build --configuration Release
      dotnet test --configuration Release

   For multi-target test projects, run the suite for ``net10.0`` and every
   other TFM the application still supports. Resolve compile, analyzer, and
   test failures instead of suppressing them as migration noise.

6. Validate the actual publish and hosting path. Publish for the deployment
   runtime identifier where applicable, update container or hosting images to
   .NET 10, and smoke startup, health checks, configuration, telemetry, and
   shutdown. Exercise database connections, queries, transactions, and schema
   migrations against a representative non-production database before
   deployment.

Completion checklist
--------------------

- Application, test, and deployment targets use .NET 10 where planned.
- ``global.json`` selects an installed, supported .NET 10 SDK.
- EF Core and all EF providers use one compatible major version; EF Core 10
  changes and provider-specific behavior have been reviewed.
- Each VersaTul package version has a direct ``net10.0`` asset when direct
  targeting is required; NuGet computed compatibility is not used as proof.
- Restore, Release build, tests, publish, and hosting/database smoke checks
  pass in the deployment-shaped environment.
- Production moves off .NET 8/9 before 2026-11-10, when Microsoft support for
  those runtimes ends. VersaTul's separate transition asset validation does
  not extend Microsoft runtime or dependency servicing.
