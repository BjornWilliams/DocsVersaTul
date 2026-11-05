Generated API Reference
=======================

Search the released public API by namespace, type, member, or signature. The current package sites use exact released NuGet assemblies and version-matched XML documentation.

* `Browse the .NET 8 API reference <https://docsversatul.readthedocs.io/en/latest/net8.0/index.html>`_
* `Browse the .NET 9 API reference <https://docsversatul.readthedocs.io/en/latest/net9.0/index.html>`_

The package versions and direct framework assets represented in these sites are listed below. Each package keeps its own NuGet version; this page does not imply that the packages share a release number.

.. include:: _generated_api_versions.rst

.. include:: _generated_historical_api_versions.rst

Source and signatures
---------------------

DocFX reflects each public assembly from the exact ``.nupkg`` identified in the manifest. The published packages do not contain XML sidecars, so the XML comments are generated from the exact source commit recorded in each package's NuGet nuspec. Assembly hashes and XML hashes are recorded in ``api-xml-manifest.json``.

DocFX generates the signatures from the released assemblies; they are not copied by hand. Nullability and default values come from assembly metadata. Exception, parameter, and return comments come from the version-matched XML documentation where present. Ownership and thread-safety statements appear only when the package documents them; missing documentation is not a guarantee about behavior.

The current-package workflow reports each public API member that has no matching XML documentation entry. Its per-framework coverage reports are attached to the workflow run. The retained 1.x SQL packages predate packaged XML documentation and Source Link metadata; their API signatures are generated from the exact assemblies and are paired with each version's published NuGet description.
