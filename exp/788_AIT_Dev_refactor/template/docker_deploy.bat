@echo off

set DOCKER_IMAGE_NAME={AIT_NAME}:{AIT_VERSION}
set REGISTORY=docker.pkg.github.com/m-akita-aist/qai-testbed

cd /d %~dp0

rem login
docker login docker.pkg.github.com --username m-akita-aist --password 6071ebd424ad5c193f27e03a545cdfd5538ee561

rem 既存削除
echo start docker crean up...
docker rmi %DOCKER_IMAGE_NAME%
docker system prune -f
docker rmi %REGISTORY%/%DOCKER_IMAGE_NAME%

rem ビルド
echo start docker build...
docker build -t %DOCKER_IMAGE_NAME% ..\deploy\container

rem タグ付け
echo start docker tag...
docker tag %DOCKER_IMAGE_NAME% %REGISTORY%/%DOCKER_IMAGE_NAME%

rem プッシュ
echo start docker push...
docker push %REGISTORY%/%DOCKER_IMAGE_NAME%

rem logout
docker logout docker.pkg.github.com

pause