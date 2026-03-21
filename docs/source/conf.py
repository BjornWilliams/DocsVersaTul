# Configuration file for the Sphinx documentation builder.

project = "VersaTul Documentation"
copyright = "2026, VersaTul"
author = "Bjorn Williams"
release = "Current"
version = release

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "readthedocs_sphinx_search.extension",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_title = "VersaTul Documentation"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 3,
    "style_external_links": False,
}

epub_show_urls = "footnote"
