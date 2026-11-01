[CmdletBinding()]
param(
    [string]$HtmlRoot
)

$ErrorActionPreference = 'Stop'
$repositoryRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
if (-not $PSBoundParameters.ContainsKey('HtmlRoot')) {
    $HtmlRoot = Join-Path $repositoryRoot 'docs/build/html'
}

$inventoryPath = Join-Path $repositoryRoot 'docs/source/package-inventory.json'
$metadataPath = Join-Path $repositoryRoot 'docs/source/seo-metadata.json'
foreach ($requiredPath in @($HtmlRoot, $inventoryPath, $metadataPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Required search metadata input does not exist: $requiredPath"
    }
}

$packages = @(Get-Content -LiteralPath $inventoryPath -Raw | ConvertFrom-Json)
$metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json -AsHashtable
$packagePages = @($packages | ForEach-Object { $_.PageName } | Sort-Object -Unique)
$metadataPages = @($metadata.Keys | Sort-Object -Unique)
if (Compare-Object -ReferenceObject $packagePages -DifferenceObject $metadataPages) {
    throw 'SEO metadata page keys do not exactly match the package inventory.'
}

$titles = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$descriptions = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($package in $packages) {
    $pagePath = Join-Path $HtmlRoot ($package.PageName + '.html')
    if (-not (Test-Path -LiteralPath $pagePath)) {
        throw "Rendered package page does not exist: $pagePath"
    }

    $pageMetadata = $metadata[$package.PageName]
    if ($pageMetadata.packageId -ne $package.PackageId) {
        throw "SEO metadata package ID does not match the inventory for $($package.PageName)."
    }

    $html = [System.IO.File]::ReadAllText($pagePath)
    $titleMatch = [regex]::Match($html, '<title>(?<value>.*?)</title>', [System.Text.RegularExpressions.RegexOptions]::Singleline)
    $descriptionMatch = [regex]::Match($html, '<meta\s+name="description"\s+content="(?<value>[^"]*)"\s*/?>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if (-not $titleMatch.Success -or -not $descriptionMatch.Success) {
        throw "Rendered package page is missing a title or description: $pagePath"
    }

    $title = [System.Net.WebUtility]::HtmlDecode($titleMatch.Groups['value'].Value)
    $description = [System.Net.WebUtility]::HtmlDecode($descriptionMatch.Groups['value'].Value)
    $expectedTitle = $pageMetadata.title + ' — VersaTul Documentation'
    if ($title -ne $expectedTitle) {
        throw "Unexpected title for $($package.PageName): $title"
    }
    if ($description -ne $pageMetadata.description) {
        throw "Unexpected description for $($package.PageName)."
    }
    if ($title -notmatch [regex]::Escape($package.PackageId) -or $description -notmatch [regex]::Escape($package.PackageId)) {
        throw "The title and description must both include the exact package ID $($package.PackageId)."
    }
    if (-not $titles.Add($title)) {
        throw "Duplicate search title: $title"
    }
    if (-not $descriptions.Add($description)) {
        throw "Duplicate search description for $($package.PageName)."
    }
}

Write-Output "Search title and description metadata passed for $($packages.Count) package pages."
