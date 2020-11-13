@echo off

echo begin generate DB document...

rem docker実行
docker run ^
    -v %~dp0\output:/output ^
    --net="host" ^
    schemaspy/schemaspy:6.1.0 ^
    -t pgsql ^
    -host localhost:5432 ^
    -db qai ^
    -u user ^
    -p pass

echo complete generate DB document...

pause
