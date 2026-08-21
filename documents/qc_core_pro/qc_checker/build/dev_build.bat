@echo off
cls


rem Tier name
echo Build Tier?:
echo 1. Core
echo 2. Pro
choice /c 12 /m "Select 1 or 2"

rem Blender Version
set /p blender_version="Your Blender Version? 

rem Condition
if errorlevel 2 set "tier=pro"
if errorlevel 1 set "tier=core"

rem Build
echo "python build_products.py --dev %tier%"
echo "C:\Users\%USERNAME%\AppData\Roaming\Blender Foundation\Blender\%blender_version%\scripts\addons\qc_checker"


pause