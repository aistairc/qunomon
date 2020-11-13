# VERSION 1.10.6
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

# FROM python:3.7-slim-stretch
FROM python:3.6-slim
LABEL maintainer="Puckel_"

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
#ARG AIRFLOW_VERSION=1.10.6
#ARG AIRFLOW_VERSION=1.10.10
# ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_VERSION=1.10.12
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# dag
ENV QAI_USER=root

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
    # start docker install
    && apt-get install -yqq \
        apt-transport-https \
        ca-certificates \
        software-properties-common \
        gnupg2 \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && apt-key fingerprint 0EBFCD88 \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    # ↓↓apt packegeのindexをupdate↓↓
    && apt-get update -yqq \
    # ↑↑apt packegeのindexをupdate↑↑
    && apt-get install  docker-ce docker-ce-cli containerd.io -yqq \
    # end docker install
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    # && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install SQLAlchemy==1.3.15 \
    && pip install werkzeug==0.16.0 \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
                     --constraint https://raw.githubusercontent.com/apache/airflow/1.10.10/requirements/requirements-python3.6.txt \
    #&& pip install tensorflow==1.14.0 \
    #&& pip install tfx==0.14.0 \
    #&& pip install ml-metadata \
    && pip install absl-py \
    && pip install redis==3.2 \
    && pip install docker==4.2.0 \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

# RUN chown -R airflow: ${AIRFLOW_USER_HOME}

# RUN adduser airflow docker

# unfortunately this is required to update the container docker gid to match the
# host's gid, we remove this permission from entrypoint.sh script
RUN echo "root ALL=NOPASSWD: ALL" >> /etc/sudoers
WORKDIR ${AIRFLOW_HOME}/.docker

# # set use sudo and set password
# RUN gpasswd -a airflow sudo \
#     && echo "airflow:pass" | chpasswd \
#     && gpasswd -a airflow docker

EXPOSE 8080 5555 8793

# mound root dir
RUN mkdir ./ip

USER ${QAI_USER}
# USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint
