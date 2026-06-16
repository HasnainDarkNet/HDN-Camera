@echo off
title Auto Startup Installer
color 0A

echo ========================================
echo Python Script Auto Startup Installer
echo ========================================
echo.

:: Get the folder where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%webcam.py"

:: Check if Python file exists
if not exist "%PYTHON_SCRIPT%" (
    echo ERROR: test.py not found in current directory!
    echo Please make sure webcam.py is in the same folder as this batch file.
    echo.
    pause
    exit /b 1
)

echo Python file found: %PYTHON_SCRIPT%
echo.

:: Method 1: Add to Startup Folder (Current User)
echo Adding to Startup Folder...
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "BAT_FILE=%STARTUP_FOLDER%\run_python_script.bat"

:: Create a launcher batch file in startup folder
(
echo @echo off
echo cd /d "%SCRIPT_DIR%"
echo start /B pythonw "%PYTHON_SCRIPT%"
echo exit
) > "%BAT_FILE%"

echo [SUCCESS] Added to Startup Folder
echo.

:: Method 2: Add to Registry (Backup method)
echo Adding to Registry...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "PythonAutoStart" /t REG_SZ /d "pythonw \"%PYTHON_SCRIPT%\"" /f >nul 2>&1
echo [SUCCESS] Added to Registry
echo.

echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Your Python script will now run automatically:
echo - Every time you start your PC
echo - Every time you login to Windows
echo.
echo To REMOVE from startup, run the uninstaller below.
echo.

pause
