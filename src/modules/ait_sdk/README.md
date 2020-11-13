# AIT Software Development Kit

## Description

AITのSDKです。

## Requirement

* python 3.6.8

## Usage

N/A

## Install

### for use

```
pip install AIT_SDK-0.1.0-py3-none-any.whl
```

### for dev

* (初回だけ)仮想環境を作成

```
python -m venv venv
```

* 仮想環境アクティベート

```
.\venv\Scripts\activate
```

* (初回だけ)仮想環境に依存パッケージをインストール

```
pip install -r requirements_dev.txt
```

* wheel作成
  distにwhlファイルが作成される

```
python setup.py bdist_wheel
```

※tools\deploy.batの実行でも上記wheel作成を実行できる

## Contribution

N/A

## Licence

※TBD  

<!--
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)
-->

## Author

[AIST](https://www.aist.go.jp/)

