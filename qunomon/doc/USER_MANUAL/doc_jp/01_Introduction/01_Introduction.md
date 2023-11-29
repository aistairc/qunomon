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

