@echo off

echo begin generate DB document...

.\plant_erd_windows_386.exe postgresql ^
    --host localhost ^
    --port 5432 ^
    --user user ^
    --password pass ^
    --database qai ^
    -f %~dp0\output\erd.puml

echo complete generate DB document...

pause
