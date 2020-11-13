# qai-testbed backend

※「win10 x64」が前提

## 準備

### パッケージマネージャインストール

* powershellを管理者権限で起動

* powershell
    ```
    Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    ```

### Pythonインストール

* powershell
    ```
    cinst python --version=3.6.8 -y
    ```

### 任意のパスにソースをチェックアウト

* コマンドプロンプト起動

* コマンドプロンプト
    ```
    cd {foo}
    ```

* コマンドプロンプト
    ```
    git clone git@github.com:aistairc/qai-testbed.git
    ```

### 仮想環境作成

* コマンドプロンプト
    ```
    cd {foo}\qai-testbed\src\backend
    ```

* コマンドプロンプト
    ```
    python -m venv venv
    ```

### 仮想環境アクティベート(コマンドアプリ実行時は必要)

* コマンドプロンプト
    ```
    .\venv\Scripts\activate
    ```

### 仮想環境に依存パッケージをインストール

* コマンドプロンプト
    ```
    pip install -r requirements_dev.txt
    ```

### report用にNotoフォントをインストール

* Pattern A： 手動で日本語フォントのみインストール

    以下からダウンロード＆インストール
    https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip
    zipを解凍し、fontファイルをダブルクリックし、install
    
* Pattern B： powershellから一括インストール
    ```
    cinst noto -y
    ```

## サーバ起動

* DQインスタンス起動

    ```
    cd ..\storage
    docker-compose up -d
    ```
    ※初回dockerの共有設定が出てくる場合は、任意のドライブを共有設定にする  
    ※以下からpggadminにアクセス可能　アクセスはDBのアカウントと同一  
    http://localhost:5050/browser/  
    以下に接続設定  
　　　ホスト名：psql  
　　　ポート：5432  
　　　管理用データベース：qai  
　　　ユーザ名：DBアカウント  
　　　パスワード：DBアカウント  

    インスタンスを落とす場合
    ```
    docker-compose down
    ```

    ※永続ボリュームを削除してインスタンスを落とす場合
    ```
    docker-compose down -V
    ```

* コマンドプロンプト
    ```
    python -m entrypoint startserver
    ```

## 疎通確認

* powershell
    ``` 
    curl http://127.0.0.1:5000/qai-testbed/api/0.0.1/health-check
    ```

## 自動テスト

### pycharm

Add Run/Debug Configrations

* Module name

`nose2`

* Parameters

`-v`

* Working

`{checkout_dir}\src\backend`

### console

* `{checkout_dir}\src\backend`に移動
* venv有効
* `nose2 -v`
