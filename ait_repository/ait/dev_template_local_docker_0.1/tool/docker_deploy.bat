@echo off

set DOCKER_IMAGE_NAME=dev_template_local_docker:0.1
set REGISTORY=localhost:5500

cd /d %~dp0

rem 既存削除
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f
docker rmi %REGISTORY%/%DOCKER_IMAGE_NAME%

rem ビルド
echo start docker build...
docker build -f ..\deploy\container\dockerfile -t %DOCKER_IMAGE_NAME% ..\deploy\container

rem タグ付け
echo start docker tag...
docker tag %DOCKER_IMAGE_NAME% %REGISTORY%/%DOCKER_IMAGE_NAME%

rem プッシュ
echo start docker push...
docker push %REGISTORY%/%DOCKER_IMAGE_NAME%

pause