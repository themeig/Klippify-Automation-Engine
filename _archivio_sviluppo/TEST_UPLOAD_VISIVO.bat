@echo off
title TEST UPLOAD TIKTOK IN DIRETTA
cd /d "c:\Users\HP\Desktop\contenuti klippify"
echo ============================================================
echo   TEST UPLOAD TIKTOK STUDIO (SCHERMO INTERATTIVO)
echo ============================================================
echo.
echo  Sto avviando Google Chrome... Vedrai la finestra aprirsi
echo  sul tuo desktop ed eseguire tutti i passaggi live!
echo.
echo ============================================================
echo.
python -u tiktok_uploader.py --payload upload_payload.json
echo.
echo ============================================================
echo   ESECUZIONE TERMINATA
echo ============================================================
pause
