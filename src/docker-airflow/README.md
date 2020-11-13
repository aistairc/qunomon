# airflow

## 起動方法

### (1)docker 設定

* プライベートレジストリにhttpで接続するように変更する。

`Docker Engine`  

以下を修正する。  

```
  "insecure-registries": [],
```
↓
```
  "insecure-registries": ["registry:5000"],
```
<!--
* dns設定

`Docker Engine`  

以下を追加する。  

```
  "dns": ["8.8.8.8"],
```
-->

### (2)docker-compose 起動

※重要※

以下ファイルの改行コードをCRLFからLFに修正してから、起動してください。  
改行コードを修正しないままだと、airflowのコンテナが起動しません。  
```
script\entrypoint.sh
```

docker-compose.ymlが格納されているフォルダに移動し、以下を実行する。  

```
docker-compose up -d
```

## 起動確認方法

以下にブラウザでアクセスする。
普通に画面が表示されればOK。

```
http://127.0.0.1:8080
```

## 停止方法

docker-compose.ymlが格納されているフォルダに移動し、以下を実行する。  

```
docker-compose down
```

## 掃除方法

### DAG

DAGは`dags`フォルダに格納される。  
コンテナ停止後、普通に上記フォルダから削除すればOK。  

### DB

airflowが扱うDBは、名前付きボリュームに保存している。  
動作が怪しいときは、コンテナ停止後に以下コマンドを入力し、DBを初期化する。  

```
docker volume docker-airflow_postgres10-data
```
