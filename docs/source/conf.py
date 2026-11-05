# Configuration file for the Sphinx documentation builder.

import json
import os
import sys
from pathlib import Path

project = "VersaTul Documentation"
copyright = "2026, VersaTul"
author = "Bjorn Williams"
# DocsVersaTul owns one docs release identifier; NuGet packages keep their
# independent package-family versions. Update docs/RELEASE for a docs release.
release_file = Path(__file__).resolve().parents[1] / "RELEASE"
release = release_file.read_text(encoding="utf-8").strip()
if not release or release.casefold() in {"current", "latest"}:
    raise ValueError(f"Set a dated docs release in {release_file}")
version = release

readthedocs_build = os.environ.get("READTHEDOCS", "").casefold() == "true"
readthedocs_version_type = os.environ.get("READTHEDOCS_VERSION_TYPE", "").casefold()
readthedocs_version = os.environ.get("READTHEDOCS_VERSION", "")

# Stable RTD releases are tagged with the same YYYY.MM identifier stored in
# docs/RELEASE. This prevents a tag from silently publishing another snapshot.
if (
    readthedocs_build
    and readthedocs_version_type == "tag"
    and readthedocs_version != release
):
    raise ValueError(
        "Read the Docs tag version must match docs/RELEASE: "
        f"{readthedocs_version!r} != {release!r}"
    )

# Development and pull-request builds can contain source-only APIs. Show a
# visible warning on every page unless this is a dated tag or the dedicated
# stable branch that backs the published latest view. Local builds are previews.
published_documentation = readthedocs_build and (
    readthedocs_version_type == "tag"
    or (readthedocs_version_type == "branch" and readthedocs_version == "stable")
)
if not published_documentation:
    rst_prolog = """
.. warning::

   **Preview documentation.** This build may describe source changes that are
   not present in published NuGet packages. Verify the exact package version
   before relying on its behavior.
"""

# Read the Docs supplies the canonical URL for the version being built. Keep
# the production URL as the local-build fallback so generated links remain
# canonical outside Read the Docs too.
html_baseurl = (
    os.environ.get("READTHEDOCS_CANONICAL_URL")
    or "https://docsversatul.readthedocs.io/en/latest/"
).rstrip("/") + "/"

seo_metadata_path = Path(__file__).with_name("seo-metadata.json")
versatul_page_metadata = json.loads(seo_metadata_path.read_text(encoding="utf-8"))
versatul_social_image_url = html_baseurl + "_static/versatul-social-preview.png"
html_context = {
    "versatul_page_metadata": versatul_page_metadata,
    "versatul_site_baseurl": html_baseurl,
    "versatul_social_image_url": versatul_social_image_url,
}

sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "sphinx_search.extension",
    "versatul_sitemap",
]

# Match the local strict build's `-n` cross-reference validation.
nitpicky = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]
html_static_path = ["_static"]
exclude_patterns = [
    "_build",
    "_api_ref",
    "_generated_api_links",
    "_generated_api_versions.rst",
    "_generated_historical_api_versions.rst",
    "_generated_historical_api_links",
    "Thumbs.db",
    ".DS_Store",
]

# The released API sites are generated before Sphinx and copied as static HTML.
html_extra_path = ["_api_ref"]

html_theme = "sphinx_rtd_theme"
html_title = "VersaTul Documentation"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 3,
    "style_external_links": False,
}

epub_show_urls = "footnote"
