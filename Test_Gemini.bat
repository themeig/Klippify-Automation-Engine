@echo off
cd /d "%~dp0"
echo Chiusura sessioni Chrome bloccate...
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'chrome.exe'\" | Where-Object { $_.CommandLine -match 'gemini_profile' } | Stop-Process -Force" 2>nul
echo ========================================
echo AVVIO TEST MANUALE GEMINI BOT
echo ========================================
python gemini_bot.py
echo.
pause
