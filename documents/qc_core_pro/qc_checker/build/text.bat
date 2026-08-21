@echo off


rem Prompt user
echo Build Tier?:
echo 1. Core
echo 2. Pro
choice /c 12 /m "Select 1 or 2 


rem Goto condition
if errorlevel 2 goto BuildPro
if errorlevel 1 goto BuildCore


rem Builds
:BuildCore
set tier_name=core
echo Tier is %tier_name%
pause
exit

:BuildPro
set tier_name=pro
echo Tier is %tier_name%
pause
exit

