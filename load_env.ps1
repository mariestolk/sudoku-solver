# Loads variables from a .env file into the current PowerShell session.
# Usage: . .\load_env.ps1          (uses .env in the current directory)
#        . .\load_env.ps1 my.env   (uses a custom file)

param(
    [string]$EnvFile = ".env"
)

$path = Join-Path (Get-Location) $EnvFile

if (-not (Test-Path $path)) {
    Write-Warning "No $EnvFile file found at $path"
    return
}

Get-Content $path | ForEach-Object {
    $line = $_.Trim()
    if ($line -eq "" -or $line.StartsWith("#")) { return }
    if ($line -notmatch "^([^=]+)=(.*)$") { return }

    $key   = $Matches[1].Trim()
    $value = $Matches[2].Trim() -replace '^["'']|["'']$'  # strip surrounding quotes

    [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
    Write-Host "Loaded: $key"
}
