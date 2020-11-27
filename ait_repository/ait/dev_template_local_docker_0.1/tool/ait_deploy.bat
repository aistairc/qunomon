@echo off

set DOCKER_IMAGE_NAME=ait_deploy_dev_template_local_docker
set REGISTORY=localhost:5500

cd /d %~dp0

rem Šù‘¶íœ
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f
docker rmi %REGISTORY%/%DOCKER_IMAGE_NAME%

rem ƒrƒ‹ƒh
echo start docker build...
docker build -t %DOCKER_IMAGE_NAME% -f .\ait_deploy\dockerfile .\ait_deploy

rem Às
echo run docker...
docker run %DOCKER_IMAGE_NAME%:latest

pause