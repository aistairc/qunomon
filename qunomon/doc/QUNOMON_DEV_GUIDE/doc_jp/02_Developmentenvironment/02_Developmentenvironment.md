# プログラミング言語

* Python3.9

バックエンド開発で使用します。

* Javascript(Vue.js)

フロントエンド開発で使用します。

# エディタ

VisualStudioCodeを推奨しています。

# Docker

本アプリを動作させるにはDocker環境が必要です。

Docker環境の詳細は{/qunomon/docker-compose.yml}を参照してください。

# 開発環境構築手順

* VScodeとアドオンのインストール
  * VScodeのインストール

  　  https://azure.microsoft.com/ja-jp/products/visual-studio-code/ 

* フロントエンド環境

  フロントエンドはVScodeを使用して開発することを推奨しています。

  * Docker for Windowsのインストール
   
    インストーラー: https://docs.docker.com/docker-for-windows/install/

  * Chromeのアドオンに以下をインストールする
    
    Vue.js devtools
    
    Allow CORS: Access-Control-Allow-Origin

  * qai-testbedディレクトリ直下のstart_up.batを実行する

  * Allow CORS: Access-Control-Allow-OriginをONの状態にする

  * https://127.0.0.1:443/ にアクセスする

  * 開発者コンソールツールを開き、Vueのタブを開く
    
    詳細は以下リンクを参考

    https://qiita.com/hashimoto-1202/items/c81f5d4c271eef16d957

* バックエンド、実行基盤

バックエンドはVScodeを利用して開発することを推奨しています。

  * パッケージマネージャをインストール
    
    管理者権限でpowershellを開く

    以下のコマンドを実行し、パッケージマネージャをインストール
    ```
    Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    ```
  
  * Pythonをインストール

    以下のコマンドを実行し、Pythonをインストール

    ```
    cinst python --version=3.9.13 -y
    ```
  
  * RESTテスト

    VSCode拡張にREST Clientをインストールします。

  * デバッグ環境と手順

    （初回のみ（前提として、src\backend\readme.md および src\integration-provider\readme.md の手順を実行済みとする） ）

  * 以下のパスでVSCodeを開く
    * backendの場合は「src\backend」
    * ipの場合は「src\integration-provider」
  
    （以降は都度実行する）

    qai-testbedディレクトリ直下のstart_up.batを実行する。

    ポートを開放するため、start_up.batで起動していたbackendとipのコンソールを終了（Ctrl + C）する。

    VSCodeでbackendとipにあるentrypointをデバッグ起動する。

    各種APIの試験を行いたい場合は、以下ファイルからAPIのテストが行える。
    
    src\backend\backend_rest_test.http
    
    src\integration-provider\integration_provider_rest_test.http
    
    ※ VSCodeでREST Client をインストールしておく必要がある。

* Docker環境下での動作方法

  本番すなわちDocker環境とデバッグ（venvの仮想環境）での動作方法は異なります。（backendなどの環境をDocker環境下で動かすか、venvの仮想環境で動かすかの違い） そのため、デバッグ環境で実行することが確認できても、Docker環境下でも正しく動作するかどうかは別途確認する必要性があります。

  * Chromeへ証明書を導入する

  * VScodeのターミナルでqai-testbedディレクトリに移動して、以下を実行する

    * Product environment （リリース版）
      ```
      docker compose up
      ```

  * フロントエンドにはhttps://127.0.0.1:443/ にアクセスする

  * 各種APIの試験を行いたい場合は、以下ファイルをVSCodeで開いてAPIのテストが行える。
    src\backend\backend_rest_test_docker.http
    src\integration-provider\integration_rest_test_docker.http
    ※ VSCodeでREST Client をインストールしておく必要がある。

  * ※ Docker環境で動かす場合、以下のような変更を行った場合は、必要に応じてcontainerやvolume、image削除や、再buildを実行すること。
    * Dockerfile、docker-compose.ymlを編集した。
    * ReportGeneratorを編集した。

* plantuml
  
  各種設計資料はplantumlで記載しています。


