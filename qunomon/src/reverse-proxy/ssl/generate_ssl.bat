@echo off

cd /d %~dp0

del cert\* /q /f /s

openssl genrsa -out cert\ca.key 4096

openssl req -new -sha256 -out cert\ca.csr -key cert\ca.key -config conf\ca.conf

openssl x509 -req -days 7300 -in cert\ca.csr -signkey cert\ca.key -out cert\ca.crt

openssl genrsa -out cert\server.key 2048

openssl req -new -sha256 -out cert\server.csr -key cert\server.key -config conf\server.conf

openssl x509 -req -days 7300 -CA cert\ca.crt -CAkey cert\ca.key -CAcreateserial -in cert\server.csr -out cert\server.crt -extensions req_ext -extfile conf\server.conf

pause
