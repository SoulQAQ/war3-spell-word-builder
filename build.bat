@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul

cd /d "%~dp0"
title PyQt EXE Template - Builder

set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
set "MAIN_SCRIPT=script\main.py"
set "APP_NAME=pyqt-exe-template"
set "SETUP_SCRIPT=setup.bat"
set "SPEC_FILE=%APP_NAME%.spec"

echo ========================================
echo   PyQt EXE Template - Build
echo ========================================
echo.

:: Check required files
if not exist "%SETUP_SCRIPT%" (
    echo [ERROR] Setup script not found: %SETUP_SCRIPT%
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

:: Run setup
echo [INFO] Checking environment...
call "%SETUP_SCRIPT%"
if errorlevel 1 (
    echo [ERROR] Setup failed, cannot continue build.
    echo.
    pause
    exit /b 1
)

:: Ensure PyInstaller is installed
echo [INFO] Checking PyInstaller...
"%VENV_PY%" -c "import PyInstaller" >nul 2>nul
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    "%VENV_PY%" -m pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller.
        echo.
        pause
        exit /b 1
    )
)

:: Clean old build files
echo [INFO] Cleaning old build files...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

:: Check icon file
set "ICON_PARAM="
if exist "app.ico" (
    echo [INFO] Using application icon: app.ico
    set "ICON_PARAM=--icon app.ico"
) else (
    echo [WARNING] app.ico not found, using default icon
)

:: Run build
echo [INFO] Starting build...
echo.

if exist "%SPEC_FILE%" (
    echo [INFO] Using existing spec file: %SPEC_FILE%
    "%VENV_PY%" -m PyInstaller "%SPEC_FILE%" --noconfirm --clean
) else (
    echo [INFO] Building with command line parameters...
    "%VENV_PY%" -m PyInstaller ^
      --noconfirm ^
      --clean ^
      --onefile ^
      --windowed ^
      --name "%APP_NAME%" ^
      --add-data "resources;resources" ^
      --add-data "config;config" ^
      %ICON_PARAM% ^
      --hidden-import "PyQt6" ^
      --hidden-import "PyQt6.QtCore" ^
      --hidden-import "PyQt6.QtGui" ^
      --hidden-import "PyQt6.QtWidgets" ^
      --hidden-import "yaml" ^
      --hidden-import "requests" ^
      "%MAIN_SCRIPT%"
)

if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller build failed.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Build complete!
echo ========================================
echo.
echo Output file location:
echo     dist\%APP_NAME%.exe
echo.

:: Check output file
if exist "dist\%APP_NAME%.exe" (
    echo [INFO] File size:
    for %%A in ("dist\%APP_NAME%.exe") do echo     %%~zA bytes
)

echo.
pause

endlocal
exit /b 0
