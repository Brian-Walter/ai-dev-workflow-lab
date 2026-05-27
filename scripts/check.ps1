Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$VenvPath = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
$SupportedVersions = @("3.13", "3.12")

Set-Location $ProjectRoot

function Invoke-CommandChecked {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Command,

        [string[]] $Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

function Get-PythonVersion {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Command,

        [string[]] $Arguments = @()
    )

    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        return $null
    }

    $version = & $Command @Arguments -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($LASTEXITCODE -ne 0) {
        return $null
    }

    return $version.Trim()
}

function Test-SupportedVersion {
    param(
        [string] $Version
    )

    return $SupportedVersions -contains $Version
}

function Test-PythonModule {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Python,

        [Parameter(Mandatory = $true)]
        [string] $Module
    )

    $previousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $Python -m $Module --version *> $null
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = $previousErrorActionPreference

    return ($exitCode -eq 0)
}

function Test-PathInsideProject {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path
    )

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $projectPrefix = $ProjectRoot.TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar

    return $fullPath.StartsWith($projectPrefix, [System.StringComparison]::OrdinalIgnoreCase)
}

function Get-BasePython {
    $candidates = @(
        @{ Command = "py"; Arguments = @("-3.13"); Label = "Python 3.13 via py launcher" },
        @{ Command = "python"; Arguments = @(); Label = "Python 3.13 via python" },
        @{ Command = "py"; Arguments = @("-3.12"); Label = "Python 3.12 via py launcher" },
        @{ Command = "python"; Arguments = @(); Label = "Python 3.12 via python" }
    )

    foreach ($candidate in $candidates) {
        $version = Get-PythonVersion $candidate.Command $candidate.Arguments
        if ($version -eq "3.13" -and $candidate.Label -like "*3.13*") {
            return @{
                Command = $candidate.Command
                Arguments = $candidate.Arguments
                Version = $version
                Label = $candidate.Label
            }
        }

        if ($version -eq "3.12" -and $candidate.Label -like "*3.12*") {
            return @{
                Command = $candidate.Command
                Arguments = $candidate.Arguments
                Version = $version
                Label = $candidate.Label
            }
        }
    }

    return $null
}

function Initialize-VirtualEnvironment {
    $venvVersion = Get-PythonVersion $VenvPython
    if (Test-SupportedVersion $venvVersion) {
        Write-Host "Using existing .venv with Python $venvVersion"
        return
    }

    if (Test-Path -LiteralPath $VenvPath) {
        if (-not (Test-PathInsideProject $VenvPath)) {
            throw "Refusing to recreate .venv outside the project: $VenvPath"
        }

        if ($venvVersion) {
            Write-Host "Existing .venv uses unsupported Python $venvVersion. Recreating local .venv."
        }
        else {
            Write-Host "Existing .venv is broken or missing its Python executable. Recreating local .venv."
        }

        Remove-Item -LiteralPath $VenvPath -Recurse -Force
    }

    $basePython = Get-BasePython
    if (-not $basePython) {
        throw "Python 3.13 or 3.12 was not found. Install one of them and run this script again."
    }

    Write-Host "Creating .venv with $($basePython.Label)"
    Invoke-CommandChecked $basePython.Command -Arguments ($basePython.Arguments + @("-m", "venv", $VenvPath))
}

Initialize-VirtualEnvironment

if (-not (Test-PythonModule $VenvPython "pip")) {
    Write-Host "pip is missing in .venv. Bootstrapping pip with ensurepip."
    Invoke-CommandChecked $VenvPython -Arguments @("-m", "ensurepip", "--upgrade")
}

Invoke-CommandChecked $VenvPython -Arguments @("-m", "pip", "install", "-e", ".[dev]")
Invoke-CommandChecked $VenvPython -Arguments @("-m", "ruff", "check", ".")
Invoke-CommandChecked $VenvPython -Arguments @("-m", "pytest", "-q")
