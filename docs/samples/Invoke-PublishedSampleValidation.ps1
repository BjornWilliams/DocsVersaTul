param(
    [string[]]$TargetFrameworks = @('net8.0', 'net9.0', 'net10.0'),

    [string]$Configuration = 'Release'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$samplesRoot = $PSScriptRoot
$sampleNames = @(
    'GettingStarted',
    'FileImport',
    'DataExport',
    'SqlDataAccess',
    'FileLogging',
    'Caching',
    'MongoDB',
    'Mailer'
)
$projects = @(
    foreach ($sampleName in $sampleNames) {
        $projectPath = Join-Path (Join-Path $samplesRoot $sampleName) "$sampleName.csproj"
        $expectedOutputPath = Join-Path (Split-Path -Parent $projectPath) 'ExpectedOutput.txt'
        if (-not (Test-Path -LiteralPath $projectPath -PathType Leaf)) {
            throw "Documentation sample project was not found: $projectPath"
        }
        if (-not (Test-Path -LiteralPath $expectedOutputPath -PathType Leaf)) {
            throw "Expected output file was not found: $expectedOutputPath"
        }

        [xml]$projectXml = [System.IO.File]::ReadAllText($projectPath)
        $frameworkNode = $projectXml.SelectSingleNode("//*[local-name()='TargetFrameworks' or local-name()='TargetFramework']")
        $projectFrameworks = if ($frameworkNode) { @($frameworkNode.InnerText -split ';' | ForEach-Object { $_.Trim() }) } else { @() }
        $missingFrameworks = @($TargetFrameworks | Where-Object { $_ -notin $projectFrameworks })
        if ($missingFrameworks.Count -gt 0) {
            throw "Sample '$sampleName' does not target all requested frameworks: $($missingFrameworks -join ', ')."
        }

        [pscustomobject]@{
            Name = $sampleName
            Project = $projectPath
            ExpectedOutput = $expectedOutputPath
        }
    }
)

foreach ($sample in $projects) {
    Write-Host "Restoring $($sample.Name)..."
    & dotnet restore $sample.Project
    if ($LASTEXITCODE -ne 0) {
        throw "Restore failed for '$($sample.Name)' (exit code $LASTEXITCODE)."
    }

    Write-Host "Building $($sample.Name) for all declared target frameworks..."
    & dotnet build $sample.Project --configuration $Configuration --no-restore --nologo --verbosity quiet
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed for '$($sample.Name)' (exit code $LASTEXITCODE)."
    }

    $expected = ([System.IO.File]::ReadAllText($sample.ExpectedOutput) -replace "`r`n?", "`n").TrimEnd()
    foreach ($framework in $TargetFrameworks) {
        $actualLines = @(
            & dotnet run --project $sample.Project --configuration $Configuration --framework $framework --no-build --no-restore --verbosity quiet |
                ForEach-Object { [string]$_ }
        )
        $exitCode = $LASTEXITCODE
        if ($exitCode -ne 0) {
            throw "Execution failed for '$($sample.Name) ($framework)' (exit code $exitCode)."
        }

        $actual = ($actualLines -join "`n").TrimEnd()
        if ($actual -cne $expected) {
            throw "Output mismatch for '$($sample.Name) ($framework)'. Expected '$expected'; received '$actual'."
        }

        Write-Host "Passed $($sample.Name) ($framework): output matched $([System.IO.Path]::GetFileName($sample.ExpectedOutput))."
    }
}

Write-Host "All $($projects.Count) documentation samples passed on $($TargetFrameworks.Count) target frameworks."
