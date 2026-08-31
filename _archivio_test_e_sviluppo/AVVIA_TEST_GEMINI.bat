@echo off
title PIPELINE CLIPPING VIDEO - KLIPPIFY
chcp 65001 >nul
cd /d "c:\Users\HP\Desktop\contenuti klippify"

echo =======================================================================
echo          AVVIO PIPELINE CLIPPING AUTOMATICA CON GEMINI
echo =======================================================================
echo.
echo Video target: CRISTINA ZAHARIA, + DI 3000 EURO NEI PRIMI MESI DI ATTIVITÁ.mp4
echo Cartella: clipping_sources\6a71c6f7245627c68999eae2
echo.
echo 1. Avvio Bot Gemini (Upload e analisi timestamp virali)...
echo 2. Taglio FFmpeg 9:16 verticale per TikTok...
echo 3. Assegnazione automatica agli slot di pubblicazione...
echo.

python -u clipping_pipeline.py 6a71c6f7245627c68999eae2 --video "CRISTINA ZAHARIA, + DI 3000 EURO NEI PRIMI MESI DI ATTIVITÁ.mp4"

echo.
echo =======================================================================
echo   PIPELINE COMPLETATA! Le clip 9:16 sono pronte negli slot TikTok.
echo =======================================================================
pause
