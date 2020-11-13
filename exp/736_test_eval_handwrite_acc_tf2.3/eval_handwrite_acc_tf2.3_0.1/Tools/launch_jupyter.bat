@echo off

rem to set yourself environment path
set CHROME="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

cd /d %~dp0

set DST=%~dp0\..\
set CRT=%~dp0\

docker run ^
    -d ^
    -p 8888:8888 ^
    -v %DST%\exp:/tf/mnt ^
    -e TZ=Asia/Tokyo ^
    -e NB_UID=1000 ^
    -e NB_GID=100 ^
    -e GRANT_SUDO="yes" ^
    -e PASSWORD="password" ^
    -e JUPYTER_TOKEN="token" ^
    tensorflow/tensorflow:2.3.0-jupyter

echo;
echo wait start complete docker container...
timeout 3 /nobreak

echo open theia
echo;
%CHROME% --app=http://localhost:8888?token=token  --disable-background-mode --disable-extensions
