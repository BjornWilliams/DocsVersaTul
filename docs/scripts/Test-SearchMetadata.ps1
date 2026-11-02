[CmdletBinding()]
param(
    [string]$HtmlRoot,
    [string]$ExpectedBaseUrl = 'https://docsversatul.readthedocs.io/en/latest/'
)

$ErrorActionPreference = 'Stop'
$repositoryRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
if (-not $PSBoundParameters.ContainsKey('HtmlRoot')) {
    $HtmlRoot = Join-Path $repositoryRoot 'docs/build/html'
}

$inventoryPath = Join-Path $repositoryRoot 'docs/source/package-inventory.json'
$metadataPath = Join-Path $repositoryRoot 'docs/source/seo-metadata.json'
$socialImagePath = Join-Path $repositoryRoot 'docs/source/_static/versatul-social-preview.png'
$socialImageOutputPath = Join-Path $HtmlRoot '_static/versatul-social-preview.png'
$sitemapPath = Join-Path $HtmlRoot 'sitemap-pages.xml'
$robotsPath = Join-Path $HtmlRoot 'robots.txt'
$ExpectedBaseUrl = $ExpectedBaseUrl.TrimEnd('/') + '/'
if (-not (Test-Path -LiteralPath $socialImagePath)) {
    throw "Social preview image does not exist: $socialImagePath"
}
foreach ($requiredPath in @($HtmlRoot, $inventoryPath, $metadataPath, $socialImageOutputPath, $sitemapPath, $robotsPath)) {
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
$packageUrls = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
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
    $structuredDataMatch = [regex]::Match($html, '<script\s+type="application/ld\+json">(?<value>.*?)</script>', [System.Text.RegularExpressions.RegexOptions]::Singleline -bor [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if (-not $titleMatch.Success -or -not $descriptionMatch.Success -or -not $ogTitleMatch.Success -or -not $ogDescriptionMatch.Success -or -not $ogUrlMatch.Success -or -not $ogImageMatch.Success -or -not $canonicalMatch.Success -or -not $twitterCardMatch.Success -or -not $structuredDataMatch.Success) {
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
    $canonicalUrl = [System.Net.WebUtility]::HtmlDecode($canonicalMatch.Groups['value'].Value)
    $expectedCanonicalUrl = $ExpectedBaseUrl + $package.PageName + '.html'
    if ($canonicalUrl -ne $expectedCanonicalUrl) {
        throw "Unexpected canonical URL for $($package.PageName): $canonicalUrl"
    }
    $structuredData = $structuredDataMatch.Groups['value'].Value | ConvertFrom-Json
    if ($structuredData.'@context' -ne 'https://schema.org' -or $structuredData.'@type' -ne 'BreadcrumbList' -or $structuredData.itemListElement.Count -ne 2) {
        throw "Expected a two-level schema.org BreadcrumbList for $($package.PageName)."
    }
    if ($structuredData.itemListElement[0].position -ne 1 -or $structuredData.itemListElement[0].name -ne 'Home' -or
        $structuredData.itemListElement[1].position -ne 2 -or
        $structuredData.itemListElement[1].item -ne [System.Net.WebUtility]::HtmlDecode($canonicalMatch.Groups['value'].Value)) {
        throw "Breadcrumb structured data does not match the visible route and canonical URL for $($package.PageName)."
    }
    $socialImage = [System.Net.WebUtility]::HtmlDecode($ogImageMatch.Groups['value'].Value)
    $expectedSocialImage = $ExpectedBaseUrl + '_static/versatul-social-preview.png'
    if ($socialImage -ne $expectedSocialImage) {
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
    if (-not $packageUrls.Add($canonicalUrl)) {
        throw "Duplicate package canonical URL: $canonicalUrl"
    }
}

$sitemap = [System.Xml.XmlDocument]::new()
$sitemap.Load($sitemapPath)
$sitemapUrls = @($sitemap.SelectNodes('/*[local-name()="urlset"]/*[local-name()="url"]/*[local-name()="loc"]') | ForEach-Object { $_.InnerText })
if ($sitemapUrls.Count -eq 0) {
    throw 'Generated sitemap contains no URLs.'
}
$uniqueSitemapUrls = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($url in $sitemapUrls) {
    if (-not $url.StartsWith($ExpectedBaseUrl, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Sitemap URL is outside the expected canonical base URL: $url"
    }
    if (-not $uniqueSitemapUrls.Add($url)) {
        throw "Generated sitemap contains a duplicate URL: $url"
    }
}
foreach ($url in $packageUrls) {
    if (-not $uniqueSitemapUrls.Contains($url)) {
        throw "Package page is missing from the generated sitemap: $url"
    }
}
if ($uniqueSitemapUrls.Contains($ExpectedBaseUrl) -or $uniqueSitemapUrls.Contains($ExpectedBaseUrl + 'index.html')) {
    throw 'The documentation sitemap must leave the root document to Read the Docs and use its canonical URL.'
}

$robots = [System.IO.File]::ReadAllText($robotsPath)
if ($robots -notmatch '(?m)^User-agent: \*\s*$' -or $robots -notmatch '(?m)^Allow: /\s*$') {
    throw 'Generated robots.txt must allow crawlers to index documentation.'
}
$baseUri = [Uri]$ExpectedBaseUrl
$expectedRootSitemap = '{0}://{1}/sitemap.xml' -f $baseUri.Scheme, $baseUri.Authority
$expectedPageSitemap = $ExpectedBaseUrl + 'sitemap-pages.xml'
foreach ($expectedSitemap in @($expectedRootSitemap, $expectedPageSitemap)) {
    if ($robots -notmatch ('(?m)^Sitemap: ' + [regex]::Escape($expectedSitemap) + '\s*$')) {
        throw "Generated robots.txt is missing sitemap URL $expectedSitemap."
    }
}

Write-Output "Search metadata, social previews, structured data, robots.txt, and sitemap passed for $($packages.Count) package pages across $($sitemapUrls.Count) documentation URLs."
