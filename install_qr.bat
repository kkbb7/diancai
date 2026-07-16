@echo off
cd /d "%~dp0"
echo.
echo   Installing dependencies (Tsinghua mirror)...
echo.
python -m pip install qrcode Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
echo.
echo   Done. Run serve.bat to start.
echo.
pause
