# テストメソッド開発用ワークスペース

## index
* [必要環境](#必要環境)
* [開発手順](#開発手順)
* [必要ファイルの配置](#必要ファイルの配置)

## 必要環境
* docker
* docker compose

// 必要環境を細かくリストアップするのが面倒なので、とりあえずdockerとdocker composeだけ

## 開発手順
1. [必要ファイルの配置](#必要ファイルの配置)を参考にモデル・データを配置する。
2. Docker Composeの実行し、jupyterサーバーを起動する。
    ```sh
    docker compose up -d
    ```
3. ブラウザからアクセス(http://127.0.0.1:8887)
4. ノートブックを作成し、テストメソッドの開発・動作試験を行う。
   * 参考として[サンプル](http://)があります。// まだサンプルないので、リンク先不通
5. ノートブックのコードをブラッシュアップし、repository/entrypoint.pyへ配置
6. // push作業。具体的に決まっていない。


## 必要ファイルの配置
// 配置のタイミングがごっちゃになっている。「ステップ1で準備するのはコレ」、「ステップ2で準備するのはコレ」などと書くべきか？

### argsの配置
// args部分は検討中。現状、ファイル配置は省略してもOK

### inventoryの配置
モデル・データはここに配置します。
動作試験用にモデル・データを読み込ませたい場合はここに配置してください。
配置のルールは、
inventory / `任意のインベントリ名` / `モデル・データのファイル`
の様に配置してください。
* `任意のインベントリ名` は [repository/argument.yaml](#repository) で設定したインベントリ名を使用できます。インベントリ名はテストメソッド作成者が自由に設定できます。

### repository
以下の4つのファイルを順次準備してください
* repository/entrypoint.py
  * テストメソッド本体
* repository/requirements.txt
  * テストに必要なpythonライブラリのリスト
  * 書式は、pipの[Requirements Files](https://pip.pypa.io/en/latest/user_guide/#requirements-files)に従います。
* repository/argument.yaml
  * // 後で書く
* repository/readme.md
  * 説明用。省略可。
