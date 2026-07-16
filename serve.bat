@echo off
chcp 65001 >nul
title 点餐助手 · 服务器

cd /d "%~dp0"

echo.
echo   正在启动服务器...
echo.

python serve.py

pause
