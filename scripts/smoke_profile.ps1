$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $RepoRoot
try {
    python -m scripts.build_voice_profile --samples samples --output _workspace\voice-profile.smoke.md
    if (-not (Test-Path "_workspace\voice-profile.smoke.md")) {
        throw "Smoke output was not created."
    }
    python -m scripts.export_agent_context --output _workspace\AGENTS.write-as-me-ko.smoke.md
    if (-not (Test-Path "_workspace\AGENTS.write-as-me-ko.smoke.md")) {
        throw "Agent context smoke output was not created."
    }
    Write-Host "Smoke profile generated at _workspace\voice-profile.smoke.md"
    Write-Host "Smoke agent context generated at _workspace\AGENTS.write-as-me-ko.smoke.md"
}
finally {
    Pop-Location
}
