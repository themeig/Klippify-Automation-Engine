@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   INSTALLAZIONE DIPENDENZE KLIPPIFY AUTOMATION ENGINE
echo ============================================================
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python core\setup_antigravity_cron.py
echo.
echo [OK] Dipendenze e Cronjob Antigravity configurati con successo!
pause
