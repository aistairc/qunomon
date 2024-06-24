# Introduction

## Qunomon

Qunomon is a open-sourced platform for quality assessment for AI/ML systems.

It assist your AI/ML quality management through various features including (1) ML components (models/datasets) management, (2) isolated test execution environment, (3) test package management and (4) systematic report generation along with customizable guideline or standards.

In this document, we will provide you information about how to use Qunomon, with some explanation of technical terms and concepts.


## Download of Qunomon

You can download the Qunomon through our [landing page](https://aistairc.github.io/qunomon/).

## Required Software

### Installation of docker

* An environment capable of running Docker 19.03 or higher is required.
  * For Windows user, your system also must be capable of Docker Desktop 2.3.0.3 or higher.
  * For Mac user, your system also must be capable of Docker Desktop 4.20.1 or higher.
* Google Chrome may be required for correctly operating Qunomon.

## Preparations for launching Qunomon on Linux

If you are trying to launch Qunomon on Linux environment, you are required to create appropriate group and user in advance and should place the downloaded resource on specified location.

In this guide, we will create a new group named "qunomon" with group ID of 5000, and then create a new user with user ID of 50000 will be participated to that group.

### Change permissions for docker.sock

* After installing "docker", change the permissions of docker.sock using the following command.

  ```
  chmod -R 777 /var/run/docker.sock
  ```

### User create

* Create a new group.

  ```
  groupadd -g 50000 qunomon
  ```

* Create a new user assigned to the qunomon and docker group.

  ```
  useradd -u 50000 -g 50000 -G docker -m -d /home/qunomon -s /bin/bash qunomon
  ```

### Unpacking materials

Unpack and place the required materials.

* Change root privileges using the command below.
  ```
  sudo su -
  ```

* Create a directory with appropriate permission configuration.
  ```
  chmod -R 777 /home/qunomon
  mkdir -p /home/qunomon/workspace
  chmod -R 777 /home/qunomon/workspace
  ```

* Move to the workspace directory.
  ```
  cd /home/qunomon/workspace
  ```

* If you do not have the unzipping tool, install it. (If you use apt, run the following command.)
  ```
  sudo apt-get install zip unzip
  ```

* Place the zipped material (qunomon.zip) under the {/home/qunomon/workspace} and unzip it.
  ```
  unzip qunomon.zip
  ```

* After unpacking, change the permissions for each folder.
  ```
  chmod -R 777 /home/qunomon/workspace/qunomon
  chown -R qunomon /home/qunomon/workspace/qunomon/src/docker-airflow/logs
  chown -R qunomon /home/qunomon/workspace/qunomon/src/docker-airflow/dags
  ```


## Starting Qunomon

After installation, execute the following command under the "~/qunomon" directory.

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

Please open your browser and access "https://127.0.0.1".

