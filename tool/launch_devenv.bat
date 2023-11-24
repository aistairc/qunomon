@echo off

set YML="%~dp0\docker\docker-compose.yml"

echo Launching docker containers.
echo;

copy ..\deploy\container\resolve-dependencies.sh docker\jupyter\

docker-compose -f %YML% up -d

echo;
echo Please wait until all docker containers are running...
timeout 3 /nobreak

echo Opening Jupyter environment.
echo;
start chrome --app=http://localhost:9888?token=token --disable-background-mode --disable-extensions

choice /m "Do you want to stop AIT development environment (containers)? <Y/N>"
if errorlevel 2 goto :no
if errorlevel 1 goto :yes

:yes
docker-compose -f %YML% down

:no
pause