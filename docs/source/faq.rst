FAQ
===

This page answers the most common evaluation questions a .NET developer is likely to have before adopting VersaTul.

Is VersaTul One Framework Or A Set Of Packages?
-----------------------------------------------

VersaTul is a set of focused NuGet packages, not one monolithic framework.

That means you can start with one package for one problem and expand only when the next need is real.

What Is The Best First Package To Try?
--------------------------------------

For a low-friction first evaluation, start with :doc:`getting-started` and ``VersaTul.Configurations``.

That path gives you a fast, copy-paste success case without needing database or infrastructure setup first.

How Do I Know Which Package To Pick?
------------------------------------

Use :doc:`package-selection` first.

That page is organized around developer jobs such as configuration, data access, import, export, logging, and scheduling.

If you want to see how packages work together instead of choosing from the catalog, use :doc:`scenario-guides/index`.

Do I Need To Adopt A Large Part Of The Ecosystem At Once?
---------------------------------------------------------

No.

The documentation now assumes a staged adoption ladder:

1. Start with one package.
2. Prove one workflow.
3. Add only the adjacent package that clearly supports the next step.

Are The Packages Intended To Work Together?
-------------------------------------------

Yes, but not all at once.

Some of the strongest combinations are:

1. ``VersaTul.Configurations`` with ``VersaTul.Configuration.Defaults``.
2. ``VersaTul.Data.FileReader`` with ``VersaTul.Data.Bulk`` and ``VersaTul.Data.MsSql``.
3. ``VersaTul.Collection.Streamers`` with ``VersaTul.Display.Attributes`` and ``VersaTul.Object.Converters``.
4. ``VersaTul.Logger`` with a sink package such as ``VersaTul.Logger.File``.

Should I Start With ``Data.Sql`` Or ``Data.MsSql``?
---------------------------------------------------

Start with :doc:`sql` when provider flexibility still matters.

Start with :doc:`mssql` when SQL Server is an intentional platform choice and the workflow needs SQL Server-specific behavior such as bulk copy or structured parameters.

Should I Start With ``Logger`` Or A Concrete Logger Package?
------------------------------------------------------------

Use :doc:`logger` as the shared contract and formatting layer.

Use a sink package such as :doc:`logger-file`, :doc:`logger-mail`, or :doc:`logger-web` when you need logs to actually be delivered somewhere.

If you want the fastest working setup, start with :doc:`scenario-guides/logging-setup`.

What If My Main Need Is Import Or Export?
-----------------------------------------

Start with the workflow pages, not the full package catalog.

1. For import workflows, start with :doc:`scenario-guides/file-import`.
2. For export workflows, start with :doc:`scenario-guides/data-export`.

How Stable Is The Documentation Path For New Users?
---------------------------------------------------

The recommended first path is now:

1. :doc:`getting-started`
2. :doc:`package-selection`
3. :doc:`scenario-guides/index`
4. specific package pages only after the first workflow is clear

That path is the intended evaluation flow for new adopters.

What Should I Read After The First Successful Quickstart?
---------------------------------------------------------

The next best step depends on the problem you are solving.

1. Read :doc:`recommended-paths` for opinionated starting sets by application type.
2. Read :doc:`scenario-guides/index` if your next need involves multiple packages.
3. Read :doc:`package-catalog` if you want the broader ecosystem map.