# コンテナ起動用PostgreSQLのコンテナ作成

* 非コンテナ起動では使用しない。  
　（バックエンドがDB初期化を実施するため）

# SQL作成方法

前提条件：
* DBコンテナが使用するボリュームはあらかじめ削除しておくこと
　ボリュームが残っていると、シーケンス部分が初期化されない
* DBコンテナが起動し、さらにバックエンドで初期化終了済みの状態であること

## DDL生成
```
docker exec -it psql pg_dump -h localhost -p 5432 -d qai -s -U user -E SJIS > DDL.sql
```

## DML生成
```
docker exec -it psql pg_dump -h localhost -p 5432 -d qai -a --column-inserts -E SJIS -U user > DML.sql
```
