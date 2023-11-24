# qai-testbed integration providor

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
    cinst python --version=3.9.13 -y
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
    cd {checkout_dir}\src\integration-provider
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
    pip install -r constraints.txt
    ```

## サーバ起動

* コマンドプロンプト
    ```
    python -m entrypoint startserver
    ```

## 疎通確認

* powershell
    ``` 
    curl http://127.0.0.1:6000/qai-ip/api/0.0.1/health-check
    ```

