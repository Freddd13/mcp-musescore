[CmdletBinding(SupportsShouldProcess)]
param(
    [ValidateSet('User', 'Project')] [string]$Scope = 'User',
    [switch]$SkipEnvironment,
    [switch]$SkipMcp,
    [switch]$SkipSkill
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$taskRepo = Split-Path -Parent $PSScriptRoot
$taskPython = Join-Path $taskRepo '.venv\Scripts\python.exe'
$taskSkillSource = Join-Path $taskRepo 'skills\mcp-musescore'
$taskSkillRoot = if ($Scope -eq 'User') { Join-Path $HOME '.agents\skills' } else { Join-Path $taskRepo '.agents\skills' }
$taskSkillTarget = Join-Path $taskSkillRoot 'mcp-musescore'
if (-not $SkipEnvironment -and $PSCmdlet.ShouldProcess($taskRepo, 'Create Python 3.13 venv and install MCP dependencies')) {
    $taskUv = (Get-Command uv -ErrorAction Stop).Source
    $taskPreviousCache = $env:UV_CACHE_DIR
    $taskPreviousPythonDir = $env:UV_PYTHON_INSTALL_DIR
    try {
        $env:UV_CACHE_DIR = Join-Path $taskRepo '.cache\uv'
        $env:UV_PYTHON_INSTALL_DIR = Join-Path $taskRepo '.cache\python'
        if (-not (Test-Path -LiteralPath $taskPython)) {
            & $taskUv venv --python 3.13 (Join-Path $taskRepo '.venv')
            if ($LASTEXITCODE -ne 0) { throw 'uv venv failed' }
        }
        & $taskUv pip install --python $taskPython -r (Join-Path $taskRepo 'requirements.txt')
        if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
        Push-Location $taskRepo
        try {
            & $taskPython -c 'import server'
            if ($LASTEXITCODE -ne 0) { throw 'Server import failed' }
        } finally { Pop-Location }
    } finally {
        $env:UV_CACHE_DIR = $taskPreviousCache
        $env:UV_PYTHON_INSTALL_DIR = $taskPreviousPythonDir
    }
}
if (-not $SkipMcp -and $PSCmdlet.ShouldProcess('Codex user config', 'Register musescore stdio server (replaces this named entry only)')) {
    if (-not (Test-Path -LiteralPath $taskPython)) { throw "Missing environment: $taskPython" }
    & codex mcp add musescore --env "MCP_MUSESCORE_DIR=$taskRepo" -- $taskPython (Join-Path $taskRepo 'server.py')
    if ($LASTEXITCODE -ne 0) { throw 'Codex MCP registration failed' }
}
if (-not $SkipSkill -and $PSCmdlet.ShouldProcess($taskSkillTarget, 'Install the Codex skill, preserving any existing copy in a backup')) {
    if (Test-Path -LiteralPath $taskSkillTarget) {
        $taskBackup = Join-Path $taskRepo ('.cache\skill-backups\' + [DateTime]::Now.ToString('yyyyMMdd-HHmmss-ffff'))
        New-Item -ItemType Directory -Path $taskBackup -Force | Out-Null
        Copy-Item -LiteralPath $taskSkillTarget -Destination $taskBackup -Recurse
        Write-Host "Previous skill backed up to $taskBackup"
    }
    New-Item -ItemType Directory -Path $taskSkillTarget -Force | Out-Null
    Get-ChildItem -LiteralPath $taskSkillSource | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $taskSkillTarget -Recurse -Force
    }
}
Write-Host "Repository: $taskRepo"
Write-Host "Skill target: $taskSkillTarget"
Write-Host 'Open MuseScore 3 Evolution, run Plugins > MuseScore API Server, then start a new Codex chat and invoke $mcp-musescore.'
