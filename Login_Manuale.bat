@echo off
cd /d "%~dp0"
echo Sto chiudendo eventuali processi bloccati in background...
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'chrome.exe'\" | Where-Object { $_.CommandLine -match 'gemini_profile' } | Stop-Process -Force" 2>nul
echo.
echo Sto aprendo Chrome per il login manuale...
"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="%cd%\gemini_profile" "https://gemini.google.com/"
