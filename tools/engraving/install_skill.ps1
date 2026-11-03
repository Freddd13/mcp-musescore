[CmdletBinding()]
param(
    [string]$Repository = (Join-Path $PSScriptRoot '..\..'),
    [string]$Destination = (Join-Path $HOME '.agents\skills\piano-engraving')
)

$ErrorActionPreference = 'Stop'
$repoPath = (Resolve-Path -LiteralPath $Repository).Path
$skillSource = Join-Path $repoPath 'skills\piano-engraving'
if (-not (Test-Path -LiteralPath (Join-Path $skillSource 'SKILL.md') -PathType Leaf)) {
    throw "Skill source missing: $skillSource"
}
if (-not (Test-Path -LiteralPath (Join-Path $repoPath 'docs\engraving\README.md') -PathType Leaf)) {
    throw 'Keep the skill and its knowledge library in the same release folder.'
}
$skillTarget = [IO.Path]::GetFullPath($Destination)
$existing = Get-Item -LiteralPath $skillTarget -Force -ErrorAction SilentlyContinue
if ($null -ne $existing) {
    $pointsToSource = $false
    if ($existing.LinkType -in @('Junction', 'SymbolicLink')) {
        $resolved = $existing.ResolveLinkTarget($true)
        $pointsToSource = $null -ne $resolved -and
            [string]::Equals($resolved.FullName.TrimEnd('\'), $skillSource.TrimEnd('\'), [StringComparison]::OrdinalIgnoreCase)
    }
    if (-not $pointsToSource) {
        throw "Destination exists and is not linked to this skill; nothing overwritten: $skillTarget"
    }
    $action = 'already-linked'
} else {
    $parentPath = Split-Path -Parent $skillTarget
    if (-not (Test-Path -LiteralPath $parentPath -PathType Container)) {
        New-Item -ItemType Directory -Path $parentPath -Force | Out-Null
    }
    New-Item -ItemType Junction -Path $skillTarget -Target $skillSource | Out-Null
    $action = 'linked'
}
$installed = Get-Item -LiteralPath $skillTarget -Force
[PSCustomObject]@{
    action = $action
    path = $skillTarget
    source = $installed.ResolveLinkTarget($true).FullName
    version = (Select-String -LiteralPath (Join-Path $skillTarget 'SKILL.md') -Pattern '^\s+version:').Line.Trim()
    mcp_configuration_changed = $false
} | ConvertTo-Json
