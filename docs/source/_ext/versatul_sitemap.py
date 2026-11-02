"""Write a per-version sitemap while preserving Read the Docs' root sitemap."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from xml.etree import ElementTree

from sphinx.application import Sphinx
from sphinx.errors import ExtensionError

SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
ElementTree.register_namespace("", SITEMAP_NAMESPACE)


def _write_search_files(app: Sphinx, exception: Exception | None) -> None:
    if exception is not None or app.builder.format != "html":
        return

    base_url = app.config.html_baseurl
    parsed_base = urlsplit(base_url)
    if parsed_base.scheme not in {"http", "https"} or not parsed_base.netloc:
        raise ExtensionError("html_baseurl must be an absolute HTTP or HTTPS URL.")

    base_url = base_url.rstrip("/") + "/"
    sitemap = ElementTree.Element(f"{{{SITEMAP_NAMESPACE}}}urlset")
    seen_urls: set[str] = set()
    for docname in sorted(app.env.found_docs):
        if docname == app.config.root_doc:
            # Read the Docs' root sitemap already contains the default-version URL.
            continue
        target_uri = app.builder.get_target_uri(docname)
        if not target_uri or target_uri.startswith(("#", "javascript:")):
            continue

        location = urljoin(base_url, target_uri)
        if location in seen_urls:
            raise ExtensionError(f"Duplicate URL in documentation sitemap: {location}")
        seen_urls.add(location)
        url_entry = ElementTree.SubElement(sitemap, f"{{{SITEMAP_NAMESPACE}}}url")
        ElementTree.SubElement(url_entry, f"{{{SITEMAP_NAMESPACE}}}loc").text = location

    output_dir = Path(app.builder.outdir)
    ElementTree.ElementTree(sitemap).write(
        output_dir / "sitemap-pages.xml",
        encoding="utf-8",
        xml_declaration=True,
    )

    # Read the Docs serves robots.txt from the project root using the default
    # version's build output. Preserve its generated root sitemap and point to
    # the per-version page sitemap under this build's canonical URL.
    site_root = urlunsplit((parsed_base.scheme, parsed_base.netloc, "", "", ""))
    robots = "\n".join(
        (
            "User-agent: *",
            "Allow: /",
            "",
            f"Sitemap: {site_root}/sitemap.xml",
            f"Sitemap: {base_url}sitemap-pages.xml",
            "",
        )
    )
    (output_dir / "robots.txt").write_text(robots, encoding="utf-8", newline="\n")


def setup(app: Sphinx) -> dict[str, object]:
    app.connect("build-finished", _write_search_files)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
