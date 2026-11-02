param(
    [Parameter(Mandatory = $true, ParameterSetName = 'Update')]
    [switch]$Update,

    [Parameter(Mandatory = $true, ParameterSetName = 'Check')]
    [switch]$Check,

    [string]$SourceRoot = (Join-Path $PSScriptRoot '..\source'),

    [string]$DocsRoot = (Join-Path $PSScriptRoot '..')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$resolvedSourceRoot = [System.IO.Path]::GetFullPath($SourceRoot)
$resolvedDocsRoot = [System.IO.Path]::GetFullPath($DocsRoot)
$manifestPath = Join-Path $resolvedSourceRoot 'snippet-inventory.json'
$inventoryPagePath = Join-Path $resolvedSourceRoot 'snippet-inventory.rst'
foreach ($requiredPath in @($manifestPath, $inventoryPagePath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Documentation snippet inventory file was not found: $requiredPath"
    }
}

$manifestText = [System.IO.File]::ReadAllText($manifestPath)
$manifest = $manifestText | ConvertFrom-Json -AsHashtable
$existingById = @{}
foreach ($snippet in $manifest.snippets) {
    if ($existingById.ContainsKey([string]$snippet.id)) {
        throw "Snippet inventory ID '$($snippet.id)' is duplicated."
    }
    $existingById[[string]$snippet.id] = $snippet
}

$directivePattern = '^(?<indent>\s*)\.\.\s+(?<directive>code-block|sourcecode|code|literalinclude|parsed-literal)::\s*(?<argument>.*?)\s*$'
$actualSnippets = @(
    foreach ($file in Get-ChildItem -LiteralPath $resolvedSourceRoot -Recurse -File -Filter '*.rst' | Sort-Object FullName) {
        $relativeFile = [System.IO.Path]::GetRelativePath($resolvedSourceRoot, $file.FullName).Replace('\', '/')
        $lines = [System.IO.File]::ReadAllLines($file.FullName)
        $ordinal = 0
        $insideGeneratedQuickstart = $false
        for ($lineIndex = 0; $lineIndex -lt $lines.Length; $lineIndex++) {
            if ($lines[$lineIndex] -ceq '.. BEGIN VERSATUL GENERATED PACKAGE QUICKSTART') {
                $insideGeneratedQuickstart = $true
                continue
            }
            if ($lines[$lineIndex] -ceq '.. END VERSATUL GENERATED PACKAGE QUICKSTART') {
                $insideGeneratedQuickstart = $false
                continue
            }
            if ($lines[$lineIndex] -notmatch $directivePattern) {
                continue
            }

            $ordinal++
            $directive = $Matches.directive
            $argument = $Matches.argument.Trim()
            [pscustomobject]@{
                Id = "$relativeFile#$ordinal"
                File = $relativeFile
                Ordinal = $ordinal
                Directive = $directive
                Argument = $argument
                GeneratedQuickstart = $insideGeneratedQuickstart
            }
        }
    }
)

$records = @(
    foreach ($actual in $actualSnippets) {
        if ($existingById.ContainsKey($actual.Id)) {
            $existing = $existingById[$actual.Id]
            if ($actual.File -cne [string]$existing.file -or
                $actual.Ordinal -ne [int]$existing.ordinal -or
                $actual.Directive -cne [string]$existing.directive -or
                $actual.Argument -cne [string]$existing.argument) {
                throw "Existing snippet metadata changed for '$($actual.Id)'; update its verification classification deliberately before regenerating the inventory."
            }
            $classification = [string]$existing.classification
            $verification = [string]$existing.verification
        }
        else {
            $packageSampleMatch = [regex]::Match(
                $actual.Argument,
                '^(?:\.\./)?samples/Packages/(?<packageId>VersaTul\.[A-Za-z0-9.]+)/(?<file>Program\.cs|ExpectedOutput\.txt)$'
            )
            if ($actual.GeneratedQuickstart -and $actual.Directive -ceq 'code-block' -and $actual.Argument -ceq 'console') {
                $classification = 'configuration-only'
                $verification = 'Canonical dotnet install command displayed in the package quickstart; not compiled as C# source.'
            }
            elseif ($actual.Directive -ceq 'literalinclude' -and $packageSampleMatch.Success) {
                $packageId = $packageSampleMatch.Groups['packageId'].Value
                $sampleFile = $packageSampleMatch.Groups['file'].Value
                $samplePath = Join-Path (Join-Path (Join-Path $resolvedDocsRoot 'docs/samples/Packages') $packageId) $sampleFile
                if (-not (Test-Path -LiteralPath $samplePath -PathType Leaf)) {
                    throw "Canonical package snippet '$($actual.Id)' refers to a missing file: $samplePath"
                }

                $classification = 'executed'
                $verification = if ($sampleFile -ceq 'Program.cs') {
                    'Canonical package README sample is built and run for every supported framework; stdout is checked against ExpectedOutput.txt.'
                }
                else {
                    'Compared with stdout from the canonical package README sample after it is built and run for every supported framework.'
                }
            }
            else {
                throw "New snippet '$($actual.Id)' needs an explicit classification and verification note before inventory sync."
            }
        }

        [ordered]@{
            id = $actual.Id
            file = $actual.File
            ordinal = $actual.Ordinal
            directive = $actual.Directive
            argument = $actual.Argument
            classification = $classification
            verification = $verification
        }
    }
)

$actualIdSet = @{}
foreach ($record in $records) {
    $actualIdSet[[string]$record.id] = $true
}
$staleIds = @($existingById.Keys | Where-Object { -not $actualIdSet.ContainsKey($_) })
if ($Check -and $staleIds.Count -gt 0) {
    throw "Snippet inventory contains stale directive IDs: $($staleIds -join ', '). Run docs/scripts/Sync-DocumentationSnippetInventory.ps1 -Update after reviewing the source changes."
}

$manifest.snippets = $records
$jsonLineEnding = if ($manifestText.Contains("`r`n")) { "`r`n" } else { "`n" }
$updatedManifest = ($manifest | ConvertTo-Json -Depth 12) -replace '\r?\n', $jsonLineEnding
$updatedManifest = $updatedManifest.TrimEnd([char]"`r", [char]"`n") + $jsonLineEnding

$inventoryText = [System.IO.File]::ReadAllText($inventoryPagePath)
$inventoryLines = [System.IO.File]::ReadAllLines($inventoryPagePath)
$firstRowIndex = -1
for ($index = 0; $index -lt $inventoryLines.Length; $index++) {
    if ($inventoryLines[$index] -match '^\s+\* - ``[^`]+``\s*$') {
        $firstRowIndex = $index
        break
    }
}
if ($firstRowIndex -lt 0) {
    throw 'The human-readable snippet inventory is missing its first table row.'
}

$classificationLabels = @{
    compiled = '**Compiled**'
    executed = '**Executed**'
    pseudocode = '**Pseudocode**'
    'configuration-only' = '**Configuration-only**'
}
$tableRows = @(
    foreach ($record in $records) {
        if (-not $classificationLabels.ContainsKey([string]$record.classification)) {
            throw "Snippet '$($record.id)' has an unsupported classification '$($record.classification)'."
        }
        '   * - ``{0}``' -f [string]$record.id
        '     - ``{0}:: {1}``' -f [string]$record.directive, [string]$record.argument
        '     - {0}' -f $classificationLabels[[string]$record.classification]
        '     - {0}' -f [string]$record.verification
    }
)
$rstLineEnding = if ($inventoryText.Contains("`r`n")) { "`r`n" } else { "`n" }
$prefix = @($inventoryLines[0..($firstRowIndex - 1)]) -join $rstLineEnding
$updatedInventory = $prefix + $rstLineEnding + ($tableRows -join $rstLineEnding) + $rstLineEnding

if ($Check) {
    if ($updatedManifest -cne $manifestText -or $updatedInventory -cne $inventoryText) {
        throw 'The human-readable and machine-readable snippet inventories are stale. Run docs/scripts/Sync-DocumentationSnippetInventory.ps1 -Update after reviewing the source changes.'
    }
    Write-Output "Snippet inventory is current for $($records.Count) RST directives."
    return
}

if ($updatedManifest -cne $manifestText) {
    [System.IO.File]::WriteAllText($manifestPath, $updatedManifest, [System.Text.UTF8Encoding]::new($false))
}
if ($updatedInventory -cne $inventoryText) {
    [System.IO.File]::WriteAllText($inventoryPagePath, $updatedInventory, [System.Text.UTF8Encoding]::new($false))
}
Write-Output "Synchronized the snippet manifest and human-readable inventory for $($records.Count) RST directives."
