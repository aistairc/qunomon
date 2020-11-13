#PythonのDockerイメージを指定
FROM python:3.7

#ファイルをappディレクトリに追加
COPY script.py /app/

#ルートディレクトリ設定
WORKDIR /app

#tensorflowをpipする
RUN pip install tensorflow

CMD ["python", "script.py"]