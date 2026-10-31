param(
    [string]$SourceRoot = (Join-Path $PSScriptRoot '..\source'),

    [switch]$RequirePseudocodeCaptions
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$resolvedSourceRoot = [System.IO.Path]::GetFullPath($SourceRoot)
$manifestPath = Join-Path $resolvedSourceRoot 'snippet-inventory.json'
$inventoryPagePath = Join-Path $resolvedSourceRoot 'snippet-inventory.rst'
foreach ($requiredPath in @($manifestPath, $inventoryPagePath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Documentation snippet inventory file was not found: $requiredPath"
    }
}

$manifest = [System.IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json
$allowedClassifications = @('compiled', 'executed', 'pseudocode', 'configuration-only')
$expectedById = @{}
foreach ($snippet in $manifest.snippets) {
    if ($snippet.classification -notin $allowedClassifications) {
        throw "Snippet '$($snippet.id)' has an unsupported classification '$($snippet.classification)'."
    }
    if ([string]::IsNullOrWhiteSpace([string]$snippet.verification)) {
        throw "Snippet '$($snippet.id)' has no verification note."
    }
    if ($expectedById.ContainsKey([string]$snippet.id)) {
        throw "Snippet inventory ID '$($snippet.id)' is duplicated."
    }
    $expectedById[[string]$snippet.id] = $snippet
}

$directivePattern = '^(?<indent>\s*)\.\.\s+(?<directive>code-block|sourcecode|code|literalinclude|parsed-literal)::\s*(?<argument>.*?)\s*$'
$actualSnippets = @(
    foreach ($file in Get-ChildItem -LiteralPath $resolvedSourceRoot -Recurse -File -Filter '*.rst' | Sort-Object FullName) {
        $relativeFile = [System.IO.Path]::GetRelativePath($resolvedSourceRoot, $file.FullName).Replace('\', '/')
        $lines = [System.IO.File]::ReadAllLines($file.FullName)
        $ordinal = 0
        for ($lineIndex = 0; $lineIndex -lt $lines.Length; $lineIndex++) {
            if ($lines[$lineIndex] -notmatch $directivePattern) {
                continue
            }

            $ordinal++
            $directiveMatch = $Matches
            $directiveIndent = $directiveMatch.indent.Length
            $caption = $null
            $insideOptions = $false
            for ($optionIndex = $lineIndex + 1; $optionIndex -lt $lines.Length; $optionIndex++) {
                $optionLine = $lines[$optionIndex]
                if ([string]::IsNullOrWhiteSpace($optionLine)) {
                    if ($insideOptions) { break }
                    continue
                }
                $optionIndent = $optionLine.Length - $optionLine.TrimStart().Length
                if ($optionIndent -le $directiveIndent) { break }
                if ($optionLine -match '^\s*:caption:\s*(?<caption>.*)$') {
                    $caption = $Matches.caption.Trim()
                    $insideOptions = $true
                    continue
                }
                if ($optionLine -match '^\s+:[A-Za-z][A-Za-z0-9_-]*(?::|\s)') {
                    $insideOptions = $true
                    continue
                }
                break
            }

            [pscustomobject]@{
                Id = "$relativeFile#$ordinal"
                File = $relativeFile
                Ordinal = $ordinal
                Directive = $directiveMatch.directive
                Argument = $directiveMatch.argument.Trim()
                Caption = $caption
            }
        }
    }
)

$actualById = @{}
foreach ($snippet in $actualSnippets) {
    $actualById[$snippet.Id] = $snippet
}
$missingFromManifest = @($actualSnippets | Where-Object { -not $expectedById.ContainsKey($_.Id) })
$missingFromDocs = @($manifest.snippets | Where-Object { -not $actualById.ContainsKey([string]$_.id) })
if ($missingFromManifest.Count -gt 0 -or $missingFromDocs.Count -gt 0) {
    $untracked = @($missingFromManifest | ForEach-Object { $_.Id }) -join ', '
    $stale = @($missingFromDocs | ForEach-Object { $_.id }) -join ', '
    throw "Snippet inventory does not match the reStructuredText directives. Untracked: [$untracked]. Stale: [$stale]."
}

foreach ($snippet in $actualSnippets) {
    $expected = $expectedById[$snippet.Id]
    if ($snippet.File -cne [string]$expected.file -or
        $snippet.Ordinal -ne [int]$expected.ordinal -or
        $snippet.Directive -cne [string]$expected.directive -or
        $snippet.Argument -cne [string]$expected.argument) {
        throw "Snippet inventory metadata is stale for '$($snippet.Id)'."
    }
    if ($expected.classification -eq 'pseudocode' -and
        ($snippet.Directive -cne 'code-block' -or $snippet.Argument -cne 'csharp')) {
        throw "Only C# code blocks may be classified as pseudocode: '$($snippet.Id)'."
    }
    if ($expected.classification -eq 'executed' -and
        ($snippet.Directive -cne 'literalinclude' -or $snippet.Argument -notmatch '(Program\.cs|ExpectedOutput\.txt)$')) {
        throw "Executed entries must refer to a canonical program or asserted output file: '$($snippet.Id)'."
    }
    if ($RequirePseudocodeCaptions -and $expected.classification -eq 'pseudocode' -and
        $snippet.Caption -notmatch '^Pseudocode:') {
        throw "Pseudocode snippet '$($snippet.Id)' needs a visible 'Pseudocode:' code-block caption."
    }
}

$inventoryPage = [System.IO.File]::ReadAllText($inventoryPagePath)
$inventoryLines = [System.IO.File]::ReadAllLines($inventoryPagePath)
foreach ($snippet in $manifest.snippets) {
    $idText = '``{0}``' -f [string]$snippet.id
    $occurrences = [regex]::Matches($inventoryPage, [regex]::Escape($idText)).Count
    if ($occurrences -ne 1) {
        throw "Human-readable inventory must contain '$($snippet.id)' exactly once; found $occurrences."
    }

    $classificationLabel = switch ([string]$snippet.classification) {
        'compiled' { '**Compiled**' }
        'executed' { '**Executed**' }
        'pseudocode' { '**Pseudocode**' }
        'configuration-only' { '**Configuration-only**' }
    }
    $locationRow = '   * - {0}' -f $idText
    $locationRowIndex = [Array]::IndexOf($inventoryLines, $locationRow)
    if ($locationRowIndex -lt 0 -or
        $locationRowIndex + 2 -ge $inventoryLines.Length -or
        $inventoryLines[$locationRowIndex + 2].Trim() -cne ('- ' + $classificationLabel)) {
        throw "Human-readable inventory has a missing or incorrect classification row for '$($snippet.id)'."
    }
}

$counts = @(
    foreach ($classification in $allowedClassifications) {
        [pscustomobject]@{
            Classification = $classification
            Count = @($manifest.snippets | Where-Object classification -eq $classification).Count
        }
    }
)
Write-Host ("Documentation snippet inventory passed: {0} directives. {1}" -f $manifest.snippets.Count, (($counts | ForEach-Object { "$($_.Classification)=$($_.Count)" }) -join ', '))
