#!/usr/bin/env python3
"""Build DocFX API sites from checksum-verified released VersaTul packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPOSITORY_ROOT / "docs" / "source"
BUILD_ROOT = REPOSITORY_ROOT / "docs" / "build" / "api-reference"
INVENTORY_PATH = SOURCE_ROOT / "package-inventory.json"
VERSION_STATUS_PATH = SOURCE_ROOT / "package-version-status.json"
XML_MANIFEST_PATH = SOURCE_ROOT / "api-xml-manifest.json"
DOCS_RELEASE_PATH = REPOSITORY_ROOT / "docs" / "RELEASE"
GENERATED_ROOT = SOURCE_ROOT / "_api_ref"
FRAMEWORKS = ("net8.0", "net9.0")
DOCS_RELEASE = DOCS_RELEASE_PATH.read_text(encoding="utf-8").strip()
if not re.fullmatch(r"\d{4}\.\d{2}", DOCS_RELEASE):
    raise ValueError(f"Set docs/RELEASE to a dated YYYY.MM snapshot, found {DOCS_RELEASE!r}.")
PUBLIC_DOCS_BASE = f"https://docsversatul.readthedocs.io/en/{DOCS_RELEASE}"


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_xml_sha256(data: bytes) -> str:
    """Hash XML content independently of the checkout's line-ending convention."""
    canonical_bytes = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return sha256(canonical_bytes)


def download_package(package_id: str, version: str, cache_root: Path) -> Path:
    package_file = f"{package_id.lower()}.{version}.nupkg"
    package_path = cache_root / package_file
    if package_path.is_file():
        return package_path

    package_url = (
        "https://api.nuget.org/v3-flatcontainer/"
        f"{package_id.lower()}/{version}/{package_file}"
    )
    request = urllib.request.Request(
        package_url,
        headers={"User-Agent": "VersaTul-Docs-API-Reference/1.0"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
    temporary_path = package_path.with_suffix(package_path.suffix + ".tmp")
    temporary_path.write_bytes(payload)
    temporary_path.replace(package_path)
    return package_path


def load_release_inputs() -> tuple[list[dict], dict[str, dict], dict[str, dict]]:
    inventory = read_json(INVENTORY_PATH)
    status_rows = read_json(VERSION_STATUS_PATH)
    manifest = read_json(XML_MANIFEST_PATH)
    if not isinstance(inventory, list) or not isinstance(status_rows, list):
        raise ValueError("Package inventory and version status must be JSON arrays.")
    if not isinstance(manifest, dict) or manifest.get("schemaVersion") != 1:
        raise ValueError("The released API XML manifest is missing or unsupported.")

    inventory_by_id = {row["PackageId"]: row for row in inventory}
    status_by_id = {row["PackageId"]: row for row in status_rows}
    package_rows = manifest.get("packages")
    if not isinstance(package_rows, list):
        raise ValueError("The released API XML manifest has no package list.")
    manifest_by_id = {row["packageId"]: row for row in package_rows}

    expected = set(inventory_by_id)
    if expected != set(status_by_id) or expected != set(manifest_by_id):
        raise ValueError("Inventory, version status, and XML manifest package sets differ.")
    for package_id in sorted(expected):
        if package_id.startswith(("VersaTul.Host", "VersaTul.Test")):
            raise ValueError(f"Non-package assembly appeared in the public package inventory: {package_id}")
        status = status_by_id[package_id]
        entry = manifest_by_id[package_id]
        version = status.get("LastVerifiedVersion")
        if status.get("VerificationSource") != "NuGet Gallery":
            raise ValueError(f"{package_id} does not have a verified NuGet Gallery version.")
        if status.get("VersionPageUrl") != f"https://www.nuget.org/packages/{package_id}/{version}":
            raise ValueError(f"{package_id} does not link to its exact verified package version.")
        if entry.get("version") != version or entry.get("packageUrl") != status["VersionPageUrl"]:
            raise ValueError(f"{package_id} release version does not match the XML manifest.")
        if not re.fullmatch(r"[0-9a-f]{40}", entry.get("repositoryCommit", "")):
            raise ValueError(f"{package_id} has no exact 40-character source commit in the XML manifest.")
    return inventory, status_by_id, manifest_by_id


def validate_xml_documentation(xml_path: Path, expected_hash: str) -> set[str]:
    payload = xml_path.read_bytes()
    if canonical_xml_sha256(payload) != expected_hash:
        raise ValueError(f"XML documentation hash mismatch: {xml_path}")
    document = ET.fromstring(payload)
    members_node = document.find("./members")
    if members_node is None:
        raise ValueError(f"XML documentation has no members element: {xml_path}")
    return {
        member.attrib["name"]
        for member in members_node.findall("./member")
        if member.attrib.get("name")
    }


def parse_xrefmap(path: Path) -> list[dict[str, str]]:
    references: list[dict[str, str]] = []
    current: dict[str, str] = {}

    def append_current() -> None:
        if current.get("uid") and current.get("href"):
            references.append(current.copy())

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("- uid: "):
            append_current()
            current = {"uid": line[len("- uid: ") :].strip()}
        elif current and line.startswith("  href: "):
            current["href"] = line[len("  href: ") :].strip()
        elif current and line.startswith("  commentId: "):
            current["commentId"] = line[len("  commentId: ") :].strip()
        elif current and line.startswith("  name: "):
            current["name"] = line[len("  name: ") :].strip()
    append_current()
    return references


def restore_framework_references(
    framework: str,
    packages: list[dict],
    stage_root: Path,
) -> list[Path]:
    probe_root = stage_root / framework / "dependency-probe"
    probe_root.mkdir(parents=True, exist_ok=True)
    package_references = [package for package in packages if framework in package["frameworks"]]
    reference_items = "\n".join(
        f'    <PackageReference Include="{package["packageId"]}" Version="{package["version"]}" />'
        for package in package_references
    )
    project = (
        '<Project Sdk="Microsoft.NET.Sdk">\n'
        "  <PropertyGroup>\n"
        f"    <TargetFramework>{framework}</TargetFramework>\n"
        "    <NuGetAudit>false</NuGetAudit>\n"
        "  </PropertyGroup>\n"
        "  <ItemGroup>\n"
        f"{reference_items}\n"
        "  </ItemGroup>\n"
        "</Project>\n"
    )
    project_path = probe_root / "VersaTul.ApiReference.Dependencies.csproj"
    project_path.write_text(project, encoding="utf-8")
    print(f"Restoring exact package dependencies for {framework}.", flush=True)
    subprocess.run(
        ["dotnet", "restore", str(project_path), "--nologo", "--verbosity", "quiet"],
        cwd=probe_root,
        check=True,
    )

    assets_path = probe_root / "obj" / "project.assets.json"
    assets = read_json(assets_path)
    target = assets.get("targets", {}).get(framework)
    if not isinstance(target, dict):
        raise ValueError(f"NuGet restore did not produce a {framework} dependency target.")
    package_folders = [Path(folder) for folder in assets.get("packageFolders", {})]
    references_root = stage_root / framework / "references"
    reference_paths: list[Path] = []
    for package_key, package_assets in target.items():
        package_id, separator, package_version = package_key.partition("/")
        if not separator or package_id.casefold().startswith("versatul."):
            continue
        if package_id.casefold().startswith(("system.", "microsoft.netcore.")) or package_id.casefold() in {
            "microsoft.csharp",
            "netstandard.library",
        }:
            # The .NET reference pack supplies platform assemblies. Adding old
            # System.* NuGet facades as DocFX extras can shadow those core refs.
            continue
        for relative_asset in package_assets.get("compile", {}):
            if not relative_asset.casefold().endswith(".dll"):
                continue
            source_path = next(
                (
                    folder / package_id.casefold() / package_version.casefold() / relative_asset
                    for folder in package_folders
                    if (folder / package_id.casefold() / package_version.casefold() / relative_asset).is_file()
                ),
                None,
            )
            if source_path is None:
                raise ValueError(f"NuGet restore asset is missing: {package_key}/{relative_asset}")
            destination = references_root / package_id.casefold() / package_version.casefold() / relative_asset
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, destination)
            reference_paths.append(destination)

    if not reference_paths:
        raise ValueError(f"NuGet restore found no external references for {framework}.")
    print(f"Restored {len(reference_paths)} external reference assemblies for {framework}.", flush=True)
    return reference_paths


def build_docfx_site(
    framework: str,
    packages: list[dict],
    stage_root: Path,
    package_assemblies: dict[str, list[Path]],
    dependency_assemblies: list[Path],
) -> tuple[Path, list[dict[str, str]]]:
    site_root = stage_root / framework
    site_root.mkdir(parents=True, exist_ok=True)
    package_rows = [
        package
        for package in packages
        if any(asset["targetFramework"] == framework for asset in package["assets"])
    ]
    frameworks_by_id = {package["packageId"]: package["frameworks"] for package in packages}

    table = [
        "| Package | Released NuGet version | Matching docs snapshot | Package source commit |",
        "| --- | --- | --- | --- |",
    ]
    for package in package_rows:
        table.append(
            "| `{}` | [{}]({}) | [{}]({}) | `{}` |".format(
                package["packageId"],
                package["version"],
                package["packageUrl"],
                DOCS_RELEASE,
                package["documentationUrl"],
                package["repositoryCommit"],
            )
        )
    frameworks_note = [
        "| Package | Direct released assets |",
        "| --- | --- |",
    ]
    for package in packages:
        frameworks_note.append(
            f"| `{package['packageId']}` | {', '.join(f'`{tfm}`' for tfm in frameworks_by_id[package['packageId']])} |"
        )

    index_lines = [
        f"# VersaTul API reference ({framework})",
        "",
        "This reference is generated from the exact published NuGet assemblies listed below. "
        "XML comments are paired from the source commit recorded in each package's NuGet nuspec "
        "because the released packages do not contain XML sidecars. Signatures come from the "
        "released assemblies.",
        "",
        "The assemblies are public NuGet packages only. The DocFX metadata build excludes "
        "internal APIs, and the input inventory excludes test and host projects.",
        "",
        "## Package versions represented in this target-specific site",
        "",
        *table,
        "",
        "## Direct target-framework availability",
        "",
        *frameworks_note,
        "",
        "XML summaries, parameter and return text, and exception comments are shown where the "
        "release source documents them. Nullability and default values are reflected from the "
        "released assembly signature. Ownership and thread-safety claims appear only when the "
        "package documentation states them; undocumented behavior is not inferred.",
        "",
    ]
    (site_root / "index.md").write_text("\n".join(index_lines), encoding="utf-8")

    assembly_paths = [
        path.relative_to(site_root).as_posix()
        for package in package_rows
        for path in package_assemblies[package["packageId"]]
        if site_root in path.parents
    ]
    assembly_paths.extend(path.relative_to(site_root).as_posix() for path in dependency_assemblies)
    if not assembly_paths:
        raise ValueError(f"No released package assemblies were staged for {framework}.")

    config = {
        "metadata": [
            {
                "src": [{"files": ["packages/**/*.dll"]}],
                "dest": "api",
                "references": assembly_paths,
                "disableGitFeatures": True,
                "disableDefaultFilter": False,
                "includePrivateMembers": False,
            }
        ],
        "build": {
            "content": ["api/**/*.yml", "index.md"],
            "output": "_site",
            "globalMetadata": {
                "_appName": "VersaTul API",
                "_appTitle": f"VersaTul API Reference ({framework})",
                "_appFooter": "VersaTul generated API reference",
                "_enableSearch": True,
            },
            "postProcessors": ["ExtractSearchIndex"],
        },
    }
    (site_root / "docfx.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )

    for command in (("dotnet", "docfx", "metadata", "docfx.json"), ("dotnet", "docfx", "build", "docfx.json")):
        print(f"Running {' '.join(command)} ({framework})", flush=True)
        subprocess.run(command, cwd=site_root, check=True)

    output_root = site_root / "_site"
    xrefmap_path = output_root / "xrefmap.yml"
    search_index_path = output_root / "index.json"
    if not (output_root / "index.html").is_file():
        raise ValueError(f"DocFX did not generate an index page for {framework}.")
    if not search_index_path.is_file():
        raise ValueError(f"DocFX did not generate its full-text search index for {framework}.")
    if not xrefmap_path.is_file():
        raise ValueError(f"DocFX did not generate an xref map for {framework}.")

    references = parse_xrefmap(xrefmap_path)
    local_api = [reference for reference in references if reference["href"].startswith("api/")]
    if not local_api:
        raise ValueError(f"DocFX generated no local API links for {framework}.")
    public_types = [
        reference
        for reference in local_api
        if reference.get("commentId", "").startswith("T:")
    ]
    if not public_types:
        raise ValueError(f"DocFX generated no public types for {framework}.")
    forbidden = [
        reference["uid"]
        for reference in public_types
        if re.search(r"(?:^|\.)(?:Host|Test)(?:\.|$)", reference["uid"])
    ]
    if forbidden:
        raise ValueError(f"Host or test types appeared in {framework} API output: {forbidden[:10]}")

    search_payload = json.dumps(read_json(search_index_path), ensure_ascii=False).casefold()
    missing_search = []
    missing_pages = []
    for reference in public_types:
        type_name = reference["uid"].split(".")[-1].split("+")[-1].split("`")[0]
        if type_name.casefold() not in search_payload:
            missing_search.append(reference["uid"])
        page_path = output_root / reference["href"].split("#", 1)[0]
        if not page_path.is_file():
            missing_pages.append(reference["uid"])
    if missing_pages:
        raise ValueError(f"DocFX type pages are missing for {framework}: {missing_pages[:10]}")
    if missing_search:
        raise ValueError(
            f"Public types are absent from the DocFX full-text search index for {framework}: "
            f"{missing_search[:10]}"
        )
    print(
        f"{framework}: {len(public_types)} public types appear in API pages and search index.",
        flush=True,
    )
    return output_root, references


def render_package_api_fragment(
    package: dict,
    page_path: Path,
    references_by_framework: dict[str, list[dict[str, str]]],
) -> list[str]:
    package_id = package["packageId"]
    package_namespace = package_id + "."
    page_text = page_path.read_text(encoding="utf-8").casefold()
    page_label = "`{} {}`".format(package_id, package["version"])
    lines = [
        "Generated API reference",
        "^^^^^^^^^^^^^^^^^^^^^^^",
        "",
        f"The current published surface is {page_label}. This package's links use that exact "
        f"version; links to related packages use their independently listed release versions.",
        "",
        f"The matching DocsVersaTul snapshot is `{DOCS_RELEASE} "
        f"<{package['documentationUrl']}>`_.",
        "",
    ]
    for framework in package["frameworks"]:
        references = references_by_framework[framework]
        package_references = [
            reference
            for reference in references
            if reference.get("commentId", "").startswith("T:")
            and reference["uid"].startswith(package_namespace)
        ]
        if not package_references:
            raise ValueError(f"No public API types were found for {package_id} ({framework}).")
        lines.append(
            f"* Browse this package's `{framework} API reference "
            f"<{PUBLIC_DOCS_BASE}/_api_ref/{framework}/index.html>`_."
        )

        def match_types(candidates: list[dict[str, str]]) -> list[tuple[int, str, dict[str, str]]]:
            matches: list[tuple[int, str, dict[str, str]]] = []
            for reference in candidates:
                simple_name = reference["uid"].split(".")[-1].split("+")[-1].split("`")[0]
                match = re.search(
                    rf"(?<![a-z0-9_]){re.escape(simple_name.casefold())}(?![a-z0-9_])",
                    page_text,
                )
                if match:
                    matches.append((match.start(), simple_name, reference))
            matches.sort(key=lambda candidate: candidate[0])
            return matches

        own_matches = match_types(package_references)
        if not own_matches:
            raise ValueError(f"No public type name from {package_id} appears in its conceptual guide.")
        own_uids = {reference["uid"] for reference in package_references}
        related_matches = match_types(
            [
                reference
                for reference in references
                if reference.get("commentId", "").startswith("T:")
                and reference["href"].startswith("api/")
                and reference["uid"] not in own_uids
            ]
        )
        candidates = own_matches + related_matches

        chosen_types: list[dict[str, str]] = []
        chosen_names: set[str] = set()
        for _, simple_name, reference in candidates:
            if simple_name in chosen_names:
                continue
            chosen_types.append(reference)
            chosen_names.add(simple_name)
            if len(chosen_types) == 5:
                break

        lines.append("")
        lines.append(f"Key {framework} API entries used by this package guide:")
        lines.append("")
        for reference in chosen_types:
            simple_name = reference["uid"].split(".")[-1].split("+")[-1].split("`")[0]
            url = f"{PUBLIC_DOCS_BASE}/_api_ref/{framework}/{reference['href']}"
            lines.append(f"* `{simple_name} <{url}>`_")
            type_prefix = reference["uid"] + "."
            member_links: list[tuple[int, dict[str, str], str]] = []
            for member in references:
                comment_id = member.get("commentId", "")
                uid = member["uid"]
                if not comment_id.startswith(("M:", "P:", "F:", "E:")) or not uid.startswith(type_prefix):
                    continue
                member_name = uid[len(type_prefix) :].split("(", 1)[0].split(".", 1)[0]
                member_name = member_name.split("`")[0]
                if not member_name or member_name.startswith("#ctor"):
                    continue
                match = re.search(
                    rf"(?<![a-z0-9_]){re.escape(member_name.casefold())}(?![a-z0-9_])",
                    page_text,
                )
                if match:
                    member_links.append((match.start(), member, member_name))
            member_links.sort(key=lambda item: item[0])
            seen_members: set[str] = set()
            for _, member, member_name in member_links:
                if member_name in seen_members:
                    continue
                seen_members.add(member_name)
                lines.append(
                    f"  * `{simple_name}.{member_name} "
                    f"<{PUBLIC_DOCS_BASE}/_api_ref/{framework}/{member['href']}>`_"
                )
                if len(seen_members) == 3:
                    break
        lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--package-cache",
        type=Path,
        help="Existing directory of exact-version .nupkg files; defaults to docs/build/api-reference/packages.",
    )
    args = parser.parse_args()

    inventory, status_by_id, manifest_by_id = load_release_inputs()
    BUILD_ROOT.mkdir(parents=True, exist_ok=True)
    package_cache = args.package_cache or (BUILD_ROOT / "packages")
    package_cache = package_cache.resolve()
    package_cache.mkdir(parents=True, exist_ok=True)

    # Each run gets an isolated staging tree. The build output is copied into the
    # Sphinx extra-path only after both TFM sites and every validation succeeds.
    stage_root = BUILD_ROOT / "staging"
    if stage_root.exists():
        shutil.rmtree(stage_root)
    stage_root.mkdir(parents=True)
    candidate_root = stage_root / "published"
    candidate_root.mkdir()
    packages: list[dict] = []
    documented_by_framework: dict[str, set[str]] = {framework: set() for framework in FRAMEWORKS}
    xml_docs_by_framework: dict[str, set[str]] = {framework: set() for framework in FRAMEWORKS}
    package_assemblies: dict[str, list[Path]] = {package_id: [] for package_id in manifest_by_id}
    xml_assets_by_package_framework: dict[tuple[str, str], set[str]] = {}

    for inventory_row in inventory:
        package_id = inventory_row["PackageId"]
        status = status_by_id[package_id]
        manifest_package = manifest_by_id[package_id]
        version = status["LastVerifiedVersion"]
        package_path = download_package(package_id, version, package_cache)
        package_hash = sha256(package_path.read_bytes())
        if package_hash != manifest_package["packageSha256"]:
            raise ValueError(f"Exact NuGet package SHA256 mismatch for {package_id} {version}.")

        assets = manifest_package.get("assets")
        if not isinstance(assets, list) or not assets:
            raise ValueError(f"No released assembly assets are recorded for {package_id}.")
        package_frameworks: list[str] = []
        for asset in assets:
            framework = asset["targetFramework"]
            assembly_file = asset["assemblyFile"]
            if framework not in FRAMEWORKS:
                raise ValueError(f"Unsupported released TFM {framework} for {package_id}.")
            if not re.fullmatch(r"lib/[^/]+/[^/]+\.dll", assembly_file):
                raise ValueError(f"Unexpected package assembly path in manifest: {assembly_file}")
            if asset["assemblyFile"].split("/")[1] != framework:
                raise ValueError(f"Assembly path and framework disagree for {package_id}.")
            package_frameworks.append(framework)
            xml_relative = asset["xmlFile"]
            if Path(xml_relative).is_absolute() or ".." in Path(xml_relative).parts:
                raise ValueError(f"Unsafe XML documentation path in manifest: {xml_relative}")
            xml_path = REPOSITORY_ROOT / xml_relative
            documented = validate_xml_documentation(xml_path, asset["xmlSha256"])
            xml_docs_by_framework[framework].update(documented)
            xml_assets_by_package_framework[(package_id, framework)] = documented

            with zipfile.ZipFile(package_path) as package_archive:
                try:
                    assembly_bytes = package_archive.read(assembly_file)
                except KeyError as error:
                    raise ValueError(f"Released package {package_id} is missing {assembly_file}.") from error
            if sha256(assembly_bytes) != asset["assemblySha256"]:
                raise ValueError(f"Released DLL SHA256 mismatch for {package_id} {framework}.")
            assembly_dir = stage_root / framework / "packages" / package_id
            assembly_dir.mkdir(parents=True, exist_ok=True)
            assembly_path = assembly_dir / Path(assembly_file).name
            assembly_path.write_bytes(assembly_bytes)
            shutil.copyfile(xml_path, assembly_path.with_suffix(".xml"))
            package_assemblies[package_id].append(assembly_path)
            if framework not in documented_by_framework:
                continue
            package_frameworks.sort()

        package = {
            "packageId": package_id,
            "version": version,
            "packageUrl": status["VersionPageUrl"],
            "repositoryCommit": manifest_package["repositoryCommit"],
            "assets": assets,
            "frameworks": sorted(set(package_frameworks)),
            "pageName": inventory_row["PageName"],
            "documentationUrl": f"{PUBLIC_DOCS_BASE}/{inventory_row['PageName']}.html",
        }
        packages.append(package)

    references_by_framework: dict[str, list[dict[str, str]]] = {}
    sites_by_framework: dict[str, Path] = {}
    for framework in FRAMEWORKS:
        site_root = stage_root / framework
        site_root.mkdir(parents=True, exist_ok=True)
        dependency_assemblies = restore_framework_references(framework, packages, stage_root)
        site_output, references = build_docfx_site(
            framework,
            packages,
            stage_root,
            package_assemblies,
            dependency_assemblies,
        )
        sites_by_framework[framework] = site_output
        references_by_framework[framework] = references
        local_api = [reference for reference in references if reference["href"].startswith("api/")]
        for reference in local_api:
            comment_id = reference.get("commentId", "")
            if comment_id.startswith(("T:", "M:", "P:", "F:", "E:")):
                documented_by_framework[framework].add(comment_id)

        missing = sorted(documented_by_framework[framework] - xml_docs_by_framework[framework])
        BUILD_ROOT.mkdir(parents=True, exist_ok=True)
        coverage = {
            "framework": framework,
            "publicApiSymbolCount": len(documented_by_framework[framework]),
            "xmlDocumentedSymbolCount": len(
                documented_by_framework[framework] & xml_docs_by_framework[framework]
            ),
            "missingXmlMembers": missing,
            "packageVersions": [
                {"packageId": package["packageId"], "version": package["version"]}
                for package in packages
                if framework in package["frameworks"]
            ],
        }
        (BUILD_ROOT / f"xml-coverage-{framework}.json").write_text(
            json.dumps(coverage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(
            f"{framework}: {coverage['xmlDocumentedSymbolCount']}/"
            f"{coverage['publicApiSymbolCount']} public XML member IDs documented; "
            f"{len(missing)} missing (reported in docs/build/api-reference/xml-coverage-{framework}.json).",
            flush=True,
        )

    # Generate package-page links only from UIDs emitted by the exact release DLLs.
    fragments_root = stage_root / "_generated_api_links"
    fragments_root.mkdir()
    all_uids: set[str] = set()
    for references in references_by_framework.values():
        all_uids.update(reference["uid"] for reference in references if reference["href"].startswith("api/"))
    page_links_by_package: dict[str, list[str]] = {}
    for package in packages:
        framework = "net8.0"
        if framework not in package["frameworks"]:
            raise ValueError(f"Every released package must have a net8.0 direct asset: {package['packageId']}.")
        page_path = SOURCE_ROOT / f"{package['pageName']}.rst"
        fragment_lines = render_package_api_fragment(
            package,
            page_path,
            references_by_framework,
        )
        fragment_path = fragments_root / f"{package['pageName']}.rst"
        fragment_path.write_text("\n".join(fragment_lines), encoding="utf-8")
        page_links_by_package[package["packageId"]] = fragment_lines
        if not set(reference["uid"] for reference in references_by_framework[framework] if reference["href"].startswith("api/")):
            raise ValueError("DocFX emitted no linked API UIDs.")

    versions_lines = [
        "Released package versions represented by this generated reference",
        "--------------------------------------------------------------------",
        "",
        "Each NuGet package is versioned independently. The docs link is the site snapshot "
        "that documents the exact package version used to build the signatures and XML comments.",
        "",
        ".. list-table:: Released package API versions and direct target frameworks",
        "   :header-rows: 1",
        "",
        "   * - Package",
        "     - NuGet version",
        "     - Matching docs snapshot",
        "     - Direct TFM assets",
    ]
    for package in packages:
        versions_lines.extend(
            [
                f"   * - `{package['packageId']}`",
                f"     - `{package['version']} <{package['packageUrl']}>`_",
                f"     - `{DOCS_RELEASE} <{package['documentationUrl']}>`_",
                f"     - {', '.join(f'``{tfm}``' for tfm in package['frameworks'])}",
            ]
        )
    versions_lines.append("")
    (stage_root / "_generated_api_versions.rst").write_text(
        "\n".join(versions_lines) + "\n", encoding="utf-8"
    )

    # Keep the assembled public site replace atomic from Sphinx's perspective.
    candidate_sites = candidate_root / "_api_ref"
    candidate_sites.mkdir()
    for framework, output_path in sites_by_framework.items():
        shutil.copytree(output_path, candidate_sites / framework)
    if GENERATED_ROOT.exists():
        if GENERATED_ROOT.resolve().parent != SOURCE_ROOT.resolve():
            raise ValueError(f"Refusing to replace API output outside docs/source: {GENERATED_ROOT}")
        shutil.rmtree(GENERATED_ROOT)
    shutil.move(str(candidate_sites), str(GENERATED_ROOT))

    generated_links_root = SOURCE_ROOT / "_generated_api_links"
    if generated_links_root.exists():
        if generated_links_root.resolve().parent != SOURCE_ROOT.resolve():
            raise ValueError(f"Refusing to replace generated links outside docs/source: {generated_links_root}")
        shutil.rmtree(generated_links_root)
    shutil.move(str(fragments_root), str(generated_links_root))
    generated_versions = SOURCE_ROOT / "_generated_api_versions.rst"
    shutil.copyfile(stage_root / "_generated_api_versions.rst", generated_versions)

    print(
        f"Generated API reference for {len(packages)} packages at "
        f"{GENERATED_ROOT.relative_to(REPOSITORY_ROOT)}.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print(f"API reference generation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
