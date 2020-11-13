@echo off

cd /d %~dp0\..\

rem if use this command, need pip install wheel

sphinx-apidoc -f -o .\docs .\src\ait_sdk
sphinx-build -b html .\docs .\docs\_build

pause
