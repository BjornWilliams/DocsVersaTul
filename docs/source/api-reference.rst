Generated API Reference
=======================

Search the released public API by namespace, type, member, or signature. Each target-specific site is generated from exact released NuGet assemblies and their version-matched XML documentation.

* `Browse the .NET 8 API reference <https://docsversatul.readthedocs.io/en/latest/_api_ref/net8.0/index.html>`_
* `Browse the .NET 9 API reference <https://docsversatul.readthedocs.io/en/latest/_api_ref/net9.0/index.html>`_

The package versions and direct framework assets represented in these sites are listed below. Each package keeps its own NuGet version; this page does not imply that the packages share a release number.

.. include:: _generated_api_versions.rst

Source and signatures
---------------------

DocFX reflects each public assembly from the exact ``.nupkg`` identified in the manifest. The published packages do not contain XML sidecars, so the XML comments are generated from the exact source commit recorded in each package's NuGet nuspec. Assembly hashes and XML hashes are recorded in ``api-xml-manifest.json``.

DocFX generates the signatures from the released assemblies; they are not copied by hand. Nullability and default values come from assembly metadata. Exception, parameter, and return comments come from the version-matched XML documentation where present. Ownership and thread-safety statements appear only when the package documents them; missing documentation is not a guarantee about behavior.

The documentation workflow reports each public API member that has no matching XML documentation entry. Its per-framework coverage reports are attached to the workflow run.
