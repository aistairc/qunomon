@echo off

rem steup.pyのフォルダに移動 
cd /d %~dp0\..\

rem if use thiscommand, need pip install wheel
python setup.py  bdist_wheel

pause
