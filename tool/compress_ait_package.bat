rem LICENSE
rem (1)This uses part of the 7-Zip program.
rem (2)7-Zip is licensed under the GNU LGPL
rem (3)Source code URL (www.7-zip.org)

@echo off

set exe="./compress_exe/7za.exe"

@REM define what to compress
set target_file="../deploy/container/*"

@REM define zipfile name
for %%I in ("%~dp0\..") do set FILE_NAME=%%~nI.zip

@REM make zipfile
call %exe% a -tzip "%FILE_NAME%" "%target_file%"

pause
