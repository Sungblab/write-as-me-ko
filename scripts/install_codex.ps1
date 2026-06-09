param(
    [switch]$Force,
    [string]$CodexHome = "$HOME\.codex"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Source = Join-Path $RepoRoot "codex\skills\write-as-me-ko"
$DestRoot = Join-Path $CodexHome "skills"
$Dest = Join-Path $DestRoot "write-as-me-ko"

if (-not (Test-Path $Source)) {
    throw "Skill source not found: $Source"
}

New-Item -ItemType Directory -Force -Path $DestRoot | Out-Null

if (Test-Path $Dest) {
    if (-not $Force) {
        throw "Destination already exists: $Dest. Re-run with -Force to replace it."
    }
    Remove-Item -Recurse -Force -LiteralPath $Dest
}

Copy-Item -Recurse -Force -LiteralPath $Source -Destination $Dest
Write-Host "Installed write-as-me-ko Codex skill to $Dest"

