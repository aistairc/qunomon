@echo off

rem to set yourself environment path
set CHROME="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

set YML="%~dp0\docker\docker-compose.yml"

echo start docker container
echo;

docker-compose -f %YML% up -d 

echo;
echo wait start complete docker container...
timeout 3 /nobreak

echo open jupyter
echo;
%CHROME% --app=http://localhost:9988?token=token --disable-background-mode --disable-extensions

choice /m "you want docker down <Y> , not down is <N>"
if errorlevel 2 goto :no
if errorlevel 1 goto :yes
 
:yes
docker-compose -f %YML% down

:no
pause