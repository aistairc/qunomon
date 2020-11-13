# ThirdPartyNoticesMaker

## 必要ファイル
* 1_preface.txt
    * 序文
    * 基本的に編集しなくてよい
* license_table.tsv
    * 以下の列で書かれたtsv
    * 列
        * ソフト名
        * バージョン
        * ライセンス名
            * 新たにライセンスを追加したい場合は `license_templete/{ライセンス名}`に配置してください。
        * リリース年
            * 最初にリリースした年
        * 権利者
        * ライセンスが掲載されているページのURL
* license_templete/{ライセンス名}
    * ライセンスの本文
    * `{変数名}`と書くことで、license_table.tsvに書かれた値を代入することができます
      | 変数名  | 列名       |
      |---------|------------|
      | name    | ソフト名   |
      | version | バージョン |
      | since   | リリース年 |
      | owner   | 権利者     |

## 使い方
1. プログラム起動
  ```sh
  python make_notice.py
  ```

2. プロジェクトのルートディレクトリに `ThirdPartyNotices.txt` が作成されます。
