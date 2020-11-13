# AIT AITDevTool

## Description

It will be integrated into AIT Studio.  
Used as a preliminary version of the alpha version.

AIT's development environment, all in docker.

---

いずれAIT Studioに統合する。  
α版の暫定バージョンとして利用。  

AITの開発環境、すべてdockerで用意する。

### Folder Structure

* root
  * mnt : Folders mounted by docker. * mnt : Folders mounted by docker.
  * env : a folder which manages docker images for each ML engine.
    * {XXX}/docker-compose.yml 
  * launch_{XXX}.bat : Launch batch of development environment. {XXX} is the ML engine and version.
  * README.md

Create a folder for each ML engine with the following basic set of development environment.
* jupyter notebook
* eclipse theia

---

* root
  * mnt : dockerでマウントされるフォルダ。開発用のデータや、開発したAITが格納される。
  * env : MLエンジンごとに起動するdockerimageを管理するフォルダ。
    * {XXX}/docker-compose.yml 
  * launch_{XXX}.bat : 開発環境起動バッチ。{XXX}はMLエンジン、バージョンが記載される。
  * README.md

開発環境は以下を基本セットとし、MLエンジンごとにフォルダを作成する
* jupyter notebook
* eclipse theia

## Requirement

* Windows 10 Pro x64 / version 1909
* docker desktop 2.3.0.4 or late
* Google Chrome 84.0.4147.125 or late

## Usage

Double-click on the following
````
launch_tf23.bat
````

---

以下をダブルクリック
```
launch_tf23.bat
```

## Install

### docker desktop

https://download.docker.com/win/stable/Docker%20Desktop%20Installer.exe

### Google Chrome

https://www.google.com/intl/ja_jp/chrome/

## Contribution

N/A

## Licence

※TBD  

<!--
[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)
-->

## Author

[AIST](https://www.aist.go.jp/)

