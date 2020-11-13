# テストランナーに搭載するDAG

## 前提条件

* python : 3.6
* aiflow : 1.10.5

## 配置フォルダ構成

* root
  * <dag_name>
    * ait.manifest.json  
      * 種類：ファイル(必須)  
      * 説明：メタ情報を格納する。
    * dag.py  
      * 種類：ファイル(必須)  
      * 説明：実行するpythonのプログラムを記載する。  
            原則はコンテナの処理を呼び出すプログラムであり、実体はコンテナで実現することを推奨する。  
            このプログラム内に記載するdag_idは{dag_name}とすること。
    * docker  
      * 種類：フォルダ(任意)  
      * 説明：コンテナ構築に必要な各種ファイルを格納する  
    * readme.md
      * 種類：ファイル(任意)  
      * 説明：説明情報を格納する。

## 命名規則

### dag_name

dag_nameは全体を通して一意になる必要がある。  
それを踏まえて、以下の命名規則に沿って定義する。  

* {prefix}\_{process_name}\_{version}
  * {prefix}
    * eval : 品質評価
    * alyz : 分析
    * mics : その他
    * dev : 開発でのみ使用
  * {process_name}
    * 処理の名称を端的に示す。  
      インプット、アウトプットの型も踏まえて命名することを推奨する。  
      たとえば精度計測でも、tensorflow用とxgboost用で分ける必要があるため。  
  * {version}
    * {メジャーバージョン}.{マイナーバージョン}とする。

## ファイル構成

### ait.manifest.json

* エンコード：utf-8

#### 以下要メンテナンス

* ファイルフォーマット

|PATH|値|型|必須/任意|備考|
|---|---|---|---|---|
|general\auther|作成者|文字列|任意||
|general\version|バージョン|文字列|任意||
|dag_id|dag_id|文字列|必須||
|dag_file|dag.pyを入力|文字列|必須||

* 記述サンプル

```
{
    "general": {
        "auther": "airc",
        "version": "1.0"
    },
    "dag_id": "dev_hello_world_0.1",
    "dag_file": "dag.py"
}
```

## AIT実行フォルダ構成

* /usr/local/qai/
  * mnt
    * mnt/ip/job_args/{job_id}/{run_id}/
      * ait.input.json
    * mnt/ip/job_result/{job_id}/{run_id}/
      * ait.output.json
  * inventory

### ait.input.json

* エンコード：utf-8

#### ファイルフォーマット

| PATH                      | 値                                          | 型     | 必須/任意 | 備考 |
|---------------------------|---------------------------------------------|--------|-----------|------|
| Inventories               | インベントリの情報が書かれたリスト          | -      | 必須      | ※A   |
| Inventories/Name          | インベントリの名前                          | 文字列 | 必須      |      |
| Inventories/Value         | インベントリのディレクトリパス              | 文字列 | 必須      |      |
| MethodParams              | AIT実行に必要なパラメータが書かれたリスト   | -      | 必須      | ※B   |
| MethodParams/Name         | パラメータの名前                            | 文字列 | 必須      |      |
| MethodParams/Value        | パラメータの値                              | 文字列 | 必須      |      |
| testbed_mount_volume_path | AITコンテナ上でのtestbed_mount_volumeのパス | 文字列 | 必須      |      |
| run_id                    | テスト実行の際に振られるrun_id              | 整数 | 必須      |      |
| job_id                    | テスト実行の際に振られるjob_id              | 整数 | 必須      |      |

* ※A：インベントリを用いないAITの場合、空リストとなる
* ※B：パラメータを用いないAITの場合、空リストとなる

#### 記述サンプル
```json
{
    "Inventories": [
        {
            "Name": "TrainedModel",
            "Value": "/usr/local/qai/mnt/ip/TrainedModel"
        }
    ],
    "MethodParams": [
        {
            "Name": "Name",
            "Value": "ODAIBA"
        }
    ],
    "testbed_mount_volume_path": "/usr/local/qai/mnt",
    "run_id": 2,
    "job_id": 2
}
```


### ait.output.json

* エンコード：utf-8

#### ファイルフォーマット

|PATH|値|型|必須/任意|備考|
|---|---|---|---|---|
|AIT/Name|実行したAITの名称|文字列|必須||
|AIT/Version|実行したAITのバージョン|文字列|必須||
|ExecuteInfo/StartDateTime|実行開始した日時|文字列(※1)|必須||
|ExecuteInfo/EndDateTime|実行完了した日時|文字列(※1)|必須||
|ExecuteInfo/Error|エラー発生時の詳細情報|-|任意|※5|
|Result|実行結果|-|必須|※6|
|Result/Measures|算出した指標値|-|任意|※2|
|Result/Measures/Name|指標名称|文字列|必須||
|Result/Measures/Value|指標値|文字列|必須||
|Result/Resources|生成したリソースファイル|-|任意|※3|
|Result/Resources/Name|リソース名称|文字列|必須||
|Result/Resources/Path|リソースファイルパス|文字列|必須||
|Result/Downloads|生成したダウンロードファイル|-|任意|※4|
|Result/Downloads/Name|ダウンロード名称|文字列|必須||
|Result/Downloads/Path|ダウンロードファイルパス|文字列|必須||

* ※1：yyyy-MM-ddThh:mm:ss+TT:TT  
    例：2018-01-02T03:04:05+09:00
* ※2：指標値を算出しないAITは、項目が存在しない
* ※3：リソースファイルを生成しないAITは、項目が存在しない
* ※4：ダウンロードファイルを生成しないAITは、項目が存在しない
* ※5：エラー発生時、項目は存在する
* ※6：エラー発生時、項目は存在しない

#### 記述サンプル

```json
{
  "AIT": {
    "Name": "dev_hello_world",
    "Version": "0.1"
  },
  "ExecuteInfo": {
    "StartDateTime": "2020-08-12T10:00:00+09:00",
    "EndDateTime": "2020-08-12T10:00:10+09:00",
  },
  "Result": {
    "Measures":[
      {
        "Name":"学習モデルの敵対的サンプル安定性計測2",
        "Value":"0.7"
      }
    ],
    "Resources":[
      {
        "Name":"acc.csv",
        "Path":"./acc.csv"
      },
      {
        "Name":"acc.png",
        "Path":"./acc.png"
      },
      {
        "Name":"images.png",
        "Path":"./images.png"
      },
      {
        "Name":"incorrect_data.csv",
        "Path":"./incorrect_data.csv"
      }
    ]
  }
}
```
