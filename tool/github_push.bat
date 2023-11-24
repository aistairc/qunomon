@echo off

echo #####AIT GITHUB PUSH#####

set INPUT_INVENTORY_ADD_FLAG=
set INPUT_COMMIT_COMMENT=
set COMMIT_ID=
set REPO_URL=
set REPO_NAME=
set GITHUB_ACCOUNT=
set CLONE_TYPE=

choice /c YN /m "--- Step-1 Inventory upload? (Y:upload N:not upload) : " /n
if errorlevel 1 set INPUT_INVENTORY_ADD_FLAG=Y
if errorlevel 2 set INPUT_INVENTORY_ADD_FLAG=N

echo Selected Inventory upload : %INPUT_INVENTORY_ADD_FLAG%

echo --- Step-2 Input commit comment.
set /P INPUT_COMMIT_COMMENT=


echo Inputed commit comment : %INPUT_COMMIT_COMMENT%

cd ..

git remote get-url origin > repo_url.txt
for /f "tokens=1" %%a in (repo_url.txt) do (
  set REPO_URL=%%a
)
del repo_url.txt

echo "%REPO_URL%" | find "https" >NUL
if %errorlevel%==0 (
  set CLONE_TYPE=H
  for /f "tokens=3-4 delims=/" %%a in ("%REPO_URL:~0,-4%") do (
    set GITHUB_ACCOUNT=%%a
    set REPO_NAME=%%b
  )
) else (
  set CLONE_TYPE=S
  for /f "tokens=2-3 delims=:/" %%a in ("%REPO_URL:~0,-4%") do (
    set GITHUB_ACCOUNT=%%a
    set REPO_NAME=%%b
 )

)

if %CLONE_TYPE%==S (
  git remote set-url origin git@github.com:%GITHUB_ACCOUNT%/%REPO_NAME%.git
)

git add deploy
git add develop
git add tool
git add LICENSE.txt
git add readme.md
git add ThirdPartyNotices.txt

if %INPUT_INVENTORY_ADD_FLAG%==Y (
 git add local_qai/inventory
)

git commit -m %INPUT_COMMIT_COMMENT%

git push origin main

if %errorlevel% neq 0 (
  echo Failed push to Github.
  PAUSE
  EXIT
)

git show --format="%%H" --no-patch > commit_id.txt
for /f "tokens=1" %%a in (commit_id.txt) do (
  set COMMIT_ID=%%a
)
del commit_id.txt

echo ----------- Repository URL Start----------
echo https://github.com/%GITHUB_ACCOUNT%/%REPO_NAME%/tree/%COMMIT_ID%
echo ----------- Repository URL End-----------

PAUSE
EXIT