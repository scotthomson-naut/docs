@echo off
cls


rem ------------------------------------------------------------
rem Variables
rem ------------------------------------------------------------

set "bat_path=%~dp0"
set "tool_path_file=%bat_path%local_tool_path.txt"


rem ------------------------------------------------------------
rem Check if local tool path file exists
rem ------------------------------------------------------------

if not exist "%tool_path_file%" (
    echo Error: local_tool_path.txt was not found.
    echo Expected:
    echo %tool_path_file%
    goto :end
)


rem ------------------------------------------------------------
rem Get user local tool path
rem ------------------------------------------------------------

set /p local_tool_path=<"%tool_path_file%"

if "%local_tool_path%"=="" (
    echo Error: local_tool_path.txt is empty.
    goto :end
)


rem ------------------------------------------------------------
rem Tier
rem ------------------------------------------------------------


echo Build Tier:
echo 1. Core
echo 2. Pro

choice /c 12 /m "Select 1 or 2"

if errorlevel 2 (
    set "tier=pro"
) else (
    set "tier=core"
)


rem ------------------------------------------------------------
rem Blender Version
rem ------------------------------------------------------------

set /p blender_version="Your Blender Version? "

if "%blender_version%"=="" (
    echo Error: Blender version was not entered.
    goto :end
)


rem ------------------------------------------------------------
rem Blender Addon Path
rem ------------------------------------------------------------

set "blender_addon_path=C:\Users\%USERNAME%\AppData\Roaming\Blender Foundation\Blender\%blender_version%\scripts\addons\qc_checker"


rem ------------------------------------------------------------
rem Display Build Information
rem ------------------------------------------------------------

echo ------------------------------------------------------------
echo Scriptronaut QC Checker Development Build
echo ------------------------------------------------------------
echo.
echo Local Tool Path:
echo %local_tool_path%
echo.
echo Tier:
echo %tier%
echo.
echo Blender Version:
echo %blender_version%
echo.
echo Blender Addon Path:
echo %blender_addon_path%
echo.
echo Build Command:
echo python "%bat_path%build_products.py" --dev %tier%
echo.
echo ------------------------------------------------------------


rem ------------------------------------------------------------
rem Build
rem ------------------------------------------------------------

python "%bat_path%build_products.py" --dev %tier%


rem ------------------------------------------------------------
rem Check Build Result
rem ------------------------------------------------------------

if errorlevel 1 (
    echo Error: Build failed.
    goto :end
)

echo Build completed successfully.


:end
pause