# AIT Installer

## 前提条件

* 本プログラムでインストールする対象は、  
  あらかじめプレインストールする対象にのみ限定する。  
  テストベッドユーザが作成したAPIは含めない。

## 処理概要

コンテナ起動時にAITのインストールをする。  
具体的には、`ait`フォルダに格納される各フォルダに対して、以下2つのAPIを実行する。  

* POST /testRunners/manifest

* POST /deploy-dag-non-build

## `ait`フォルダ格納ルール

- ait
  - {AIT名称}_{AITバージョン}
    - ait.manifest.json
    - {AIT名称}_{AITバージョン}.zip

### {AIT名称}_{AITバージョン}.zipの内容物

- 圧縮するトップフォルダ名：{AIT名称}_{AITバージョン}
  - dag.py
  - container
    - dockerfile
    - repository
      - ait.manifest.json
      - ait_sdk-X.X.X-py3-none-any.whl
      - entrypoint.py
      - my_ait.py
      - requirements.txt

※プレインストールするAITはdocker build済みであるため、container配下のフォルダは不要であるが、
　docker buildを実施するAPIと互換性を持っているため、このような形式となっている。
