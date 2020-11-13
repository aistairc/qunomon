@echo off

cd /d %~dp0

cd .\src\integration-provider
call .\venv\Scripts\activate.bat
python -m entrypoint startserver

