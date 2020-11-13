#!/usr/bin/env bash

# DOCKER_SOCKET=/var/run/docker.sock
# DOCKER_GROUP=docker
# AIRFLOW_USER=airflow

# # In order run DooD (Docker outside of Docker) we need to make sure the
# # container's docker group id matches the host's group id. If it doens't match,
# # update the group id and then restart the script. (also remove sudoer privs)
# if [ ! -S ${DOCKER_SOCKET} ]; then
#   echo 'Docker socket not found!'
# else
#   DOCKER_GID=$(stat -c '%g' $DOCKER_SOCKET)
#   if $(id -G $AIRFLOW_USER | grep -qw $DOCKER_GID); then
#     echo "User $AIRFLOW_USER in the correct host docker groupid $DOCKER_GID"
#   else
#     echo "User $AIRFLOW_USER not in the correct group $DOCKER_GID"
#     echo "Updating docker group to host docker group $DOCKER_GID"
#     sudo groupmod -g ${DOCKER_GID} ${DOCKER_GROUP}
#     # it doens't protect from docker but it's a little more secure
#     sudo sed -i "/$AIRFLOW_USER/d" /etc/sudoers
#     echo "Restarting script"
#     exec sg $DOCKER_GROUP "$0 $*"
#   fi
# fi

TRY_LOOP="20"

: "${REDIS_HOST:="redis"}"
: "${REDIS_PORT:="6379"}"
: "${REDIS_PASSWORD:=""}"

# to set docker-compose
#: "${POSTGRES_HOST:="postgres"}"
#: "${POSTGRES_PORT:="5432"}"
#: "${POSTGRES_USER:="airflow"}"
#: "${POSTGRES_PASSWORD:="airflow"}"
#: "${POSTGRES_DB:="airflow"}"

# Defaults and back-compat
: "${AIRFLOW_HOME:="/usr/local/airflow"}"
: "${AIRFLOW__CORE__FERNET_KEY:=${FERNET_KEY:=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")}}"
: "${AIRFLOW__CORE__EXECUTOR:=${EXECUTOR:-Sequential}Executor}"

export \
  AIRFLOW_HOME \
  AIRFLOW__CELERY__BROKER_URL \
  AIRFLOW__CELERY__RESULT_BACKEND \
  AIRFLOW__CORE__EXECUTOR \
  AIRFLOW__CORE__FERNET_KEY \
  AIRFLOW__CORE__LOAD_EXAMPLES \
  AIRFLOW__CORE__SQL_ALCHEMY_CONN \

if [ -e /var/run/docker.sock ]; then 
  echo "set permission docker.sock..."
  chgrp docker /var/run/docker.sock
  echo airflow | sudo -S chmod 777 /var/run/docker.sock; 
fi

# Load DAGs exemples (default: Yes)
if [[ -z "$AIRFLOW__CORE__LOAD_EXAMPLES" && "${LOAD_EX:=n}" == n ]]
then
  AIRFLOW__CORE__LOAD_EXAMPLES=False
fi

# Install custom python package if requirements.txt is present
if [ -e "/requirements.txt" ]; then
    $(command -v pip) install --user -r /requirements.txt
fi

if [ -n "$REDIS_PASSWORD" ]; then
    REDIS_PREFIX=:${REDIS_PASSWORD}@
else
    REDIS_PREFIX=
fi

wait_for_port() {
  local name="$1" host="$2" port="$3"
  local j=0
  while ! nc -z "$host" "$port" >/dev/null 2>&1 < /dev/null; do
    j=$((j+1))
    if [ $j -ge $TRY_LOOP ]; then
      echo >&2 "$(date) - $host:$port still not reachable, giving up"
      exit 1
    fi
    echo "$(date) - waiting for $name... $j/$TRY_LOOP"
    sleep 5
  done
}

if [ "$AIRFLOW__CORE__EXECUTOR" != "SequentialExecutor" ]; then
  AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"
  AIRFLOW__CELERY__RESULT_BACKEND="db+postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"
  wait_for_port "Postgres" "$POSTGRES_HOST" "$POSTGRES_PORT"
fi

if [ "$AIRFLOW__CORE__EXECUTOR" = "CeleryExecutor" ]; then
  AIRFLOW__CELERY__BROKER_URL="redis://$REDIS_PREFIX$REDIS_HOST:$REDIS_PORT/1"
  wait_for_port "Redis" "$REDIS_HOST" "$REDIS_PORT"
fi

case "$1" in
  webserver)
    airflow initdb
    if [ "$AIRFLOW__CORE__EXECUTOR" = "LocalExecutor" ] || [ "$AIRFLOW__CORE__EXECUTOR" = "SequentialExecutor" ]; then
      # With the "Local" and "Sequential" executors it should all run in one container.
      airflow scheduler &
    fi
    exec airflow webserver
    ;;
  worker|scheduler)
    # To give the webserver time to run initdb.
    sleep 10
    exec airflow "$@"
    ;;
  flower)
    sleep 10
    exec airflow "$@"
    ;;
  version)
    exec airflow "$@"
    ;;
  *)
    # The command is something like bash, not an airflow subcommand. Just run it in the right environment.
    exec "$@"
    ;;
esac
