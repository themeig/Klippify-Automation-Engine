@echo off
title TEST GENERAZIONE VIDEO GEMINI
cd /d "%~dp0"
echo ========================================================
echo   TEST CON IL PROMPT ESATTO (VISIBILE)
echo ========================================================
echo.
echo [1/2] Pulizia sessioni Chrome...
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name = 'chrome.exe'\" | Where-Object { $_.CommandLine -match 'gemini_profile' } | Stop-Process -Force" 2>nul

echo [2/2] Avvio del Bot con il prompt esatto...
echo.
python -u test_exact_prompt.py
echo.
echo ========================================================
echo   TEST TERMINATO
echo ========================================================
pause
