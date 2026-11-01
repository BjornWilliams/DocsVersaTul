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
$socialImagePath = Join-Path $repositoryRoot 'docs/source/_static/versatul-social-preview.png'
if (-not (Test-Path -LiteralPath $socialImagePath)) {
    throw "Social preview image does not exist: $socialImagePath"
}
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
    $ogTitleMatch = [regex]::Match($html, '<meta\s+property="og:title"\s+content="(?<value>[^"]*)"\s*/?>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $ogDescriptionMatch = [regex]::Match($html, '<meta\s+property="og:description"\s+content="(?<value>[^"]*)"\s*/?>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $ogUrlMatch = [regex]::Match($html, '<meta\s+property="og:url"\s+content="(?<value>[^"]*)"\s*/?>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $ogImageMatch = [regex]::Match($html, '<meta\s+property="og:image"\s+content="(?<value>[^"]*)"\s*/?>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $canonicalMatch = [regex]::Match($html, '<link\s+rel="canonical"\s+href="(?<value>[^"]*)"\s*/?>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $twitterCardMatch = [regex]::Match($html, '<meta\s+name="twitter:card"\s+content="(?<value>[^"]*)"\s*/?>', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if (-not $titleMatch.Success -or -not $descriptionMatch.Success -or -not $ogTitleMatch.Success -or -not $ogDescriptionMatch.Success -or -not $ogUrlMatch.Success -or -not $ogImageMatch.Success -or -not $canonicalMatch.Success -or -not $twitterCardMatch.Success) {
        throw "Rendered package page is missing search or social metadata: $pagePath"
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
    if ([System.Net.WebUtility]::HtmlDecode($ogTitleMatch.Groups['value'].Value) -ne $pageMetadata.title -or
        [System.Net.WebUtility]::HtmlDecode($ogDescriptionMatch.Groups['value'].Value) -ne $pageMetadata.description) {
        throw "Open Graph title or description differs from the page metadata for $($package.PageName)."
    }
    if ([System.Net.WebUtility]::HtmlDecode($ogUrlMatch.Groups['value'].Value) -ne [System.Net.WebUtility]::HtmlDecode($canonicalMatch.Groups['value'].Value)) {
        throw "Open Graph URL does not match the canonical URL for $($package.PageName)."
    }
    $socialImage = [System.Net.WebUtility]::HtmlDecode($ogImageMatch.Groups['value'].Value)
    if ($socialImage -notmatch '^https://[^/]+/.+/_static/versatul-social-preview\.png$') {
        throw "Open Graph image is not an absolute HTTPS brand asset for $($package.PageName): $socialImage"
    }
    if ([System.Net.WebUtility]::HtmlDecode($twitterCardMatch.Groups['value'].Value) -ne 'summary_large_image') {
        throw "Twitter card type is not summary_large_image for $($package.PageName)."
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

Write-Output "Search and social metadata passed for $($packages.Count) package pages."
