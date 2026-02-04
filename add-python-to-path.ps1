# Add Python to PATH - Run this in PowerShell as Administrator

# Find Python installation
$pythonPaths = @(
    "$env:LOCALAPPDATA\Programs\Python\Python313",
    "$env:LOCALAPPDATA\Programs\Python\Python312",
    "$env:LOCALAPPDATA\Programs\Python\Python311",
    "C:\Python313",
    "C:\Python312",
    "C:\Python311"
)

$pythonPath = $null
foreach ($path in $pythonPaths) {
    if (Test-Path "$path\python.exe") {
        $pythonPath = $path
        Write-Host "Found Python at: $pythonPath" -ForegroundColor Green
        break
    }
}

if ($pythonPath) {
    # Add to PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$pythonPath*") {
        $newPath = "$currentPath;$pythonPath;$pythonPath\Scripts"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "✅ Python added to PATH successfully!" -ForegroundColor Green
        Write-Host "⚠️  Please restart VS Code for changes to take effect" -ForegroundColor Yellow
    } else {
        Write-Host "Python is already in PATH" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Python installation not found. Please reinstall Python." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Cyan
}
