@echo off

rem build tier
python build_products.py --dev pro


rem blender sys link
rmdir ^
"C:\Users\Scot Thomson\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\qc_checker"

mklink /D ^
"C:\Users\Scot Thomson\AppData\Roaming\Blender Foundation\Blender\5.1\scripts\addons\qc_checker" ^
"C:\Users\Scot Thomson\Documents\scriptronaut\qc_checker\dev\qc_checker_pro"

pause