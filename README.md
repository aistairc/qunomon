# qunomon

## Description

A testbed for testing and managing AI system qualities.

## Demo

Sorry. Not deployment public server at alpha version.

## Requirement

### Installation prerequisites

Support os is Windows10 Pro and macOS.
* Windows10 Pro 1909 later
* macOS v10.15 later

### Installation

* [docker desktop](https://www.docker.com/products/docker-desktop) 2.3.0.3 or later

## Usage

### 1.launch

Execute the following command as root of this repository.

```sh
docker-compose up
```

### 2.access web browser

```
http://127.0.0.1:8888/
```

## Development for windows

### Installation

#### 1.PackageManager

* Launch `powershell` with administrator permission.

* powershell
    ```
    Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    ```

#### 2.Python

* powershell
    ```
    cinst python --version=3.6.8 -y
    ```

### Setup python virtual environment for Backend

#### 1.go to the source you checked out and create a virtual environment

* launch command prompt

```
cd {checkout_dir}\src\backend
python -m venv venv
```

#### 2.virtual environment activate

```
.\venv\Scripts\activate
```

#### 3.install python package

```
pip install -r requirements_dev.txt
```

### Setup python virtual environment for IP

#### 1.go to the source you checked out and create a virtual environment

* launch command prompt

```
cd {checkout_dir}\src\integration-provider
python -m venv venv
```
#### 2.virtual environment activate

```
.\venv\Scripts\activate
```

#### 3.install python package

```
pip install -r constraints.txt
```

### launch by without container

#### 1.execute bat file
```
start_up.bat
```

#### 2.checking web browser

```
http://127.0.0.1:8080/
```

#### 3.checking Backend

* powershell
    ``` 
    curl http://127.0.0.1:5000/qai-testbed/api/0.0.1/health-check
    ```

#### 4.checking IP

* powershell
    ``` 
    curl http://127.0.0.1:6000/qai-ip/api/0.0.1/health-check
    ```

## Contribution

Bug reports and pull requests are welcome on GitHub at [aistairc/qunomon](https://github.com/aistairc/qunomon).

## Disclaimer

qunomon is an OSS and alpha version.
so qunomon may cause damage to your system and data. You agree to use it at your own risk.

## License

[Apache License Version 2.0](LICENSE.txt)

## Author

[AIST](https://www.aist.go.jp/)

