@echo off
REM LaTeX Resume — One-click setup and launch
REM Run this on a new machine after installing MiKTeX and Python

echo ============================================
echo   LaTeX Resume — Live Preview Setup
echo ============================================
echo.

REM Check prerequisites
where pdflatex >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pdflatex not found. Install MiKTeX: https://miktex.org/download
    pause
    exit /b 1
)

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Install from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo [1/3] Compiling main.tex...
pdflatex -interaction=nonstopmode main.tex
if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed. Check main.log for details.
    pause
    exit /b 1
)
echo      OK — main.pdf created
echo.

echo [2/3] Starting HTTP server on port 8888...
echo      Browser: http://localhost:8888/preview.html
echo.
start "" python -m http.server 8888

echo [3/3] Opening preview in browser...
timeout /t 2 /nobreak >nul
start http://localhost:8888/preview.html

echo.
echo ============================================
echo   Server running at http://localhost:8888
echo   Edit main.tex → Save → Click Refresh PDF
echo   Press Ctrl+C to stop the server
echo ============================================
echo.
pause
