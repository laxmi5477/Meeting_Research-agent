@echo off
title Meeting Research Agent
cd /d "%~dp0"
echo ========================================================
echo   Starting Meeting Research Agent...
echo   Open in browser: http://localhost:8501
echo ========================================================
echo.
python -m streamlit run app.py --server.port 8501 --server.address localhost
pause
