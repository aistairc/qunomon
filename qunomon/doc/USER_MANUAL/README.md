# AIT Guid

## Description

AITのガイドドキュメントです。  
sphinxを利用して、markdownからhtmlを生成します。  

## Requirement

* python 3.6.8

## Usage

N/A

## Install

### for generate

* 仮想環境アクティベート

    ```
    .\venv\Scripts\activate
    ```

* ビルド

    ```
    sphinx-build -b html .\doc .\doc\_build
    sphinx-build -b html .\doc_jp .\doc_jp\_build
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
    pip install -r requirements.txt
    ```

* (初回だけ)pandocをインストール ※要管理者権限

    ```
    choco install pandoc
    ```

## Contribution

N/A

## Licence

※TBD  

<!--
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)
-->

## Author

[AIST](https://www.aist.go.jp/)

