# はじめに

## Qunomonとは

QunomonはAIシステムの品質評価支援プラットフォームです。

Qunomonは、機械学習コンポーネントの管理、独立したテスト実行環境、ガイドラインや標準と紐づいた体系的な評価結果の管理を通じて、品質評価者の活動を助けます。

本資料では、Qunomonの使用方法を、用語や概念の簡単な解説とともに提供します。

## Qunomonのダウンロード

[Qunomonのランディングページ](https://aistairc.github.io/qunomon/) から、DOWNLOADボタンを押下してQunomonをダウンロードしてください。

## 必要なソフトウェア

### dockerのインストール
* Docker 19.03 以上が動作可能な環境が必要です。
  Windowsにおいては、Docker Desktop 2.3.0.3 以降が動作可能な環境が必要です。
  macOSにおいては、Docker Desktop 4.20.1 以降が動作可能な環境が必要です。
* Windowsにおいては、動作にGoogle Chromeが必要です。

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

``` note:: /home/qunomon/workspaceの下に既にα版qunomonフォルダが存在する場合は全て削除してください。
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

~\qunomonディレクトリで以下コマンドを実行してください。

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

Qunomonの実行には下記ポートを使用します。他のアプリケーションでは下記ポートを使用しないでください。  
・443  
・5050  
・5051  
・5432  
・5433  
・6000  
・8000  
・8180  
・8888  
