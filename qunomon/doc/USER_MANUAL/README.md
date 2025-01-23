# Qunomon利用者マニュアル

## Description

AITのガイドドキュメントです。
sphinxを用いてドキュメント作成を行っています。
ドキュメントコンパイル手順に従うことで、利用者の環境でドキュメントを執筆・ビルドできます。

## Requirement

* python 3.9.13

## Usage

ドキュメントの更新・別所でのホスティングなどに用いることができます。
公式の最新版ドキュメントはWebページからも閲覧できます。

## ドキュメントビルド手順
### ビルド実行

* 仮想環境アクティベート

    ```
    .\venv\Scripts\activate
    ```

* ビルド

    ```
    sphinx-build -b html .\doc .\doc\_build
    sphinx-build -b html .\doc_jp .\doc_jp\_build
    ```

### ビルド用環境の準備

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

