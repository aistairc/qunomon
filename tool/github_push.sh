#!/usr/bin/bash

INPUT_INVENTORY_ADD_FLAG=""
INPUT_COMMIT_COMMENT=""
COMMIT_ID=""
REPO_URL=""
REPO_NAME=""
GITHUB_ACCOUNT=""
CLONE_TYPE=""

echo -n "--- Step-1 Inventory upload? (Y:upload N:not upload) : "

while true
do
  read yn
  if [ "$yn" = "y" -o "$yn" = "Y" ]; then
    echo "Selected Inventory upload : Y"
    INPUT_INVENTORY_ADD_FLAG="Y"
    break
  elif [ "$yn" = "n" -o "$yn" = "N" ]; then
    echo "Selected Inventory upload : N"
    INPUT_INVENTORY_ADD_FLAG="N"
    break
  else 
    echo "Invalid input. Enter Y or N."
  fi
done

read -p "--- Step-2 Input commit comment." INPUT_COMMIT_COMMENT

echo Inputed commit comment : $INPUT_COMMIT_COMMENT

cd ..

REPO_URL=$(git remote get-url origin)

if [ "`echo $REPO_URL | grep 'https' `" ]; then
 CLONE_TYPE="H"
 GITHUB_ACCOUNT="`echo $REPO_URL | cut -d '/' -f 4`"
 REPO_NAME="`echo $REPO_URL | cut -d '/' -f 5`"
else 
 CLONE_TYPE="S"
 GITHUB_ACCOUNT_TEMP="`echo $REPO_URL | cut -d '/' -f 1`"
 GITHUB_ACCOUNT="`echo $GITHUB_ACCOUNT_TEMP | cut -d ':' -f 2`"
 REPO_NAME="`echo $REPO_URL | cut -d '/' -f 2`"
fi

if [ "$CLONE_TYPE" = "S" ]; then
 git remote set-url origin git@github.com:$GITHUB_ACCOUNT/$REPO_NAME
fi

git add deploy
git add develop
git add tool
git add LICENSE.txt 
git add readme.md 
git add ThirdPartyNotices.txt

if [ "$INPUT_INVENTORY_ADD_FLAG" = "Y" ]; then 
 git add local_qai/inventory
fi

git commit -m $INPUT_COMMIT_COMMENT

git push origin main

COMMIT_ID=$(git show --format="%H" --no-patch)

echo "------------------ Repository URL Start ------------------"
echo "https://github.com/$GITHUB_ACCOUNT/$REPO_NAME/tree/$COMMIT_ID"
echo "------------------ Repository URL End ------------------"

