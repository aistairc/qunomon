@echo off

set DOCKER_IMAGE_NAME=dev_hello_world:0.1
set REGISTORY=qunomon

cd /d %~dp0

rem login
docker login --username qunomon

rem 既存削除
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f
docker rmi %REGISTORY%/%DOCKER_IMAGE_NAME%

rem ビルド
echo start docker build...
docker build -f .\docker\dockerfile -t %DOCKER_IMAGE_NAME% .\docker

rem タグ付け
echo start docker tag...
docker tag %DOCKER_IMAGE_NAME% %REGISTORY%/%DOCKER_IMAGE_NAME%

rem プッシュ
echo start docker push...
docker push %REGISTORY%/%DOCKER_IMAGE_NAME%

rem logout
docker logout

pause