# 開発用サンプルDAG

## dag.py

* airflowにデプロイするdagコード

## docker 

* dagからコールされるテストプログラム（コンテナ）

### docker/dockerfile

* コンテナビルド用のdockerfile
  * コンテナに配置するファイルなどを定義する
  * コンテナ内は以下のフォルダ構成とする
    * /usr/local/qai ... ホームディレクトリ
    * /usr/local/qai/args ... [IN]起動引数のファイル格納先ディレクトリ
    * /usr/local/qai/result ... [OUT]実行結果を格納するふぉるdふぁ
    * /usr/local/qai/inventory ... [IN]インベントリ格納フォルダ

### docker/repository/entrypoint.py

* テストプログラム本体
  * 命名は自由だが、dockerfileと同期すること
  * 引数は開発環境のjupyterから起動用jsonパスを与える用

### docker/repository/requirements.txt

* コンテナ内で使用するpythonモジュール一覧

### docker/repository/dummy_result_data

* 開発用DAG専用
  * 処理ダミー結果のコピー元

### docker/repository/dag_dev.ipynb

* 開発用のjupyter notebook

## docker_deploy.bat

* テストプログラムのコンテナをビルドしてローカルのレジストリに登録するバッチ
  * ローカルレジストリの起動：src\docker-airflow\docker-compose.yml

## launch_jupyter.bat

* テストプログラム開発用のjupyter notebookコンテナを起動するバッチ
  * コンテナ内の/tf/repositoryとホスト側のdocker\repositoryをマウントする

## meta.json

* 今後拡張予定
  * DAG自動生成の情報源に利用予定
