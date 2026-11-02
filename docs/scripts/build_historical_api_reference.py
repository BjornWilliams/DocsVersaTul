#!/usr/bin/env python3
"""Build exact API references for the explicitly retained historical package majors."""

from __future__ import annotations

import hashlib
import json
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
MANIFEST_PATH = SOURCE_ROOT / "historical-package-versions.json"
GENERATED_ROOT = SOURCE_ROOT / "_api_ref"
DOCS_RELEASE = (REPOSITORY_ROOT / "docs" / "RELEASE").read_text(encoding="utf-8").strip()
if not re.fullmatch(r"\d{4}\.\d{2}", DOCS_RELEASE):
    raise ValueError(f"Set docs/RELEASE to a dated YYYY.MM snapshot, found {DOCS_RELEASE!r}.")
PUBLIC_DOCS_BASE = f"https://docsversatul.readthedocs.io/en/{DOCS_RELEASE}"
TARGET_FRAMEWORK = "net6.0"
HISTORICAL_SITE = GENERATED_ROOT / TARGET_FRAMEWORK / "legacy"
GENERATED_LINKS_ROOT = SOURCE_ROOT / "_generated_historical_api_links"
GENERATED_VERSIONS_PATH = SOURCE_ROOT / "_generated_historical_api_versions.rst"


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def download_package(package: dict, cache_root: Path) -> Path:
    package_id = package["packageId"]
    version = package["version"]
    filename = f"{package_id.lower()}.{version}.nupkg"
    package_path = cache_root / filename
    if not package_path.is_file():
        package_url = (
            "https://api.nuget.org/v3-flatcontainer/"
            f"{package_id.lower()}/{version}/{filename}"
        )
        request = urllib.request.Request(
            package_url,
            headers={"User-Agent": "VersaTul-Docs-Historical-API-Reference/1.0"},
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = response.read()
        temporary_path = package_path.with_suffix(package_path.suffix + ".tmp")
        temporary_path.write_bytes(payload)
        temporary_path.replace(package_path)
    payload = package_path.read_bytes()
    if sha256(payload) != package["packageSha256"]:
        raise ValueError(
            f"Exact NuGet package SHA256 mismatch for {package_id} {version}."
        )
    return package_path


def read_package_metadata(package_path: Path, package: dict) -> tuple[str, list[dict[str, str]]]:
    with zipfile.ZipFile(package_path) as archive:
        nuspec_names = [name for name in archive.namelist() if name.lower().endswith(".nuspec")]
        if len(nuspec_names) != 1:
            raise ValueError(f"Expected one nuspec in {package_path.name}.")
        root = ET.fromstring(archive.read(nuspec_names[0]))
    metadata = root.find("{*}metadata")
    if metadata is None:
        raise ValueError(f"Package metadata is missing from {package_path.name}.")
    package_id = metadata.findtext("{*}id")
    version = metadata.findtext("{*}version")
    if package_id != package["packageId"] or version != package["version"]:
        raise ValueError(f"NuGet metadata disagrees with the history manifest for {package_path.name}.")
    description = " ".join((metadata.findtext("{*}description") or "").split())
    if not description:
        raise ValueError(f"Published description is missing from {package_path.name}.")

    dependencies: dict[str, str] = {}
    dependency_root = metadata.find("{*}dependencies")
    if dependency_root is not None:
        groups = dependency_root.findall("{*}group")
        if groups:
            matching_groups = [
                group for group in groups
                if group.get("targetFramework", "").casefold() == TARGET_FRAMEWORK
            ]
            if len(matching_groups) != 1:
                raise ValueError(
                    f"Expected one {TARGET_FRAMEWORK} dependency group in {package_path.name}."
                )
            dependency_nodes = matching_groups[0].findall("{*}dependency")
        else:
            dependency_nodes = dependency_root.findall("{*}dependency")

        for node in dependency_nodes:
            dependency_id = node.get("id")
            dependency_version = node.get("version")
            if not dependency_id or not dependency_version:
                raise ValueError(f"Incomplete dependency metadata in {package_path.name}.")
            # These published nuspecs use exact version tokens as minimums. Pin
            # those declared lower bounds in the temporary DocFX restore.
            match = re.search(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", dependency_version)
            if not match:
                raise ValueError(
                    f"Unsupported NuGet dependency range {dependency_version!r} "
                    f"for {dependency_id} in {package_path.name}."
                )
            dependencies[dependency_id] = match.group(0)
    return description, [{"packageId": key, "version": value} for key, value in sorted(dependencies.items())]


def load_manifest() -> tuple[list[dict], dict[str, str]]:
    manifest = read_json(MANIFEST_PATH)
    if not isinstance(manifest, dict) or manifest.get("schemaVersion") != 1:
        raise ValueError("Historical package version manifest is missing or unsupported.")
    if manifest.get("targetFramework") != TARGET_FRAMEWORK:
        raise ValueError(f"Historical package targets must be {TARGET_FRAMEWORK}.")
    package_rows = manifest.get("packages")
    if not isinstance(package_rows, list) or not package_rows:
        raise ValueError("Historical package version manifest has no packages.")
    package_ids: set[str] = set()
    for package in package_rows:
        package_id = package.get("packageId", "")
        version = package.get("version", "")
        if not re.fullmatch(r"VersaTul\.[A-Za-z0-9.]+", package_id):
            raise ValueError(f"Unexpected historical package ID: {package_id!r}.")
        if not re.fullmatch(r"1\.\d+\.\d+", version):
            raise ValueError(f"Only approved 1.x documentation lines may be listed: {package_id} {version}.")
        if package_id in package_ids:
            raise ValueError(f"Duplicate historical package ID: {package_id}.")
        package_ids.add(package_id)
        if package.get("packageUrl") != f"https://www.nuget.org/packages/{package_id}/{version}":
            raise ValueError(f"{package_id} does not link to its exact historical NuGet package.")
        if package.get("pageName") not in {"sql", "mssql"}:
            raise ValueError(f"No package documentation route is defined for {package_id}.")
        if package.get("assemblyFile") != f"lib/{TARGET_FRAMEWORK}/{package_id}.dll":
            raise ValueError(f"Unexpected historical assembly path for {package_id}.")
        if not re.fullmatch(r"[0-9a-f]{64}", package.get("packageSha256", "")):
            raise ValueError(f"{package_id} has no exact package SHA256.")

    return package_rows, {package["packageId"]: package["pageName"] for package in package_rows}


def restore_references(
    packages: list[dict],
    dependencies_by_package: dict[str, list[dict[str, str]]],
    stage_root: Path,
) -> list[Path]:
    probe_root = stage_root / "dependency-probe"
    probe_root.mkdir(parents=True, exist_ok=True)
    package_versions: dict[str, str] = {package["packageId"]: package["version"] for package in packages}
    for dependency_rows in dependencies_by_package.values():
        for dependency in dependency_rows:
            dependency_id = dependency["packageId"]
            existing_version = package_versions.get(dependency_id)
            if existing_version and existing_version != dependency["version"]:
                raise ValueError(
                    f"Historical dependency pin conflicts for {dependency_id}: "
                    f"{existing_version} vs {dependency['version']}."
                )
            package_versions[dependency_id] = dependency["version"]

    package_references = "\n".join(
        f'    <PackageReference Include="{package_id}" Version="{version}" />'
        for package_id, version in sorted(package_versions.items())
    )
    project = (
        '<Project Sdk="Microsoft.NET.Sdk">\n'
        "  <PropertyGroup>\n"
        f"    <TargetFramework>{TARGET_FRAMEWORK}</TargetFramework>\n"
        "    <NuGetAudit>false</NuGetAudit>\n"
        "  </PropertyGroup>\n"
        "  <ItemGroup>\n"
        f"{package_references}\n"
        "  </ItemGroup>\n"
        "</Project>\n"
    )
    project_path = probe_root / "HistoricalVersaTulApiReference.csproj"
    project_path.write_text(project, encoding="utf-8")
    print(f"Restoring the published {TARGET_FRAMEWORK} dependency minimums for historical packages.", flush=True)
    subprocess.run(
        ["dotnet", "restore", str(project_path), "--nologo", "--verbosity", "quiet"],
        cwd=probe_root,
        check=True,
    )

    assets = read_json(probe_root / "obj" / "project.assets.json")
    target = assets.get("targets", {}).get(TARGET_FRAMEWORK)
    if not isinstance(target, dict):
        raise ValueError(f"NuGet restore did not produce a {TARGET_FRAMEWORK} dependency target.")
    package_folders = [Path(folder) for folder in assets.get("packageFolders", {})]
    documented_ids = {package["packageId"].casefold() for package in packages}
    references_root = stage_root / TARGET_FRAMEWORK / "references"
    reference_paths: list[Path] = []
    for package_key, package_assets in target.items():
        package_id, separator, package_version = package_key.partition("/")
        if not separator or package_id.casefold() in documented_ids:
            continue
        if (
            package_id.casefold().startswith(("system.", "microsoft.netcore."))
            and package_id.casefold() != "system.data.sqlclient"
        ) or package_id.casefold() in {
            "microsoft.csharp",
            "netstandard.library",
        }:
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
                raise ValueError(f"NuGet restore asset is missing: {package_key}/{relative_asset}.")
            destination = references_root / package_id.casefold() / package_version.casefold() / relative_asset
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, destination)
            reference_paths.append(destination)
    if not reference_paths:
        raise ValueError(f"NuGet restore found no external references for {TARGET_FRAMEWORK}.")
    print(f"Restored {len(reference_paths)} historical dependency references.", flush=True)
    return reference_paths


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
    append_current()
    return references


def rst_link(label: str, url: str) -> str:
    return f"`{label} <{url}>`_"


def main() -> int:
    packages, page_names = load_manifest()
    BUILD_ROOT.mkdir(parents=True, exist_ok=True)
    cache_root = BUILD_ROOT / "historical-packages"
    cache_root.mkdir(parents=True, exist_ok=True)
    stage_root = BUILD_ROOT / "historical-staging"
    if stage_root.exists():
        shutil.rmtree(stage_root)
    package_root = stage_root / TARGET_FRAMEWORK / "packages"
    package_root.mkdir(parents=True)

    descriptions: dict[str, str] = {}
    dependencies_by_package: dict[str, list[dict[str, str]]] = {}
    assemblies: dict[str, Path] = {}
    for package in packages:
        package_path = download_package(package, cache_root)
        description, dependencies = read_package_metadata(package_path, package)
        descriptions[package["packageId"]] = description
        dependencies_by_package[package["packageId"]] = dependencies
        with zipfile.ZipFile(package_path) as archive:
            try:
                assembly_bytes = archive.read(package["assemblyFile"])
            except KeyError as error:
                raise ValueError(
                    f"Published package {package['packageId']} is missing {package['assemblyFile']}."
                ) from error
        destination = package_root / package["packageId"] / Path(package["assemblyFile"]).name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(assembly_bytes)
        assemblies[package["packageId"]] = destination

    dependency_assemblies = restore_references(packages, dependencies_by_package, stage_root)
    site_root = stage_root / TARGET_FRAMEWORK
    package_ids = {package["packageId"] for package in packages}
    assembly_paths = [
        path.relative_to(site_root).as_posix()
        for package_id, path in assemblies.items()
        if package_id in package_ids
    ]
    assembly_paths.extend(path.relative_to(site_root).as_posix() for path in dependency_assemblies)
    index_lines = [
        f"# VersaTul historical API reference ({TARGET_FRAMEWORK})",
        "",
        "This historical reference is generated from exact, checksum-verified NuGet assemblies. "
        "The retained package major is 1.x for the two packages listed below.",
        "",
        "The published 1.x packages target net6.0. Their NuGet packages do not include XML "
        "documentation sidecars or an embedded source commit, so this site reports API signatures "
        "from the exact assemblies without inventing member summaries or source history.",
        "",
        "The version-specific NuGet pages preserve each package's published description, framework "
        "metadata, and declared dependency minimums. Keeping this documentation available does not "
        "promise new package maintenance or releases for the 1.x lines.",
        "",
        "## Exact historical package versions",
        "",
    ]
    for package in packages:
        index_lines.extend(
            [
                f"### {package['packageId']} {package['version']}",
                "",
                f"- Published package and behavior description: [{package['version']}]({package['packageUrl']})",
                f"- Target framework: `{TARGET_FRAMEWORK}`",
                f"- Package hash: `{package['packageSha256']}`",
                f"- Dependency minimums from the package nuspec: "
                + (", ".join(f"`{dependency['packageId']} {dependency['version']} `" for dependency in dependencies_by_package[package['packageId']]) or "none"),
                "",
                "Published description:",
                "",
                f"> {descriptions[package['packageId']]}",
                "",
            ]
        )
    (site_root / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
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
                "_appTitle": f"VersaTul Historical API Reference ({TARGET_FRAMEWORK})",
                "_appFooter": "VersaTul historical package API reference",
                "_enableSearch": True,
            },
            "postProcessors": ["ExtractSearchIndex"],
        },
    }
    (site_root / "docfx.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    for command in (("dotnet", "docfx", "metadata", "docfx.json"), ("dotnet", "docfx", "build", "docfx.json")):
        print(f"Running {' '.join(command)} ({TARGET_FRAMEWORK} historical packages)", flush=True)
        subprocess.run(command, cwd=site_root, check=True)

    output_root = site_root / "_site"
    xrefmap_path = output_root / "xrefmap.yml"
    search_index_path = output_root / "index.json"
    if not (output_root / "index.html").is_file() or not xrefmap_path.is_file() or not search_index_path.is_file():
        raise ValueError("DocFX did not generate all required historical API files.")
    references = parse_xrefmap(xrefmap_path)
    public_types = [
        reference
        for reference in references
        if reference.get("commentId", "").startswith("T:")
        and any(reference["uid"].startswith(package_id + ".") for package_id in package_ids)
    ]
    for package_id in package_ids:
        package_types = [reference for reference in public_types if reference["uid"].startswith(package_id + ".")]
        if not package_types:
            raise ValueError(f"No public historical API types were generated for {package_id}.")
        missing_pages = [
            reference["uid"]
            for reference in package_types
            if not (output_root / reference["href"].split("#", 1)[0]).is_file()
        ]
        if missing_pages:
            raise ValueError(f"Historical API type pages are missing for {package_id}: {missing_pages[:10]}.")
    search_payload = json.dumps(read_json(search_index_path), ensure_ascii=False).casefold()
    missing_search = [
        reference["uid"]
        for reference in public_types
        if reference["uid"].split(".")[-1].split("+")[-1].split("`")[0].casefold() not in search_payload
    ]
    if missing_search:
        raise ValueError(f"Historical API types are absent from DocFX search: {missing_search[:10]}.")

    destination_root = HISTORICAL_SITE
    if destination_root.exists():
        if destination_root.resolve().parent != (GENERATED_ROOT / TARGET_FRAMEWORK).resolve():
            raise ValueError(f"Refusing to replace historical API output outside {GENERATED_ROOT}.")
        shutil.rmtree(destination_root)
    destination_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(output_root, destination_root)

    if GENERATED_LINKS_ROOT.exists():
        if GENERATED_LINKS_ROOT.resolve().parent != SOURCE_ROOT.resolve():
            raise ValueError(f"Refusing to replace generated history links outside {SOURCE_ROOT}.")
        shutil.rmtree(GENERATED_LINKS_ROOT)
    GENERATED_LINKS_ROOT.mkdir()
    version_lines = [
        "Historical 1.x package documentation",
        "-------------------------------------",
        "",
        "The following last-published 1.x versions are retained for exact historical API lookup. "
        "They are a documentation-availability choice, not a promise of active package maintenance.",
        "",
        "The API signatures come from the exact package assemblies; the version-specific NuGet pages "
        "contain the publisher's package descriptions and release metadata.",
        "",
        ".. list-table:: Retained older major package versions",
        "   :header-rows: 1",
        "",
        "   * - Package",
        "     - Exact version",
        "     - Published package and behavior description",
        "     - Matching API reference",
    ]
    for package in packages:
        package_id = package["packageId"]
        api_url = f"{PUBLIC_DOCS_BASE}/{TARGET_FRAMEWORK}/legacy/index.html"
        package_page_label = f"{package['version']} NuGet page"
        api_label = f"{TARGET_FRAMEWORK} signatures"
        version_lines.extend(
            [
                f"   * - ``{package_id}``",
                f"     - ``{package['version']}``",
                f"     - {rst_link(package_page_label, package['packageUrl'])}",
                f"     - {rst_link(api_label, api_url)}",
            ]
        )
        page_name = page_names[package_id]
        package_lines = [
            "Historical 1.x package reference",
            "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
            "",
            f"The retained 1.x release is `{package['version']}`. Open its exact "
            f"{rst_link('NuGet package page', package['packageUrl'])} for the published "
            "package description, framework metadata, and dependency minimums.",
            "",
            f"Browse its signatures in the matching {rst_link(f'{TARGET_FRAMEWORK} API reference', api_url)}.",
            "",
            "This is historical documentation availability. It does not promise new maintenance or releases for the 1.x line.",
            "",
        ]
        (GENERATED_LINKS_ROOT / f"{page_name}.rst").write_text("\n".join(package_lines), encoding="utf-8")
    GENERATED_VERSIONS_PATH.write_text("\n".join(version_lines) + "\n", encoding="utf-8")

    print(
        f"Generated exact 1.x API references for {len(packages)} packages at "
        f"{HISTORICAL_SITE.relative_to(REPOSITORY_ROOT)} ({len(public_types)} public types).",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print(f"Historical API reference generation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
