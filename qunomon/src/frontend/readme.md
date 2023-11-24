- コマンドプロンプト

```
cd {checkout_dir}\src\frontend

docker-compose up -d
```

- フロントエンドへのアクセス

  http://127.0.0.1:8080/

  **通常ではDBと通信を行う際にCORSエラーが発生するため、現状は下記のChromeアプリを追加するなどして対処する必要がある。**

  https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf?utm_source=chrome-ntp-icon


- インスタンスを落とす場合

```
docker-compose down
```
