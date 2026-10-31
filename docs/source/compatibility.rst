Compatibility And Support
=========================

This page separates three facts that can differ: the frameworks in a VersaTul package, the framework asset NuGet selects, and the runtime versions Microsoft still services.

Transition target frameworks
----------------------------

The VersaTul transition plan directly targets and tests ``net8.0``, ``net9.0``, and ``net10.0`` for all 25 library packages, including ``VersaTul.Data.FileReader``. Host and test projects use the same matrix.

.. list-table:: Framework wording
   :header-rows: 1

   * - Term
     - Meaning
   * - **Directly targeted and tested**
     - The project declares that exact TFM. The transition CI builds and tests it, and package validation packs and consumes the matching NuGet asset.
   * - **Compatible with**
     - NuGet can select another compatible asset when the package has no exact TFM asset. This does not mean the package was built or tested for that exact runtime.

Applications should target ``net10.0`` for a supported Microsoft runtime. The official `.NET support policy <https://dotnet.microsoft.com/en-us/platform/support/policy>`_ lists .NET 8 and .NET 9 support through 2026-11-10 and .NET 10 LTS support through 2028-11-14. VersaTul's additional build and test coverage for ``net8.0`` and ``net9.0`` does not extend Microsoft's runtime or dependency servicing.

VersaTul will keep the ``net8.0`` and ``net9.0`` assets in its transition target matrix through 2027-11-10. They are compatibility targets after Microsoft's support ends on 2026-11-10. Their removal is planned for the first approved major package release on or after 2027-11-10. See the source repository's ``DOTNET_FRAMEWORK_SUPPORT_POLICY.md`` for the exact policy and migration steps.

Migration before .NET 8/9 support ends
--------------------------------------

1. Install the latest serviced .NET 10 SDK and runtime. If the repository pins an SDK in ``global.json``, update that pin.
2. Change application and test projects from ``net8.0`` or ``net9.0`` to ``net10.0``.
3. Upgrade Entity Framework Core and all provider packages together to the 10.x line. Review the `EF Core 10 changes <https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-10.0/whatsnew>`_.
4. Restore and build the application, run its tests on .NET 10, and smoke its database providers and hosting/deployment paths.
5. Choose VersaTul packages that directly target ``net10.0``. Check each package's dependency graph and migration notes; a lower TFM asset being compatible with .NET 10 is not proof that the package was directly tested there.

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
5. If your workflow depends on file-based import, check :doc:`file-reader`; FileReader now follows the same target matrix as the other packages.

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
