@echo off

rem #####AIT Docker�C���[�W�쐬#####

set DOCKER_IMAGE_NAME=ait_license_base:latest

cd /d %~dp0

rem �����폜
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f

rem �r���h
echo start docker build...
docker build -f ..\deploy\container\dockerfile -t %DOCKER_IMAGE_NAME% ..\deploy\container
if %errorlevel% neq 0 (
	echo;
	echo ERROR:docker build error. Please check ..\deploy\container\dockerfile.
	pause
	exit /b
)

rem #####AIT���C�Z���X���o��#####

set LICENSE_DOCKER_IMAGE_NAME=ait_license_thirdparty_notices

cd /d %~dp0

rem �����폜
echo start docker crean up...
docker rmi %LICENSE_DOCKER_IMAGE_NAME%
docker system prune -f

rem �r���h
echo start docker build...
docker build -t %LICENSE_DOCKER_IMAGE_NAME% -f ..\deploy\container\dockerfile_license ..\deploy\container
if %errorlevel% neq 0 (
	echo;
	echo ERROR:docker build error. Please check ..\deploy\container\dockerfile_license
	pause
	exit /b
)

rem ���s
echo run docker...
docker run %LICENSE_DOCKER_IMAGE_NAME%:latest > ../ThirdPartyNotices.txt

pause