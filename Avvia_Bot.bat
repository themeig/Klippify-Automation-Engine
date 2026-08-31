@echo off
cd /d "%~dp0"
echo Chiusura di eventuali sessioni bloccate di Chrome in background...
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'chrome.exe'\" | Where-Object { $_.CommandLine -match 'gemini_profile' } | Stop-Process -Force" 2>nul
echo Sto avviando il bot...
python gemini_bot.py %*
echo.
echo ========================================================
echo Lo script e' terminato o ha riscontrato un errore.
echo Leggi l'eventuale errore qui sopra.
echo ========================================================
pause
