Package Versions And Changes
============================

VersaTul packages are published and versioned independently. The NuGet Gallery
is the published source for each package's available versions, download counts,
and release notes attached to a specific package version.

Documentation versions
----------------------

DocsVersaTul uses site-wide documentation releases. Each documentation version
is a snapshot of the package pages, scenario guides, and released API reference
for the exact set of independently versioned NuGet packages it describes. A
documentation identifier such as ``2026.10`` is not a shared NuGet version;
each package continues to follow its own SemVer line and release pipeline.

The Read the Docs ``latest`` URL is reserved for the published stable site: its
version must follow the repository's ``stable`` branch, not the default
development branch. Pull-request and development builds remain previews and
must be labeled as such. Documentation release tags use the ``YYYY.MM`` value
from ``docs/RELEASE``; Read the Docs activates these tags as separate snapshots.
Keep a snapshot active while it documents a supported package major line. If a
line is no longer supported, hide its snapshot instead of deleting it so
existing version-specific links continue to work.

Each snapshot records the exact independently versioned NuGet packages it
describes. Link a NuGet package version to a documentation snapshot only when
that snapshot describes the exact package version and behavior; otherwise, use
the package's version history and the current package guide without implying an
exact version match. The :doc:`api-reference` lists the exact package versions
represented by its generated API sites.

There is no aggregate GitHub Releases page or separate ecosystem changelog at
this time. To review a package's history, open its page from the :doc:`package-catalog`
and select **Versions**. Later package pages link directly to that package's
version history.

The :doc:`release-notes-preview` page records source-branch changes that have
not been published as NuGet versions. It is explicitly a preview; use the
version-specific NuGet page above for released notes.

The NuGet profile lists all packages published by the VersaTul owner:
`VersaTul on NuGet <https://www.nuget.org/profiles/bwiliams256>`_.

For runtime and target-framework status, see :doc:`compatibility`. Package
versions can contain different framework assets, so review the exact version
you plan to install.
