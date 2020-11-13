@echo off

rem cd /d %~dp0

set DST=%~dp0docker\repository

docker run --rm -it -p 8888:8888 -v %DST%:/tf/repository -w /repository tensorflow/tensorflow:latest-py3-jupyter
