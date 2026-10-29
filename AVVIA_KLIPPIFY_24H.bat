@echo off
chcp 65001 >nul
cd /d "%~dp0"
title KLIPPIFY BOT 24/7 - SERVER & AUTOPILOT

echo ============================================================
echo   KLIPPIFY AUTOPILOT & SERVER (MODALITA 24/7)
echo ============================================================
echo.
echo  Il server locale e' attivo e in ascolto.
echo  Dashboard: http://localhost:5000
echo.
echo  Per terminare premi CTRL + C oppure chiudi questa finestra.
echo ============================================================
echo.

echo [%date% %time%] Configurazione automatica Cronjob Antigravity per questo PC...
python core/setup_antigravity_cron.py

start "" "http://localhost:5000"

:loop
echo [%date% %time%] Avvio server in corso...
python -u core/server.py
echo.
echo [ATTENZIONE] Il server si e' interrotto. Riavvio automatico tra 5 secondi...
timeout /t 5 >nul
goto loop
