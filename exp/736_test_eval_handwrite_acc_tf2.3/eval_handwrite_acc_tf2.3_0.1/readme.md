# 手書き学習モデル精度計測 AIT

## description

* ait.manifest.jsonを参照

## フォルダ構成

### dev

#### dev/repository

  * ait.manifest.json  
    AIT開発者：編集する  

  * AIT_SDK-0.1.0-py3-none-any.whl  
    AITの開発モジュール。  
    AIT開発者：最新のモジュールを配置する  

  * entrypoint.py  
    コンテナ内で起動する入口のpythonファイルとなる。  
    AIT開発者：編集しない  

  * my_ait.py  
    AITの本処理を記載する。  
    AIT開発者：編集する  

  * requirements.txt  
    必要とするpythonモジュールを記載する。  
    AIT開発者：編集する  

#### exp

  * 実験用ファイル格納フォルダ

### local_qai

* theiaで開発するときのマウントフォルダ  
  * downloads  
    outputフォルダ  
    AIT実行後、「downloads」が格納される  

  * inventory  
    inputフォルダ  
    AIT実行前、「inventory」を格納する  

  * mnt/ip/job_args/{job_id}/{run_id}  
    inputフォルダ  
    AIT実行前、「ait.input.json」を格納する  

  * mnt/ip/job_result/{job_id}/{run_id}  
    outputフォルダ  
    AIT実行後、「ait.output.json」が格納される  

  * resources  
    outputフォルダ  
    AIT実行後、「resources」が格納される  

#### フォルダ例

```
├─downloads
│  │  .gitignore
│  │
│  ├─1
│  │      ait.log
│  │
│  └─2
│          prediction.csv
│
├─inventory
│  ├─test set images
│  │      t10k-images-idx3-ubyte.gz
│  │
│  ├─test set labels
│  │      t10k-labels-idx1-ubyte.gz
│  │
│  └─trained model
│          model_1.h5
│
├─mnt
│  └─ip
│      ├─job_args
│      │  └─1
│      │      └─1
│      │              ait.input.json
│      │
│      └─job_result
│          └─1
│              └─1
│                      .gitignore
│                      ait.output.json
│
└─resources
    │  .gitignore
    │
    ├─1
    │      confusion_matrix.csv
    │
    ├─2
    │      confusion_matrix.png
    │
    ├─3
    │      roc_curve.png
    │
    └─4
            ng_predict_actual_class_0.png
            ng_predict_actual_class_1.png
            ng_predict_actual_class_2.png
            ng_predict_actual_class_3.png
            ng_predict_actual_class_4.png
            ng_predict_actual_class_5.png
            ng_predict_actual_class_6.png
            ng_predict_actual_class_7.png
            ng_predict_actual_class_8.png
            ng_predict_actual_class_9.png
```

### Tools
  * launch_theia.bat  
    theiaコンテナ起動するためのバッチファイル  

  * launch_jupyter.bat  
    jupyter notebookコンテナ起動するためのバッチファイル  

  * docker_deploy.bat  
    AITをコンテナ化するためのバッチファイル  

  * TheiaTools  
    * TheiaTools/README.mdを参照  
