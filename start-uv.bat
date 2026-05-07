@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"
title war3-skill-text-generator - UV Launcher

set "PROJECT_NAME=war3-skill-text-generator"
set "MAIN_SCRIPT=script\main.py"
set "REQUIREMENTS=requirements.txt"
set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

echo ========================================
echo   %PROJECT_NAME% (UV)
echo ========================================
echo.

where uv >nul 2>nul
if errorlevel 1 (
    echo [ERROR] uv not found. Please install uv first.
    echo [HINT]  pip install uv
    echo.
    pause
    exit /b 1
)

if not exist "%MAIN_SCRIPT%" (
    echo [ERROR] Main script not found: %MAIN_SCRIPT%
    echo.
    pause
    exit /b 1
)

if not exist "%VENV_PY%" (
    echo [INFO] Creating virtual environment with uv...
    uv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        echo.
        pause
        exit /b 1
    )
)

echo [INFO] Installing dependencies with uv...
if exist "%REQUIREMENTS%" (
    uv pip install -r "%REQUIREMENTS%"
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        echo.
        pause
        exit /b 1
    )
) else (
    echo [ERROR] requirements.txt not found.
    echo.
    pause
    exit /b 1
)

echo.
echo [INFO] Starting application...
"%VENV_PY%" "%MAIN_SCRIPT%"
set "APP_EXIT=%ERRORLEVEL%"

echo.
if not "%APP_EXIT%"=="0" (
    echo [ERROR] Application exited with code: %APP_EXIT%
    echo.
    pause
    exit /b %APP_EXIT%
)

endlocal
exit /b 0
