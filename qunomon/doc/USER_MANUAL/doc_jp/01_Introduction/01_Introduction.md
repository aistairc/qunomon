# はじめに

## Qunomonとは

QunomonはAIシステムの品質評価支援ツールです。

機械学習マネジメントガイドライン に沿ったAIシステムの品質評価とその作業環境を提供します。

## Qunomonのダウンロード
TBD

## 必要なソフトウェア

### dockerのインストール

Windows、Macなら「docker desktop」をインストールしてください。

Linuxなら「docker」をインストールしてください。

## LinuxでQunomonを立ち上げる場合の準備

LinuxでQunomonを立ち上げる場合、あらかじめグループとユーザを作成し、指定の場所にQunomonの資材を配置する必要があります。本ガイドではグループ番号50000の「qunomon」グループを作成し、作成したグループ「qunomon」に所属するユーザID「50000」のユーザを作成します。

### docker.sockの権限変更

* 「docker」インストール後、以下のコマンドでdocker.sockの権限を変更してください。
  ```
  chmod -R 777 /var/run/docker.sock
  ```

### ユーザ作成

* 以下コマンドでユーザ作成時に利用するグループを作成してください。
  ```
  groupadd -g 50000 qunomon
  ```

* 以下コマンドでqunomonグループに所属するユーザを作成してください。
  ```
  useradd -u 50000 -g 50000 -G docker -m -d /home/qunomon -s /bin/bash qunomon
  ```

### フォルダ配置

Qunomonの資材を配置します。

* 以下コマンドでルート権限を変更してください。
  ```
  sudo su -
  ```

* 以下コマンドでディレクトリを作成してください。
  ```
  chmod -R 777 /home/qunomon
  mkdir -p /home/qunomon/workspace
  chmod -R 777 /home/qunomon/workspace
  ```

* 以下コマンドでディレクトリに移動してください。
  ```
  cd /home/qunomon/workspace
  ```

* 解凍ツールがなければ、以下コマンドでインストールしてください。
  ```
  sudo apt-get install zip unzip
  ```

* ダウンロード済みのqunomon.zipファイルを{/home/qunomon/workspace}へ格納し、解凍してください。
  ```
  unzip qunomon.zip
  ```

* 解凍後、各フォルダの権限を変更してください。
  ```
  chmod -R 777 /home/qunomon/workspace/qunomon
  chown -R qunomon /home/qunomon/workspace/qunomon/src/docker-airflow/logs
  chown -R qunomon /home/qunomon/workspace/qunomon/src/docker-airflow/dags
  ```

## Qunomonの起動

～\qunomonディレクトリで以下コマンドを実行してください。

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

ブラウザで「https://127.0.0.1」を表示してください。

