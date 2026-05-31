Compatibility And Support
=========================

This page gives a concise compatibility view for developers evaluating whether VersaTul fits their application baseline.

Current Target Framework Baseline
---------------------------------

The documented VersaTul library packages are built for modern .NET.

Based on the current package projects in the main VersaTul repository:

1. Most documented library packages target ``net8.0`` and ``net9.0``.
2. ``VersaTul.Data.FileReader`` currently targets ``net8.0``.

That means the safest adoption assumption today is that VersaTul is intended for current-generation .NET applications rather than older .NET Framework workloads.

Documented Package Surface
--------------------------

These docs are intentionally scoped to the NuGet-distributed library projects.

They do not treat host projects or test projects as part of the public adoption surface.

External Dependency Profile
---------------------------

The repository currently centralizes package versions through the shared package props file and includes dependencies such as:

1. ``Microsoft.EntityFrameworkCore`` for EF Core support.
2. ``Microsoft.Data.SqlClient`` for SQL Server access.
3. ``MongoDB.Driver`` for MongoDB support.
4. ``Microsoft.Extensions.Caching.Memory`` for default in-memory caching support.

This matters for adopters because different VersaTul packages pull in different infrastructure dependencies depending on the workflow you choose.

Practical Compatibility Guidance
--------------------------------

1. If your service is already on ``net8.0`` or ``net9.0``, VersaTul is aligned with that baseline.
2. If you need SQL Server-specific features, prefer :doc:`mssql` over trying to stretch :doc:`sql` into a SQL Server-only role.
3. If you need provider flexibility, prefer :doc:`sql` first and move to :doc:`mssql` only when the requirement becomes SQL Server-specific.
4. If your workflow depends on file-based import, check :doc:`file-reader` because it currently has the narrower target-framework baseline.

Compatibility Expectations By Package Style
-------------------------------------------

Different VersaTul packages fit different application shapes.

1. Foundation packages such as configuration, contracts, utilities, and extensions are the easiest to adopt in almost any modern .NET application.
2. Data packages depend more heavily on your storage and provider choices.
3. Operational packages such as logging and mailer depend on the delivery target you choose.
4. Export and file-processing packages depend more on your workflow than on framework integration.

What This Page Does Not Promise
-------------------------------

This page is intended as an adoption-oriented baseline, not a full support policy.

It does not attempt to guarantee:

1. every transitive dependency combination,
2. every hosting model, or
3. backward compatibility with legacy .NET Framework projects.

What To Read Next
-----------------

1. Read :doc:`recommended-paths` if you want an opinionated starting point by application type.
2. Read :doc:`faq` if your remaining questions are about adoption fit and package choice.
3. Read :doc:`package-selection` if you need to decide between similar package families.