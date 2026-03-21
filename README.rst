DocsVersaTul
============

This repository contains the Sphinx documentation for the VersaTul .NET library ecosystem.

The documentation is written against the library projects in the main VersaTul repository and is organized around the NuGet-distributed packages, not the host or test projects.

Documentation Scope
-------------------

The current documentation set covers these package groups:

1. Foundation packages such as configuration, contracts, converters, extensions, and utilities.
2. Data and storage packages such as caching, bulk, SQL, SQL Server, MongoDB, EF Core, and file readers.
3. File, processing, and integration packages such as compression, streamers, display attributes, file handling, and pipelines.
4. Operational packages such as logging, mail delivery, and task scheduling.

Repository Layout
-----------------

1. ``docs/source`` contains the reStructuredText source files.
2. ``docs/source/index.rst`` is the documentation landing page.
3. ``docs/requirements.txt`` defines the Python packages needed to build the site locally.
4. ``DOCUMENTATION_REDESIGN_PLAN.md`` tracks the modernization work completed and remaining.
5. ``PACKAGE_DOC_TEMPLATE.md`` captures the structure used for package reference pages.

Local Build
-----------

The documentation uses Sphinx with the Read the Docs theme.

Install the documented dependencies:

.. code-block:: console

   python -m pip install -r docs/requirements.txt

Build the HTML output from the repository root:

.. code-block:: console

   cd docs
   make html

On Windows without ``make``:

.. code-block:: console

   cd docs
   make.bat html

Build Requirements
------------------

The current docs dependencies are:

1. ``sphinx==5.3.0``
2. ``sphinx_rtd_theme==1.3.0``
3. ``readthedocs-sphinx-search==0.1.1``

Current Local Validation Status
-------------------------------

The documentation pages have been validated in-editor, but full local HTML validation depends on Python and Sphinx being available on the machine running the build.

In the current development environment used for the recent rewrite work, Python was not installed, so a full Sphinx build could not be executed locally there.

Writing Guidance
----------------

When updating package pages:

1. Use the VersaTul source repository as the truth source.
2. Prefer documenting the shipped library projects only.
3. Keep the page structure consistent with the package template.
4. Focus on current APIs and realistic usage patterns rather than historical changelog content.

Primary Entry Points
--------------------

1. ``docs/source/getting-started.rst`` for onboarding.
2. ``docs/source/package-selection.rst`` for choosing packages.
3. ``docs/source/package-catalog.rst`` for ecosystem browsing.
4. ``docs/source/index.rst`` for the complete documentation map.
