@echo off
cd /d "%~dp0"
title Klippify Control Server
echo ========================================================
echo AVVIO SERVER LOCALE KLIPPIFY
echo ========================================================
echo Il server sta aprendo l'interfaccia su http://localhost:5000...
echo.
python -u server.py
echo.
pause
