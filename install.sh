# PowerShell script to install dependencies for the AI-Powered Shell on Windows.
#
# How to run:
# 1. Right-click the Start button and select "Windows PowerShell (Admin)" or "Terminal (Admin)".
# 2. Navigate to the directory where you saved this script.
#    (e.g., cd C:\Users\YourUser\Downloads)
# 3. Run this command: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# 4. Run this script: .\install.ps1

Write-Host "--- AI-Powered Shell Installer for Windows ---" -ForegroundColor Green

# --- Check for Python ---
Write-Host "[1/2] Checking for Python installation..."
try {
    $pythonVersion = python --version
    Write-Host "Python is installed: $pythonVersion" -ForegroundColor Cyan
}
catch {
    Write-Host "Python not found." -ForegroundColor Yellow
    Write-Host "Please install Python 3 from the Microsoft Store or python.org and run this script again."
    Write-Host "Ensure you check the box 'Add Python to PATH' during installation."
    exit 1
}

# --- Install Python Dependencies ---
Write-Host "[2/2] Installing required Python packages..." -ForegroundColor Green
try {
    pip install requests google-generativeai
    Write-Host "Successfully installed Python packages." -ForegroundColor Cyan
}
catch {
    Write-Host "An error occurred while installing Python packages." -ForegroundColor Red
    Write-Host "Please ensure pip is working correctly."
    exit 1
}

Write-Host ""
Write-Host "--- Installation Complete ---" -ForegroundColor Green
Write-Host "You can now run the main script by typing: python ai_shell-alpha0.0.20.py"
Write-Host ""
Write-Host "IMPORTANT WARNING:" -ForegroundColor Yellow
Write-Host "The 'Metasploit Assistant' mode will NOT work when running directly on Windows." -ForegroundColor Yellow
Write-Host "This is because a required module ('pty') is only available on Linux." -ForegroundColor Yellow
Write-Host "To use the Metasploit mode, please use the Windows Subsystem for Linux (WSL)." -ForegroundColor Yellow
