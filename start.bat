@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul

cd /d "%~dp0"
title PyQt EXE Template - Launcher

set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "MAIN_SCRIPT=script\main.py"
set "REQUIREMENTS=requirements.txt"
set "SNAPSHOT_FILE=%VENV_DIR%\.requirements.snapshot"
set "SETUP_SCRIPT=setup.bat"

echo ========================================
echo   PyQt EXE Template
echo ========================================
echo.

:: Check main script
if not exist "%MAIN_SCRIPT%" (
    echo [ERROR] Main script not found: %MAIN_SCRIPT%
    echo.
    pause
    exit /b 1
)

:: Check if setup is needed
set "NEED_SETUP="
if not exist "%VENV_PY%" set "NEED_SETUP=1"
if not exist "%SNAPSHOT_FILE%" set "NEED_SETUP=1"
if exist "%REQUIREMENTS%" (
    fc /b "%REQUIREMENTS%" "%SNAPSHOT_FILE%" >nul 2>nul
    if errorlevel 1 set "NEED_SETUP=1"
)

if defined NEED_SETUP (
    echo [INFO] Environment not ready or dependencies changed, calling setup...
    call "%SETUP_SCRIPT%"
    if errorlevel 1 (
        echo [ERROR] Setup failed, cannot start application.
        echo.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Environment is up to date, skipping setup.
)

:: Start application
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
