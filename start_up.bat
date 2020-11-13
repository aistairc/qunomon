@echo off

cd /d %~dp0

echo start up storage...
cd .\src\storage
docker-compose up -d
cd ..\..\
echo start up storage complete

echo start up airflow...
cd .\src\docker-airflow
docker-compose up -d
cd ..\..\
echo start up airflow complete

echo start up backend...
start start_up_backend.bat
echo start up backend complete

echo start up integration provider...
start start_up_ip.bat
echo start up integration provider complete

echo start up flontend...
cd .\src\frontend
docker-compose up -d
cd ..\..\
echo start up flontend complete

pause
