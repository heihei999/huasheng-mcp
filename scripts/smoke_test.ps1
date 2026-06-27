$ErrorActionPreference = "Stop"

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
chcp.com 65001 | Out-Null

$ProjectRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")
Set-Location -LiteralPath $ProjectRoot

function Add-LocalPythonToPath {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand -and $pythonCommand.Source -notlike "*\WindowsApps\python.exe") {
        return
    }

    $pythonRoots = @(
        (Join-Path $env:LocalAppData "Programs\Python\Python312"),
        (Join-Path $env:LocalAppData "Programs\Python\Python311"),
        (Join-Path $env:LocalAppData "Programs\Python\Python310")
    )

    foreach ($root in $pythonRoots) {
        $pythonExe = Join-Path $root "python.exe"
        if (Test-Path -LiteralPath $pythonExe) {
            $scriptsDir = Join-Path $root "Scripts"
            $env:Path = "$root;$scriptsDir;$env:Path"
            return
        }
    }
}

function Invoke-Step {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Name,

        [Parameter(Mandatory = $true)]
        [scriptblock] $Command
    )

    Write-Host ""
    Write-Host "==> $Name"
    & $Command
}

function From-Utf8Base64 {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Value
    )

    return [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($Value))
}

Add-LocalPythonToPath

$python = Get-Command python -ErrorAction Stop
if ($python.Source -like "*\WindowsApps\python.exe") {
    throw "python still points to WindowsApps placeholder. Install Python or add a real Python directory to PATH."
}

$solver = Get-Command xingce-solver -ErrorAction Stop
$SolverPath = $solver.Source
$QueryShareGrowth = From-Utf8Base64 "5q+U6YeNIOWinumVv+eOhw=="
$QuerySharePoint = From-Utf8Base64 "5Y2g5q+U5Y+Y5YyWIOeZvuWIhueCuQ=="
$QuestionText = From-Utf8Base64 "MjAxOeW5tOafkOWcsOWMuueUn+S6p+aAu+WAvOWQjOavlOWinumVvzguNSXvvIzlhbbkuK3nrKzkuIDkuqfkuJrljaDmr5Tmj5Dpq5gwLjPkuKrnmb7liIbngrnjgILpl67ljaDmr5Tlj5jljJbmg4XlhrXvvJ8="
$ExpectedModule = From-Utf8Base64 "6LWE5paZ5YiG5p6Q"
$ExpectedQuestionType = From-Utf8Base64 "5q+U6YeN5Y+Y5YyW"
$SolveDataText = From-Utf8Base64 "MjAyMOW5tOafkOS6p+S4muaUtuWFpeS4ujEzMuS6v+WFg++8jOWQjOavlOWinumVvzEwJe+8jOmXrjIwMTnlubTmlLblhaXnuqbkuLrlpJrlsJHvvJ8gQS4xMDDkur/lhYMgQi4xMTDkur/lhYMgQy4xMjDkur/lhYMgRC4xMzLkur/lhYM="
$SolveLogicText = From-Utf8Base64 "5p+Q56CU56m26K6k5Li677yM57uP5bi45Zad6Iy255qE5Lq65pu05YGl5bq344CC5Zug5q2k77yM5Zad6Iy25Y+v5Lul5o+Q6auY5YGl5bq35rC05bmz44CC5Lul5LiL5ZOq6aG55pyA6IO95YmK5byx5LiK6L+w6K666K+B77yfQS7lgaXlurfnmoTkurrmm7Tlj6/og73mnInllp3ojLbkuaDmg68gQi7llp3ojLbnmoTkurrpgJrluLjkuZ/mm7TniLHov5DliqggQy7pg6jliIbkurrllp3ojLblkI7nnaHnnKDlj5jlt64gRC7ojLblj7bku7fmoLzpgJDlubTkuIrmtqg="

Invoke-Step "pytest" {
    python -m pytest
}

Invoke-Step "card da_share_change_004" {
    & $SolverPath card --id da_share_change_004
}

Invoke-Step "search share growth" {
    & $SolverPath search --query $QueryShareGrowth
}

Invoke-Step "search share change point" {
    & $SolverPath search --query $QuerySharePoint
}

Invoke-Step "source da_share_change_004" {
    & $SolverPath source --method-id da_share_change_004
}

$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) "xingce-solver-smoke"
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null
$QuestionPath = Join-Path $TempDir "question.txt"
Set-Content -LiteralPath $QuestionPath -Encoding UTF8 -Value $QuestionText

Invoke-Step "classify question.txt" {
    $classifyOutput = & $SolverPath classify --question $QuestionPath
    Write-Host ($classifyOutput -join [Environment]::NewLine)

    $results = $classifyOutput | ConvertFrom-Json
    if (-not $results -or $results.Count -lt 1) {
        throw "classify returned no results."
    }

    $first = @($results)[0]
    if ($first.module -ne $ExpectedModule) {
        throw "classify first result module mismatch: expected $ExpectedModule, got $($first.module)"
    }
    if ($first.question_type -ne $ExpectedQuestionType) {
        throw "classify first result question_type mismatch: expected $ExpectedQuestionType, got $($first.question_type)"
    }
    if ($first.priority_method_id -ne "da_share_change_004") {
        throw "classify first result priority_method_id mismatch: expected da_share_change_004, got $($first.priority_method_id)"
    }

    Write-Host "classify first result assertion passed."
}

Invoke-Step "solve-data base amount" {
    & $SolverPath solve-data --text $SolveDataText
}

Invoke-Step "solve-logic weaken draft" {
    $logicOutput = & $SolverPath solve-logic --text $SolveLogicText
    Write-Host ($logicOutput -join [Environment]::NewLine)

    $requiredHeadings = @(
        (From-Utf8Base64 "6aKY5Z6L5Yik5pat"),
        (From-Utf8Base64 "6LCD55So5pa55rOV"),
        (From-Utf8Base64 "6K6654K5"),
        (From-Utf8Base64 "6YCJ6aG55YiG5p6Q")
    )
    foreach ($heading in $requiredHeadings) {
        if (-not (($logicOutput -join [Environment]::NewLine).Contains($heading))) {
            throw "solve-logic output missing required heading: $heading"
        }
    }
}

Write-Host ""
Write-Host "Smoke test passed."
