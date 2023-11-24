# qai-testbed backend(report)

※「win10 x64」が前提

※reportは最終的にはbackendに組み込まれるため、ディレクトリ構成は変更されている可能性あり

## 準備

```
cd {checkout_dir}\src\backend\report
```

### 依存パッケージをインストール

* コマンドプロンプト
    ```
    pip install -r constraints.txt
    ```

※constraints.txtには、backend（API）側で必要なパッケージも含まれる

### wkhtmltopdfをインストール

    wkhtmltopdf:0.12.5を以下からインストール
    https://github.com/wkhtmltopdf/wkhtmltopdf/releases/0.12.5/
    
    64bit : wkhtmltox-0.12.5-1.msvc2015-win64.exe
    

### Notoフォントをインストール

* Pattern A： 手動で日本語フォントのみインストール

    以下からダウンロード＆インストール
    https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip
    zipを解凍し、fontファイルをダブルクリックし、install
    
* Pattern B： powershellから一括インストール
    ```
    cinst noto -y
    ```
    
### 環境変数の追加

コントロールパネルの「環境変数を編集」から、Pathに以下を追加する
```
C:\Program Files\wkhtmltopdf\bin
```

## レポート生成の確認

* PyCharmのターミナル
    ```
    python main.py
    ```
