@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul

cd /d "%~dp0"
title PyQt EXE Template - Environment Setup

set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "VENV_CFG=%VENV_DIR%\pyvenv.cfg"
set "REQUIREMENTS=requirements.txt"
set "SNAPSHOT_FILE=%VENV_DIR%\.requirements.snapshot"
set "PYTHON_VERSION=3.12"

echo ========================================
echo   PyQt EXE Template - Environment Setup
echo ========================================
echo.

:: Check py launcher
where py >nul 2>nul
if errorlevel 1 (
    echo [ERROR] py launcher not found.
    echo Please install Python %PYTHON_VERSION% and ensure Python Launcher is selected.
    echo.
    pause
    exit /b 1
)

:: Check Python version
py -%PYTHON_VERSION% -c "import sys" >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python %PYTHON_VERSION% not detected.
    echo Please install Python %PYTHON_VERSION%.
    echo.
    pause
    exit /b 1
)

:: Create virtual environment
if not exist "%VENV_PY%" (
    echo [INFO] Virtual environment not found, creating...
    py -%PYTHON_VERSION% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        echo.
        pause
        exit /b 1
    )
)

:: Verify virtual environment version
set "VENV_VER="
if exist "%VENV_CFG%" (
    for /f "tokens=1,* delims==" %%A in (%VENV_CFG%) do (
        set "KEY=%%A"
        set "VAL=%%B"
        set "KEY=!KEY: =!"
        if /i "!KEY!"=="version" (
            set "VENV_VER=!VAL!"
            set "VENV_VER=!VENV_VER: =!"
        )
    )
)

echo [INFO] Current virtual environment version: %VENV_VER%
echo %VENV_VER% | findstr /b "%PYTHON_VERSION%." >nul
if errorlevel 1 (
    echo [WARNING] Current virtual environment is not Python %PYTHON_VERSION%, rebuilding...
    rmdir /s /q "%VENV_DIR%"
    py -%PYTHON_VERSION% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to rebuild virtual environment.
        echo.
        pause
        exit /b 1
    )
)

:: Upgrade base tools
echo [INFO] Upgrading pip / setuptools / wheel ...
"%VENV_PY%" -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [ERROR] Failed to upgrade base tools.
    echo.
    pause
    exit /b 1
)

:: Install dependencies
if exist "%REQUIREMENTS%" (
    echo [INFO] Installing dependencies from requirements.txt...
    "%VENV_PY%" -m pip install -r "%REQUIREMENTS%"
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies from requirements.txt.
        echo.
        pause
        exit /b 1
    )
    copy /y "%REQUIREMENTS%" "%SNAPSHOT_FILE%" >nul
) else (
    echo [WARNING] requirements.txt not found
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Environment setup complete.
echo.
endlocal
exit /b 0
