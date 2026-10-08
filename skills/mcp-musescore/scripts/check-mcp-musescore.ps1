$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$checkoutDir = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$repoDir = if ($env:MCP_MUSESCORE_DIR) { $env:MCP_MUSESCORE_DIR } elseif (Test-Path (Join-Path $checkoutDir 'server.py')) { $checkoutDir } else { Join-Path $HOME "Downloads\mcp-musescore" }
$pythonBin = if ($env:MCP_MUSESCORE_PYTHON) { $env:MCP_MUSESCORE_PYTHON } else { Join-Path $repoDir ".venv\Scripts\python.exe" }

if (-not (Test-Path (Join-Path $repoDir "server.py"))) { throw "server.py not found in $repoDir" }
if (-not (Test-Path $pythonBin)) { throw "Python executable not found: $pythonBin" }

Push-Location $repoDir
try {
  & $pythonBin -m compileall -q server.py src
  if ($LASTEXITCODE -ne 0) { throw 'Python compilation failed' }
  & $pythonBin -c "import server; print('MCP server import OK')"
  if ($LASTEXITCODE -ne 0) { throw 'MCP server import failed' }
  & $pythonBin (Join-Path $scriptDir "probe-musescore-bridge.py")
  if ($LASTEXITCODE -ne 0) { throw 'MuseScore bridge probe failed' }
}
finally { Pop-Location }
