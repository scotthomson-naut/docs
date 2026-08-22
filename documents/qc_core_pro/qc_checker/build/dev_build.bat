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
rem Validate Blender Version
rem Expected format: X.X
rem ------------------------------------------------------------

set "version_major="
set "version_minor="
set "version_extra="

for /f "tokens=1,2,3 delims=." %%A in ("%blender_version%") do (
    set "version_major=%%A"
    set "version_minor=%%B"
    set "version_extra=%%C"
)

rem Major and minor must exist
if not defined version_major goto :invalid_blender_version
if not defined version_minor goto :invalid_blender_version

rem There must not be a third component
if defined version_extra goto :invalid_blender_version

rem Major must contain numbers only
for /f "delims=0123456789" %%A in ("%version_major%") do (
    goto :invalid_blender_version
)

rem Minor must contain numbers only
for /f "delims=0123456789" %%A in ("%version_minor%") do (
    goto :invalid_blender_version
)

goto :blender_version_valid


:invalid_blender_version
echo Error: Invalid Blender version "%blender_version%".
echo Please enter a version such as 4.3 or 5.1.
goto :end


:blender_version_valid

rem ------------------------------------------------------------
rem Blender Paths
rem ------------------------------------------------------------

set "blender_path=%APPDATA%\Blender Foundation\Blender\%blender_version%"
set "blender_addon_path=%blender_path%\scripts\addons\qc_checker"


rem ------------------------------------------------------------
rem Check Blender Version Folder Exists
rem ------------------------------------------------------------

if not exist "%blender_path%\" (
    echo.
    echo Error: Blender %blender_version% was not found.
    echo.
    echo Expected:
    echo %blender_path%
    goto :end
)


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
echo Blender Path:
echo %blender_path%
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
    echo.
    echo Error: Build failed.
    goto :end
)

echo Build completed successfully.


:end
echo.
pause