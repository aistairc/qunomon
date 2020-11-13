@echo off

rem to set yourself environment path
set CHROME="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

cd /d %~dp0

set DST=%~dp0\..\
set CRT=%~dp0\

docker run ^
    -d ^
    -p 3000:3000 ^
    -v %DST%\dev:/home/project/dev ^
    -v %DST%\exp:/home/project/exp ^
    -v %CRT%\TheiaTools:/home/project/TheiaTools ^
    -v %DST%\local_qai:/usr/local/qai ^
    -e TZ=Asia/Tokyo ^
    theiaide/theia-python:1.4.0

echo;
echo wait start complete docker container...
timeout 3 /nobreak

echo open theia
echo;
%CHROME% --app=http://localhost:3000 --disable-background-mode --disable-extensions
