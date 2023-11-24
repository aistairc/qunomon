#!/bin/bash

YML="$(dirname "$0")/docker/docker-compose.yml"

echo "Launching docker containers."
echo $YML

cp ../deploy/container/resolve-dependencies.sh docker/jupyter/resolve-dependencies.sh
docker compose -f $YML build
docker compose -f $YML up -d

echo
echo "Please wait while launching docker containers..."
sleep 3

echo "Opening Jupyter environment."
echo
JUPYTER_URL="http://localhost:9888?token=token"
if [[ "$(uname)" == "Darwin" ]]; then
  if [ -d "/Applications/Google Chrome.app" ]; then
    open -a "Google Chrome" "$JUPYTER_URL"
  else
    open "$JUPYTER_URL"
  fi
else
  su $(logname) -c "google-chrome \
    --app=$JUPYTER_URL \
    --disable-background-mode \
    --disable-extensions \
    2>/dev/null &"
fi

read -p "Do you want to stop and remove related docker containers? (y/n) " answer
if [ "$answer" = "y" ]; then
  docker compose -f $YML down
fi

read -p "Press ENTER to continue..." answer
