Documentation Snippet Verification Inventory
============================================

This inventory covers every reStructuredText source directive that displays a code block or literal file under `docs/source`. Each location uses a stable ordinal within its source file, for example `getting-started.rst#1` is its first such directive.

The machine-readable source is :download:`snippet-inventory.json`. `Test-DocumentationSnippetInventory.ps1` checks that the manifest and this table still match the source directives.

Classifications
---------------

* **Compiled**: builds successfully, but validation does not run the code.
* **Executed**: the canonical sample is built and run for each directly supported framework; the expected output is checked.
* **Pseudocode**: an illustrative API fragment, not a standalone program. Every block is visibly captioned and excluded from the Getting Started copy-paste quickstart.
* **Configuration-only**: a command, fixture, or static text/output block; it is not compiled as C# source.

Inventory
---------

.. list-table::
   :header-rows: 1
   :widths: 20 30 18 32

   * - Location
     - Directive
     - Classification
     - Verification
   * - ``api-contract-policy.rst#1``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``api-contract-policy.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``api-contract-policy.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``bulk.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``bulk.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``bulk.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``bulk.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``bulk.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.Bulk/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``bulk.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.Bulk/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``caching.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``caching.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``caching.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``caching.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``caching.rst#5``
     - ``literalinclude:: ../samples/Caching/Program.cs``
     - **Executed**
     - Canonical sample project is built and run on all directly supported TFMs; expected stdout is checked.
   * - ``caching.rst#6``
     - ``literalinclude:: ../samples/Caching/ExpectedOutput.txt``
     - **Executed**
     - Compared with the corresponding executed sample stdout on all directly supported TFMs.
   * - ``caching.rst#7``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``caching.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Caching/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``caching.rst#9``
     - ``literalinclude:: ../samples/Packages/VersaTul.Caching/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``compression.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``compression.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``compression.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``compression.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``compression.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Compression/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``compression.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Compression/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``configuration-defaults.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``configuration-defaults.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``configuration-defaults.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``configuration-defaults.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``configuration-defaults.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Configuration.Defaults/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``configuration-defaults.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Configuration.Defaults/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``configuration.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``configuration.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``configuration.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``configuration.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``configuration.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Configurations/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``configuration.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Configurations/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``contracts.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``contracts.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``contracts.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``contracts.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``contracts.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Contracts/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``contracts.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Contracts/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``converters.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``converters.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``converters.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``converters.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``converters.rst#5``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``converters.rst#6``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``converters.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Object.Converters/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``converters.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Object.Converters/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``data-contracts.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``data-contracts.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``data-contracts.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``data-contracts.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``data-contracts.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.Contracts/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``data-contracts.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.Contracts/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``display-attributes.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``display-attributes.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``display-attributes.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``display-attributes.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``display-attributes.rst#5``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``display-attributes.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Display.Attributes/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``display-attributes.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Display.Attributes/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``efcore.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``efcore.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``efcore.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``efcore.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``efcore.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.EFCore/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``efcore.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.EFCore/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``extensions.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``extensions.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``extensions.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``extensions.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``extensions.rst#5``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``extensions.rst#6``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``extensions.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Extensions/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``extensions.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Extensions/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``file-reader.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``file-reader.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``file-reader.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``file-reader.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``file-reader.rst#5``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``file-reader.rst#6``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``file-reader.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.FileReader/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``file-reader.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.FileReader/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``getting-started.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``getting-started.rst#2``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``getting-started.rst#3``
     - ``literalinclude:: ../samples/GettingStarted/Program.cs``
     - **Executed**
     - Canonical sample project is built and run on all directly supported TFMs; expected stdout is checked.
   * - ``getting-started.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``getting-started.rst#5``
     - ``literalinclude:: ../samples/GettingStarted/ExpectedOutput.txt``
     - **Executed**
     - Compared with the corresponding executed sample stdout on all directly supported TFMs.
   * - ``handler-file.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``handler-file.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``handler-file.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``handler-file.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``handler-file.rst#5``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``handler-file.rst#6``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``handler-file.rst#7``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``handler-file.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Handler.File/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``handler-file.rst#9``
     - ``literalinclude:: ../samples/Packages/VersaTul.Handler.File/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``logger-file.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``logger-file.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger-file.rst#3``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``logger-file.rst#4``
     - ``literalinclude:: ../samples/Packages/VersaTul.Logger.File/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``logger-file.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Logger.File/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``logger-mail.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``logger-mail.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger-mail.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger-mail.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger-mail.rst#5``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``logger-mail.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Logger.Mail/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``logger-mail.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Logger.Mail/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``logger-web.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``logger-web.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger-web.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger-web.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger-web.rst#5``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``logger-web.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Logger.Web/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``logger-web.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Logger.Web/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``logger.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``logger.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``logger.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``logger.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Logger/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``logger.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Logger/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``mailer.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``mailer.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``mailer.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``mailer.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``mailer.rst#5``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``mailer.rst#6``
     - ``literalinclude:: ../samples/Mailer/Program.cs``
     - **Executed**
     - Canonical sample project is built and run on all directly supported TFMs; expected stdout is checked.
   * - ``mailer.rst#7``
     - ``literalinclude:: ../samples/Mailer/ExpectedOutput.txt``
     - **Executed**
     - Compared with the corresponding executed sample stdout on all directly supported TFMs.
   * - ``mailer.rst#8``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``mailer.rst#9``
     - ``literalinclude:: ../samples/Packages/VersaTul.Mailer/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``mailer.rst#10``
     - ``literalinclude:: ../samples/Packages/VersaTul.Mailer/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``mongodb.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``mongodb.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``mongodb.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``mongodb.rst#4``
     - ``literalinclude:: ../samples/MongoDB/Program.cs``
     - **Executed**
     - Canonical sample project is built and run on all directly supported TFMs; expected stdout is checked.
   * - ``mongodb.rst#5``
     - ``literalinclude:: ../samples/MongoDB/ExpectedOutput.txt``
     - **Executed**
     - Compared with the corresponding executed sample stdout on all directly supported TFMs.
   * - ``mongodb.rst#6``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``mongodb.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.MongoDB/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``mongodb.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.MongoDB/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``mssql.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``mssql.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``mssql.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``mssql.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``mssql.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.MsSql/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``mssql.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.MsSql/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``pipeline-infrastructure.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``pipeline-infrastructure.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``pipeline-infrastructure.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``pipeline-infrastructure.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``pipeline-infrastructure.rst#5``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``pipeline-infrastructure.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Pipeline.Infrastructure/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``pipeline-infrastructure.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Pipeline.Infrastructure/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``scenario-guides/data-export.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``scenario-guides/data-export.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/data-export.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/data-export.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/data-export.rst#5``
     - ``literalinclude:: ../../samples/DataExport/Program.cs``
     - **Executed**
     - Canonical sample project is built and run on all directly supported TFMs; expected stdout is checked.
   * - ``scenario-guides/data-export.rst#6``
     - ``literalinclude:: ../../samples/DataExport/ExpectedOutput.txt``
     - **Executed**
     - Compared with the corresponding executed sample stdout on all directly supported TFMs.
   * - ``scenario-guides/file-import.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``scenario-guides/file-import.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/file-import.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/file-import.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/file-import.rst#5``
     - ``literalinclude:: ../../samples/FileImport/Program.cs``
     - **Executed**
     - Canonical sample project is built and run on all directly supported TFMs; expected stdout is checked.
   * - ``scenario-guides/file-import.rst#6``
     - ``literalinclude:: ../../samples/FileImport/Fixtures/people.csv``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``scenario-guides/file-import.rst#7``
     - ``literalinclude:: ../../samples/FileImport/ExpectedOutput.txt``
     - **Executed**
     - Compared with the corresponding executed sample stdout on all directly supported TFMs.
   * - ``scenario-guides/logging-setup.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``scenario-guides/logging-setup.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/logging-setup.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/logging-setup.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/logging-setup.rst#5``
     - ``literalinclude:: ../../samples/FileLogging/Program.cs``
     - **Executed**
     - Canonical sample project is built and run on all directly supported TFMs; expected stdout is checked.
   * - ``scenario-guides/logging-setup.rst#6``
     - ``literalinclude:: ../../samples/FileLogging/ExpectedOutput.txt``
     - **Executed**
     - Compared with the corresponding executed sample stdout on all directly supported TFMs.
   * - ``scenario-guides/sql-data-access.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``scenario-guides/sql-data-access.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/sql-data-access.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/sql-data-access.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scenario-guides/sql-data-access.rst#5``
     - ``literalinclude:: ../../samples/SqlDataAccess/Program.cs``
     - **Executed**
     - Canonical sample project is built and run on all directly supported TFMs; expected stdout is checked.
   * - ``scenario-guides/sql-data-access.rst#6``
     - ``literalinclude:: ../../samples/SqlDataAccess/ExpectedOutput.txt``
     - **Executed**
     - Compared with the corresponding executed sample stdout on all directly supported TFMs.
   * - ``scheduler.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``scheduler.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scheduler.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scheduler.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scheduler.rst#5``
     - ``code-block:: text``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``scheduler.rst#6``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``scheduler.rst#7``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``scheduler.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Task.Scheduler/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``scheduler.rst#9``
     - ``literalinclude:: ../samples/Packages/VersaTul.Task.Scheduler/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``sql.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``sql.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``sql.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``sql.rst#4``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``sql.rst#5``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.Sql/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``sql.rst#6``
     - ``literalinclude:: ../samples/Packages/VersaTul.Data.Sql/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``streamers.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``streamers.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``streamers.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``streamers.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``streamers.rst#5``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``streamers.rst#6``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``streamers.rst#7``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``streamers.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Collection.Streamers/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``streamers.rst#9``
     - ``literalinclude:: ../samples/Packages/VersaTul.Collection.Streamers/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
   * - ``utilities.rst#1``
     - ``code-block:: console``
     - **Configuration-only**
     - Command, fixture data, or static text/output; not compiled as C# source.
   * - ``utilities.rst#2``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``utilities.rst#3``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``utilities.rst#4``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``utilities.rst#5``
     - ``code-block:: csharp``
     - **Pseudocode**
     - Illustrative C# API fragment; intentionally not independently compiled or run.
   * - ``utilities.rst#6``
     - ``code-block:: console``
     - **Configuration-only**
     - Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.
   * - ``utilities.rst#7``
     - ``literalinclude:: ../samples/Packages/VersaTul.Utilities/Program.cs``
     - **Executed**
     - Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.
   * - ``utilities.rst#8``
     - ``literalinclude:: ../samples/Packages/VersaTul.Utilities/ExpectedOutput.txt``
     - **Executed**
     - Compared with stdout from the canonical package README sample after it is built and run for every supported framework.
