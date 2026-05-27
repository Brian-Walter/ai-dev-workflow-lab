Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-CheckCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Command,

        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]] $Arguments
    )

    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

function Invoke-PythonModule {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Command,

        [string[]] $PythonArguments = @(),

        [Parameter(Mandatory = $true)]
        [string] $Module,

        [string[]] $ModuleArguments = @()
    )

    & $Command @PythonArguments -m $Module @ModuleArguments
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

function Test-Executable {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $false
    }

    & $Path --version *> $null
    return ($LASTEXITCODE -eq 0)
}

function Test-StablePython {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Command,

        [string[]] $PythonArguments = @()
    )

    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        return $false
    }

    $version = & $Command @PythonArguments -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($LASTEXITCODE -ne 0) {
        return $false
    }

    return ($version -eq "3.13" -or $version -eq "3.12")
}

function Remove-BrokenVirtualEnvironment {
    param(
        [Parameter(Mandatory = $true)]
        [string] $VenvPath
    )

    $resolvedProject = (Resolve-Path -LiteralPath $PWD).Path
    $fullVenvPath = [System.IO.Path]::GetFullPath((Join-Path $PWD $VenvPath))

    if (-not $fullVenvPath.StartsWith($resolvedProject, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove virtual environment outside the project: $fullVenvPath"
    }

    $configPath = Join-Path $fullVenvPath "pyvenv.cfg"
    if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
        return
    }

    $config = Get-Content -LiteralPath $configPath
    $homeLine = $config | Where-Object { $_ -like "home = *" } | Select-Object -First 1
    $versionLine = $config | Where-Object { $_ -like "version_info = *" } | Select-Object -First 1

    $pythonHome = $null
    if ($homeLine) {
        $pythonHome = $homeLine.Substring("home = ".Length).Trim()
    }

    $pythonExecutable = $null
    if ($pythonHome) {
        $pythonExecutable = Join-Path $pythonHome "python.exe"
    }

    $usesUnstablePython = $versionLine -like "version_info = 3.14*"
    $hasBrokenPython = $pythonExecutable -and (-not (Test-Executable $pythonExecutable))

    if ($usesUnstablePython -or $hasBrokenPython) {
        Write-Host "Removing broken virtual environment at $fullVenvPath"
        Remove-Item -LiteralPath $fullVenvPath -Recurse -Force
    }
}

Remove-BrokenVirtualEnvironment ".venv"

if (Get-Command uv -ErrorAction SilentlyContinue) {
    $env:UV_CACHE_DIR = Join-Path $PWD ".uv-cache"
    $env:UV_PROJECT_ENVIRONMENT = Join-Path $PWD ".venv"
    $env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD ".uv-python"

    Invoke-CheckCommand uv run --python 3.13 --extra dev ruff check .
    Invoke-CheckCommand uv run --python 3.13 --extra dev pytest
    exit
}

if (Test-StablePython "py" @("-3.13")) {
    Invoke-PythonModule "py" @("-3.13") "ruff" @("check", ".")
    Invoke-PythonModule "py" @("-3.13") "pytest"
    exit
}

if (Test-StablePython "py" @("-3.12")) {
    Invoke-PythonModule "py" @("-3.12") "ruff" @("check", ".")
    Invoke-PythonModule "py" @("-3.12") "pytest"
    exit
}

if (Test-StablePython "python") {
    Invoke-PythonModule "python" @() "ruff" @("check", ".")
    Invoke-PythonModule "python" @() "pytest"
    exit
}

throw "Python 3.12/3.13 was not found. Install Python 3.12 or 3.13, or install uv."
