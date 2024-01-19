# Introduction

## Qunomon

Qunomon is a quality assessment support tool for AI systems.

qunomon provides quality assessment of AI systems in line with machine learning management guidelines, and working environment.


## Download of Qunomon

TBD

## Required Software

### Installation of docker

If you are on Windows or Mac, install "docker desktop"

If you are on Linux, install "docker".

## Preparations for launching Qunomon on Linux

When starting Qunomon on Linux, you need to create groups and users in advance and place the Qunomon folder in the specified location. In this guide, we will create a group "qunomon" with group number 50000, and create a user with user ID "50000" who belongs to the created group "qunomon".

### Change permissions for docker.sock

* After installing "docker", change the permissions of docker.sock using the following command.
  ```
  chmod -R 777 /var/run/docker.sock
  ```

### User create

* Create a group to be used when creating users using the command below.
  ```
  groupadd -g 50000 qunomon
  ```

* Create a user belonging to the qunomon group using the command below.
  ```
  useradd -u 50000 -g 50000 -G docker -m -d /home/qunomon -s /bin/bash qunomon
  ```

### Folder arrangement

Place the Qunomon folder.

* Change root privileges using the command below.
  ```
  sudo su -
  ```

* Create a directory using the command below.
  ```
  chmod -R 777 /home/qunomon
  mkdir -p /home/qunomon/workspace
  chmod -R 777 /home/qunomon/workspace
  ```

* Move to the directory using the command below.
  ```
  cd /home/qunomon/workspace
  ```

* If you do not have the unzipping tool, install it using the command below.
  ```
  sudo apt-get install zip unzip
  ```

* Store the downloaded qunomon.zip file in {/home/qunomon/workspace} and unzip it.
  ```
  unzip qunomon.zip
  ```

* After unzipping, change the permissions for each folder.
  ```
  chmod -R 777 /home/qunomon/workspace/qunomon
  chown -R qunomon /home/qunomon/workspace/qunomon/src/docker-airflow/logs
  chown -R qunomon /home/qunomon/workspace/qunomon/src/docker-airflow/dags
  ```


## Starting Qunomon

Please execute the following command in the "(root)/qunomon" directory

* Windows  
  ```sh
  docker compose up -d
  ```
* Mac  
  ```sh
  sudo docker compose -f docker-compose.yml -f docker-compose-mac.yml up -d
  ```
* Linux  
  ```sh
  sudo docker compose up -d
  ```

Please view "https://127.0.0.1" in your browser.

