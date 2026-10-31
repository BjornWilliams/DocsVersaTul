Compatibility And Support
=========================

**Last checked:** 2026-10-31 (Microsoft policy updated 2026-10-25)

**Page owner:** VersaTul maintainers

**Next scheduled review:** 2026-11-09

Framework support as of 2026-10-31
----------------------------------

The Microsoft status and patches below are taken from the official `.NET support policy <https://dotnet.microsoft.com/en-us/platform/support/policy>`_. The current VersaTul source branch directly targets and tests all three listed TFMs for its 25 library packages. The TFM assets inside a published NuGet package are version-specific and may differ from current source.

.. list-table:: .NET runtime support and VersaTul framework state
   :header-rows: 1

   * - Runtime and TFM
     - Microsoft servicing state on 2026-10-31
     - Latest Microsoft patch (released)
     - Microsoft end of support
     - Current VersaTul source
     - Published NuGet asset state
   * - .NET 8 / ``net8.0``
     - LTS; Maintenance
     - ``8.0.33`` (2026-10-25)
     - 2026-11-10
     - Directly targeted and tested for all 25 library packages
     - Version-specific: direct only when that package version contains a ``net8.0`` asset
   * - .NET 9 / ``net9.0``
     - STS; Maintenance
     - ``9.0.22`` (2026-10-25)
     - 2026-11-10
     - Directly targeted and tested for all 25 library packages
     - Version-specific: direct only when that package version contains a ``net9.0`` asset; otherwise NuGet may report computed compatibility from a lower TFM
   * - .NET 10 / ``net10.0``
     - LTS; Active
     - ``10.0.14`` (2026-10-25)
     - 2028-11-14
     - Directly targeted and tested for all 25 library packages
     - Version-specific: direct only when that package version contains a ``net10.0`` asset; otherwise NuGet may report computed compatibility from a lower TFM

**Production runtime choice:** target .NET 10 and keep it on the latest serviced patch. .NET 8 and .NET 9 reach Microsoft's end of support on 2026-11-10. VersaTul's source build and test coverage does not extend Microsoft runtime or dependency servicing.

Framework and package wording
-----------------------------

.. list-table:: How to read framework and package states
   :header-rows: 1

   * - State
     - Meaning
   * - **Directly targeted and tested**
     - The VersaTul source project declares that exact TFM and the audit validation builds and tests it.
   * - **Direct NuGet asset**
     - The exact package version contains an asset for that TFM. Check the version-specific ``Included target framework(s)`` list on NuGet.
   * - **Computed-compatible**
     - NuGet can select a lower-TFM asset for the requested framework. This is not a direct asset, direct build, or test for that framework, and does not establish runtime support.
   * - **Maintenance / Active**
     - Microsoft's servicing phase for the runtime on the date above. Use the latest Microsoft patch while the runtime remains in support.
   * - **End of support**
     - Microsoft's servicing end date. After it, Microsoft no longer provides routine runtime security fixes or servicing for that release.

Use the exact package version's included assets to decide whether that package is directly targeted for your runtime. A NuGet ``computed-compatible`` result alone is not evidence that the package version contains a native TFM asset or was directly tested for it.

Package-version exceptions
--------------------------

Published package assets can lag behind the current source TFM matrix. The following exception was checked against NuGet on 2026-10-31:

.. list-table:: Verified published package asset exception
   :header-rows: 1

   * - Package version
     - Included target framework assets
     - NuGet computed compatibility
     - Current VersaTul source
   * - ``VersaTul.Data.FileReader`` 1.0.9, the latest published version shown on the review date
     - ``net8.0`` only
     - ``net9.0`` and ``net10.0`` are computed from the lower ``net8.0`` asset
     - The current source branch directly targets and tests ``net8.0``, ``net9.0``, and ``net10.0``; those newer assets are not in published version 1.0.9

See the exact `NuGet Gallery page for VersaTul.Data.FileReader 1.0.9 <https://www.nuget.org/packages/VersaTul.Data.FileReader/1.0.9>`_ before choosing an asset. NuGet's compatibility list is not a substitute for the package page's ``Included target framework(s)`` list. Check the exact version of every package you install because asset sets can change between versions.

VersaTul transition support
---------------------------

Microsoft support for .NET 8 and .NET 9 ends on 2026-11-10. VersaTul's continued builds and tests do not extend Microsoft's runtime or dependency servicing, and do not promise security fixes or support for applications that remain on those end-of-support runtimes. Production applications should migrate to .NET 10 before that date.

VersaTul will directly target, build, and test ``net8.0`` and ``net9.0`` transition assets through 2027-11-10, one year after Microsoft's end-of-support date. This is a time-limited compatibility-validation window, not a promise that Microsoft or third-party dependencies will continue servicing .NET 8 or .NET 9. After 2027-11-10, VersaTul makes no support or validation promise for those targets. If no major release is ready on that date, assets may remain temporarily for best-effort compatibility; their removal is planned for the first approved major package release on or after 2027-11-10. Removing a TFM is a breaking package change. See the source repository's ``DOTNET_FRAMEWORK_SUPPORT_POLICY.md`` for the policy and migration steps.

Migration before .NET 8/9 support ends
--------------------------------------

Follow the :doc:`dotnet-10-upgrade` guide to update the SDK, target framework, framework-specific dependencies, package assets, tests, and deployment runtime. Move production applications to ``net10.0`` before .NET 8 and .NET 9 reach Microsoft's end of support on 2026-11-10.

Package and dependency notes
----------------------------

The target matrix includes the NuGet library packages. Host and test projects are validation assets and are not included in the public adoption surface.

Database package dependencies vary by target. The transition uses EF Core 9.x for ``net8.0`` and ``net9.0`` and EF Core 10.x for ``net10.0``; keep EF Core providers on the same major version. Microsoft.Extensions packages follow the same 9.x / 10.x target split. VersaTul uses Microsoft.Data.SqlClient 6.1 LTS, which targets .NET 8 and is compatible with later .NET runtimes. MongoDB.Driver 3.1 provides .NET 6 and .NET Standard 2.1 assets, which NuGet can use for later targets. Exact selected versions are maintained in the source repository's central package file.

Practical guidance
------------------

1. For production applications, migrate to ``net10.0`` before .NET 8 and .NET 9 reach end of support.
2. When upgrading Entity Framework, upgrade EF Core and its provider packages together and review the `EF Core 10 changes <https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-10.0/whatsnew>`_.
3. For SQL Server-specific features, prefer :doc:`mssql` over trying to stretch :doc:`sql` into a SQL Server-only role.
4. For provider flexibility, prefer :doc:`sql` first and move to :doc:`mssql` only when the requirement becomes SQL Server-specific.
5. If your workflow depends on file-based import, check :doc:`file-reader` and the exact NuGet version's included target frameworks; published ``VersaTul.Data.FileReader`` 1.0.9 contains only ``net8.0``.

Compatibility expectations by package style
--------------------------------------------

Different VersaTul packages fit different application shapes.

1. Foundation packages such as configuration, contracts, utilities, and extensions are the easiest to adopt in a .NET application.
2. Data packages depend more heavily on your storage and provider choices.
3. Operational packages such as logging and mailer depend on the delivery target you choose.
4. Export and file-processing packages depend more on your workflow than on framework integration.

What this page does not promise
-------------------------------

Direct framework targeting and tests do not guarantee every transitive dependency combination, every hosting model, or backward compatibility with legacy .NET Framework projects. A lower TFM asset selected by NuGet is a compatibility result, not evidence of direct validation.

What to read next
-----------------

1. Read :doc:`recommended-paths` for an opinionated starting point by application type.
2. Read :doc:`faq` if your remaining questions are about adoption fit and package choice.
3. Read :doc:`package-selection` if you need to decide between similar package families.
