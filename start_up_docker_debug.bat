@echo off
docker-compose -f docker-compose.yml -f dc-debug-option.yml up -d
echo 【説明】
echo Docker環境でデバッグモードとして開始しました。
echo VSCodeの「Run(実行)」からbackendとipのデバッグを開始させてください。
echo 注: デバッグを実行しない限り、backendやipは停止したままになります。片方だけデバッグする場合でも、両方のデバッグを実行してください。
echo 【プログラムの終了】
echo `docker-compose down` (一般的なdocker-composeコマンドと同様のコマンドです。)