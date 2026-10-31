param(
    [string]$DocsRoot = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -LiteralPath $DocsRoot).Path
$sourceRoot = Join-Path $root 'docs/source'
$samplesRoot = Join-Path $root 'docs/samples/Packages'
$inventoryPath = Join-Path $sourceRoot 'package-inventory.json'
$versionStatusPath = Join-Path $sourceRoot 'package-version-status.json'
$inventoryPagePath = Join-Path $sourceRoot 'package-inventory.rst'
$indexPath = Join-Path $sourceRoot 'index.rst'

foreach ($path in @($sourceRoot, $samplesRoot, $inventoryPath, $versionStatusPath, $inventoryPagePath, $indexPath)) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Required package documentation asset was not found: $path"
    }
}

$entries = @([System.IO.File]::ReadAllText($inventoryPath) | ConvertFrom-Json)
$versionStatusEntries = @([System.IO.File]::ReadAllText($versionStatusPath) | ConvertFrom-Json)
if ($entries.Count -ne 25) {
    throw "Expected 25 package inventory entries; found $($entries.Count)."
}
if ($versionStatusEntries.Count -ne $entries.Count) {
    throw "Expected one package version status entry per package; found $($versionStatusEntries.Count)."
}

$packageIds = @($entries | ForEach-Object { [string]$_.PackageId })
if (@($packageIds | Where-Object { [string]::IsNullOrWhiteSpace($_) }).Count -gt 0 -or
    @($packageIds | Select-Object -Unique).Count -ne $packageIds.Count) {
    throw 'The package inventory contains a missing or duplicate PackageId.'
}

$expectedPages = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$versionStatusByPackage = @{}
foreach ($statusEntry in $versionStatusEntries) {
    $packageId = [string]$statusEntry.PackageId
    $version = [string]$statusEntry.LastVerifiedVersion
    $verifiedOn = [string]$statusEntry.VerifiedOn
    $source = [string]$statusEntry.VerificationSource
    $verifiedDate = [DateTime]::MinValue
    if ([string]::IsNullOrWhiteSpace($packageId) -or $versionStatusByPackage.ContainsKey($packageId) -or
        $version -notmatch '^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$' -or
        -not [DateTime]::TryParseExact($verifiedOn, 'yyyy-MM-dd', [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::None, [ref]$verifiedDate) -or
        [string]::IsNullOrWhiteSpace($source)) {
        throw "Package version status metadata is invalid or duplicated for '$packageId'."
    }
    if ($source -ceq 'NuGet Gallery') {
        if ([string]$statusEntry.VersionPageUrl -cne "https://www.nuget.org/packages/$packageId/$version") {
            throw "Package '$packageId' has an invalid NuGet version page URL."
        }
    }
    elseif ($null -ne $statusEntry.VersionPageUrl) {
        throw "Package '$packageId' must not link to an unverified version page."
    }
    $versionStatusByPackage[$packageId] = $statusEntry
}

$inventoryPage = [System.IO.File]::ReadAllText($inventoryPagePath)
foreach ($entry in $entries) {
    $packageId = [string]$entry.PackageId
    if (-not $versionStatusByPackage.ContainsKey($packageId)) {
        throw "Package '$packageId' is missing last-verified version metadata."
    }
    $versionStatus = $versionStatusByPackage[$packageId]
    $expectedProjectPath = "$packageId/$packageId.csproj"
    $expectedReadmePath = "$packageId/Assets/README.md"
    $expectedSamplePath = "docs/samples/Packages/$packageId/Program.cs"
    $expectedNuGetUrl = "https://www.nuget.org/packages/$packageId"
    if ($entry.ProjectPath -cne $expectedProjectPath -or $entry.ReadmePath -cne $expectedReadmePath -or
        $entry.SamplePath -cne $expectedSamplePath -or $entry.NuGetUrl -cne $expectedNuGetUrl) {
        throw "Package inventory paths or NuGet URL are inconsistent for '$packageId'."
    }

    $documentationUri = $null
    if (-not [uri]::TryCreate([string]$entry.DocumentationUrl, [System.UriKind]::Absolute, [ref]$documentationUri) -or
        $documentationUri.Scheme -ne 'https') {
        throw "Package '$packageId' has an invalid HTTPS documentation URL."
    }
    $expectedPageName = [System.IO.Path]::GetFileNameWithoutExtension($documentationUri.AbsolutePath)
    if ($entry.PageName -cne $expectedPageName -or -not $expectedPages.Add($expectedPageName)) {
        throw "Package '$packageId' maps to a missing or duplicate documentation page name '$($entry.PageName)'."
    }

    $frameworks = @($entry.TargetFrameworks | ForEach-Object { [string]$_ })
    if ($frameworks.Count -eq 0 -or @($frameworks | Where-Object { $_ -notmatch '^net\d+\.\d+$' }).Count -gt 0 -or
        @($frameworks | Select-Object -Unique).Count -ne $frameworks.Count) {
        throw "Package '$packageId' has a missing, malformed, or duplicated target framework list."
    }

    $pagePath = Join-Path $sourceRoot ($expectedPageName + '.rst')
    $programPath = Join-Path (Join-Path $samplesRoot $packageId) 'Program.cs'
    $outputPath = Join-Path (Join-Path $samplesRoot $packageId) 'ExpectedOutput.txt'
    foreach ($path in @($pagePath, $programPath, $outputPath)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
            throw "Package '$packageId' is missing a public documentation page or sample file: $path"
        }
    }

    $pageText = [System.IO.File]::ReadAllText($pagePath)
    $badgeBeginCount = [regex]::Matches($pageText, '(?m)^\.\. BEGIN VERSATUL GENERATED PACKAGE BADGES\r?$').Count
    $badgeEndCount = [regex]::Matches($pageText, '(?m)^\.\. END VERSATUL GENERATED PACKAGE BADGES\r?$').Count
    $expectedVersionBadge = "https://img.shields.io/nuget/v/${packageId}?logo=nuget&label=NuGet%20version"
    $expectedDownloadsBadge = "https://img.shields.io/nuget/dt/${packageId}?logo=nuget&label=NuGet%20downloads"
    $expectedNuGetTarget = "   :target: $expectedNuGetUrl"
    if ($badgeBeginCount -ne 1 -or $badgeEndCount -ne 1 -or
        -not $pageText.Contains($expectedVersionBadge, [System.StringComparison]::Ordinal) -or
        -not $pageText.Contains($expectedDownloadsBadge, [System.StringComparison]::Ordinal) -or
        -not $pageText.Contains('https://img.shields.io/badge/license-MIT-blue.svg', [System.StringComparison]::Ordinal) -or
        ([regex]::Matches($pageText, [regex]::Escape($expectedNuGetTarget))).Count -ne 3) {
        throw "Package page '$expectedPageName' is missing a version, download, or MIT badge with its NuGet target."
    }

    $statusBeginCount = [regex]::Matches($pageText, '(?m)^\.\. BEGIN VERSATUL GENERATED PACKAGE STATUS\r?$').Count
    $statusEndCount = [regex]::Matches($pageText, '(?m)^\.\. END VERSATUL GENERATED PACKAGE STATUS\r?$').Count
    $expectedMaintenance = '**Maintenance:** Community maintained; support is best-effort with no published response SLA.'
    $version = [string]$versionStatus.LastVerifiedVersion
    $verifiedOn = [string]$versionStatus.VerifiedOn
    $versionLine = if ([string]$versionStatus.VersionPageUrl) {
        "**Last verified published version:** ``$version`` on ``$verifiedOn`` (NuGet Gallery)."
    }
    else {
        "**Last version found in the local NuGet cache:** ``$version`` (checked ``$verifiedOn``)."
    }
    if ($statusBeginCount -ne 1 -or $statusEndCount -ne 1 -or
        -not $pageText.Contains($expectedMaintenance, [System.StringComparison]::Ordinal) -or
        -not $pageText.Contains($versionLine, [System.StringComparison]::Ordinal)) {
        throw "Package page '$expectedPageName' is missing its maintenance status or last-verified version."
    }
    $expectedVersionDetails = if ([string]$versionStatus.VersionPageUrl) {
        ('`NuGet version details <{0}>`_.' -f $versionStatus.VersionPageUrl)
    }
    if ([string]$versionStatus.VersionPageUrl -and
        -not $pageText.Contains($expectedVersionDetails, [System.StringComparison]::Ordinal)) {
        throw "Package page '$expectedPageName' is missing its verified NuGet version link."
    }
    if (-not [string]$versionStatus.VersionPageUrl -and
        -not $pageText.Contains("Verification note: $($versionStatus.VerificationSource). Use the NuGet badge above for the current listing.", [System.StringComparison]::Ordinal)) {
        throw "Package page '$expectedPageName' is missing the version verification limitation."
    }

    $programInclude = ".. literalinclude:: ../samples/Packages/$packageId/Program.cs"
    $outputInclude = ".. literalinclude:: ../samples/Packages/$packageId/ExpectedOutput.txt"
    if ([regex]::Matches($pageText, '(?m)^\.\. BEGIN VERSATUL GENERATED PACKAGE QUICKSTART\r?$').Count -ne 1 -or
        [regex]::Matches($pageText, '(?m)^\.\. END VERSATUL GENERATED PACKAGE QUICKSTART\r?$').Count -ne 1 -or
        -not $pageText.Contains($programInclude, [System.StringComparison]::Ordinal) -or
        -not $pageText.Contains($outputInclude, [System.StringComparison]::Ordinal) -or
        -not $pageText.Contains("dotnet add package $packageId", [System.StringComparison]::Ordinal)) {
        throw "Package page '$expectedPageName' is missing its generated install command or canonical sample includes."
    }

    foreach ($expectedValue in @($packageId, $expectedProjectPath, $expectedReadmePath, $expectedPageName, $expectedSamplePath, ($frameworks -join ', '), $expectedNuGetUrl)) {
        if (-not $inventoryPage.Contains($expectedValue, [System.StringComparison]::Ordinal)) {
            throw "The public package matrix is missing '$expectedValue' for '$packageId'."
        }
    }
}

$actualSampleDirectories = @(
    Get-ChildItem -LiteralPath $samplesRoot -Directory | ForEach-Object { $_.Name } | Sort-Object
)
$expectedSampleDirectories = @($packageIds | Sort-Object)
$missingSamples = @($expectedSampleDirectories | Where-Object { $_ -notin $actualSampleDirectories })
$orphanSamples = @($actualSampleDirectories | Where-Object { $_ -notin $expectedSampleDirectories })
if ($missingSamples.Count -gt 0 -or $orphanSamples.Count -gt 0) {
    throw "Package sample directories do not match the inventory (missing: $($missingSamples -join ', '); orphaned: $($orphanSamples -join ', '))."
}

$orphanedPages = @(
    Get-ChildItem -LiteralPath $sourceRoot -File -Filter '*.rst' | Where-Object {
        $pageText = [System.IO.File]::ReadAllText($_.FullName)
        $pageText -match '(?m)^\.\. BEGIN VERSATUL GENERATED PACKAGE QUICKSTART\r?$' -and -not $expectedPages.Contains($_.BaseName)
    } | ForEach-Object { $_.Name } | Sort-Object
)
if ($orphanedPages.Count -gt 0) {
    throw "Sphinx contains orphaned generated package pages: $($orphanedPages -join ', ')."
}

if ([System.IO.File]::ReadAllText($indexPath) -notmatch '(?m)^\s+package-inventory\s*$') {
    throw 'The public Sphinx index does not link to package-inventory.'
}

Write-Output "Package documentation assets passed: $($entries.Count) package mappings, badges, verified-version status, pages, samples, and NuGet links; no orphaned pages or samples."
