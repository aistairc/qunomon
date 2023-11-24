# ER Diagram リバースエンジニアリング

## 前提条件

* dockerがインストールされていること

* storeage/docker-compose.ymlでDBインスタンスが起動済みであること

* backendが起動され、テーブル構造がDBに反映されていること
  ※backendを起動しないと、docker volumeで古いテーブルが残っている可能性がある

* Windows OS限定
  実行がバッチであるため。dockerコマンドをbashで起動すれば、ほかOSでも理論的には問題ない想定

## 使い方

* gen_doc.batをダブルクリックする
  output/erd.pumlが出力される

