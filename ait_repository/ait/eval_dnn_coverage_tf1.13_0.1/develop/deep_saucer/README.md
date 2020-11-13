# DeepSaucer

Integrated GUI to manage multiple test and verification functions with different execution environments

See https://arxiv.org/abs/1811.03752

## Environment (operation verified)
* Ubuntu&trade; 17.10 & Anaconda&reg; 3

## Required Libraries
* flask (`conda install flask`)
* PyYAML (`conda install pyyaml`)

## Start-up
python deep_saucer_core/main.py

## Register Script
### Anaconda&reg; Virtual Environment Creation Script

Registering a script to build an environment for executing test functions

Select from the menu bar as follows:

```
「File」-「Add Env Setup Script」
```

In the environment creation script, be sure to execute conda create in the format.

```sh
conda create -n 【ENV_NAME】... -y
```


Script Example：
```sh
#!/bin/bash
conda create -n dnn_encoding python=3.6 -y
source activate dnn_encoding
pip install tensorflow==1.12.0
pip install z3-solver
pip install pyparsing

```

---
### Verification Script
Registering the test function executed by DeepSaucer

1. Select `「File」-「Add Verification Script」` from the menu bar
2. Select the script file (* .py) to register
3. Select an Anaconda&reg; virtual environment creation script to be used for script execution from the list

In this script, be sure to implement the function

```python
def main(model, dataset=None, config_path=None):

```

format．

DeepSaucer will invoke this function when the test function is executed．

**It is strongly recommended that you check the model and learned data passed as arguments at the beginning of main function processing.**

The return value of the function invoked from Model Load Script specified at the time of execution is passed to the 1st argument 'model'.

The return value of the function invoked from Dataset Load Script specified at the time of execution is passed to the 2nd argument 'dataset'.

The absolute path (string) of the config file specified at the time of execution is passed to the 3rd argument 'config_path'.

'dataset', 'config_path' are optional.

---
### Test Dataset Load Script

Register a script to load and process the test data to be used for the test function execution

1. Select `「File」-「Add Test Dataset Load Script」` from the menu bar
2. Select the script file (*.py) to register
3. Select an Anaconda&reg; virtual environment construction script to be used for script execution from the list

In this script, be sure to implement the function

```python
def data_create(downloaded_data):
```



The absolute path (string) of the `deep_saucer_core/downloaded_data` will be passed to the argument `downloaded_data`.

Specify the object of the test data and the path of the saved data as the return value of the function．

DeepSaucer invokes this function when the test function is executed, and passes the return value to the main function implemented in Verification Script．

Script Example：[dataset_ref_model.py](deep_saucer_core/gtsrb/data/dataset_ref_model.py)

---
### Model Load Script

Register a script to load a learned model used in the test function execution

1. Select `「File」-「Add Model Load Script」` from the menu bar
2. Select the script file (*.py) to register
3. Select an Anaconda&reg; virtual environment creation script to be used for script execution from the list

In this script, be sure to implement the function

```python
def model_load(downloaded_data):
```



The absolute path (string) of `deep_saucer_core/downloaded_data` will be passed to the argument `downloaded_data`.

Specify the object of the learned model and the path of the saved model as the return value of the function.

DeepSaucer invokes this function when the function is executed and passes the return value to the main function implemented in `Verification Script`.

Script Example：[model_ref_model.py](deep_saucer_core/gtsrb/model/model_ref_model.py)

---
### Output to DeepSaucer

You can display the standard output on the DeepSaucer console by including

```
print('xxxx')
```

to these `Verification Script`，`Test Dataset Load Script`，`Model Load Script`．

## Executing the Test Function

1.  Select `Verification Script`，`Test Dataset Load Script`，`Model Load Script` from the DeepSaucer screen．(Scripts grayed out after script selection cannot be selected. If Dataset Load Script does not use any scripts, selection can be omitted)
2.  Select `「Run」-「Run Test Function」` from the menu bar
3.  Select `Next` if you want to use the Configuration file to be used for execution．Select `Run` if you want to run without using it.
4.  (When `Next` is selected) Select the Configuration file to be used for execution from `Select`，then select `Run`.

DeepSaucer generates and executes [such a script](deep_saucer_core/tmp/20190219141253_tmp_test_exec.py) from the selected script.
