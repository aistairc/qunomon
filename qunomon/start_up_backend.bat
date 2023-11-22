@echo off

cd /d %~dp0

cd .\src\backend
call .\venv\Scripts\activate.bat
python -m entrypoint startserver

