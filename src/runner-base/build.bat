@echo off

set DOCKER_IMAGE_NAME=runner-base:3.6

cd /d %~dp0

echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f

echo start docker build...
docker build --no-cache -t %DOCKER_IMAGE_NAME% .

pause