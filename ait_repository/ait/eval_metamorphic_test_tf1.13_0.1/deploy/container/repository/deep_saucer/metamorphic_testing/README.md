# Metamorphic Testing
The output value of DNN when x is accepted as an input value is denoted as DNN(x). A function for checking whether DNN(T(x)) = S(DNN(x)) will be established for the function T for converting x, and the function S for converting DNN(x). DNN(T<sup>n</sup>(x)) = S(DNN(x)) can be checked by changing "number of input data conversion = n" in the config file.

## Requirement
* python 3.6
* See [lib/metamorphic_testing_setup.sh](lib/metamorphic_testing_setup.sh)

## Tutorial
* There are 2 ways to use this function: importing as a module and invoking from DeepSaucer.

* When used as a module: [1. Common operation](#1-common-operation) → [2. Direct execution](#2-direct-execution) → [4. Output ](#4-output)
* When invoked from DeepSaucer: [1. Common operation](#1-common-operation) → [3. Invoking from DeepSaucer](#3-invoking-from-deepsaucer) → [4. Output ](#4-output)


### 1. Common Operation
---
1. **Create the following files**
   * Structure Information File (json format)<br>ex) [examples/mnist/model/model_mnist.ckpt_name.json](examples/mnist/model/model_mnist.ckpt_name.json)<br>

   * Variable Name List<br>ex) [examples/mnist/model/vars_list.txt](examples/mnist/model/vars_list.txt)<br>

   **Automatic Generation Method**
     1. Prepare code that uses the model definition from existing Python code ([examples/mnist/train_and_create_struct.py](examples/mnist/train_and_create_struct.py))
     1. Include the instance creation of the NetworkStruct class of structutil.py in the code (line: [32](examples/mnist/train_and_create_struct.py#L32))
     1. Add `set_input` processing taking the placeholder used as input on the model definition (line: [41](examples/mnist/train_and_create_struct.py#L41))
     1. Add `set_output` processing taking the `node used as output` on the model definition code (line: [76](examples/mnist/train_and_create_struct.py#L76))
     1. After the model training process, add `set_info_by_session` processing taking `Session` (line: [103](examples/mnist/train_and_create_struct.py#L103))
     1. Add `save` processing taking `Session` and `model output destination path` (line: [105](examples/mnist/train_and_create_struct.py#L105))
     1. Add `print_vars` process taking the `destination file stream` (line: [112](examples/mnist/train_and_create_struct.py#L112))

   **Manual Generation**
     1. Create a json file with the following content
        ```json
        {
          "input_placeholder": [
            {
              "name": "Placeholder_Name_XX",
              "shape": "(X, Y)"
            },
            {
              "name": "Placeholder_Name_YY",
              "shape": "(X, Y)"
            }, ...
          ],
          "out_node": {
            "name": "Out_Node_Name_XX",
            "shape": "(X, Y)"
          }
        }
        ```

        **json Structure**
        * **input_placeholder**

            | Name | Value | Description |
            | ---- | ---- | ---- |
            | input_placeholder | List | Dictionary using the following "name", "shape", "description" as the key |
            | name | String | Input Placeholder Name |
            | shape | String | Input Placeholder Shape |
            | description | String | Input Placeholder Description (optional)<br>When describing in the json list format, the explanation is displayed for each shape at the time of the variable name listing<br>Example: <br>"name": "VAR1",<br>"shape": "(1, 3)",<br>"description": "[\\"value0\\", \\"value1\\", \\"value2\\"]"<br><br>Variable Name List<br>Input:<br>VAR1_0 : value0<br>VAR1_1 : value1<br>VAR1_2 : value2<br> |

        * **output_node**

            | Name | Value | Description |
            | ---- | ---- | ---- |
            | output_node | Dictionary | Use the dictionary with the following "name", "shape", "description" as the key |
            | name | String | Output Node Name |
            | shape | String | Output Node Shape |
            | description | String | Output Node Description (optional)<br>Same specification as the input_placeholderのdescription |

     1. Create a variable name list by executing the following code in which the path of the created json file is used
        ```python
        network_struct = NetworkStruct()
        network_struct.load_struct('/Any/Struct/json/path')
        network_struct.print_vars()
        with open('vars_list.txt', 'w') as ws:
            ns.print_vars(ws=ws)
        ```

1. **Create the config file (json format) that describes the `structure information file path`, `comparison operator`, `input data conversion number`, and the `number of test data to be used`**

   | Setting Item | Key | Type | Note |
   | ---- | ---- | ----| ---- |
   | Structure Information File Path | `NameList` | String |  |
   | Comparison Operator | `CompOp` | String | `==`, `>=`, `<=`, `>`, `<`  |
   | Input Data Conversion Number | `Lap` | Number Value | Default Value: `10` |
   | Number of Test Data to be Used | `NumTest` | Number Value | Optional<br>If omitted, all data used |

   ex) [examples/mnist/configs/config_mnist.json](examples/mnist/configs/config_mnist.json)

1. **Implement Conversion Function**
    1. Implement conversion process of `input data` in `T()` function of [lib/transformation.py](lib/transformation.py)
    1. Implement conversion process of `output data` in `S()` function of [lib/transformation.py](lib/transformation.py)

### 2. Direct Execution
---
For execution as a module, execute by giving 3 parameters to the main function as follows
```python
main(sess, dataset, config_path)
```
| Parameters | Type | Description |
| --- | --- | --- |
| sess | Session | Graph Session Created by Tensorflow |
| dataset | List | Dataset Used for Test |
| conf_path | String | Config File Path used for Test |
```python
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

from lib.metamorphic_verification import main

if __name__ == '__main__':
    detaset_save_dir = 'xxxx' # Any directory
    mnist_dataset = input_data.read_data_sets(
        detaset_save_dir, one_hot=True)

    sess = tf.Session()
    # create or restore tensorflow graph session

    config_path = 'XXX.json' # Any config file path

    # dataset : List of values given each input placeholder
    main(sess, [mnist_dataset.test.images], config_path)
```

Practical Example using MNIST material: [examples/mnist/run_mnist.py](examples/mnist/run_mnist.py)

### 3. Invoking from DeepSaucer
---
Tutorial Using MNIST

Execute from DeepSaucer assuming the following directory structure
```text
Any Directory
|-- deep_saucer_core
|   |-- downloaded_data
|   |   `-- mnist_tensorflow_metamorphic (empty also OK)
|   `-- mnist
|       |-- configs
|       |   `-- config_metamorphic.json
|       |-- data
|       |   `-- dataset_metamorphic.py
|       `-- model
|           `-- model_metamorphic_check.py
`-- metamorphic_testing
    `-- lib
        |-- metamorphic_testing_setup.sh
        `-- metamorphic_verification.py
```

1. Start `DeepSaucer`
1. Selct `File` - `Add Env Setup Script`
    1. Select [lib/metamorphic_testing_setup.sh](lib/metamorphic_testing_setup.sh)
1. Select `File` - `Add Test Dataset Load Script`
   1. Select `deep_saucer_core/mnist/data/dataset_metamorphic.py`
   1. Select the `Env Setup Script` selected above
1. Select `File` - `Add Model Load Script`
   1. Select `deep_saucer_core/mnist/model/model_metamorphic.py`
   1. Select the `Env Setup Script` selected above
1. Select `File` - `Add Verification Script`
   1. Select [lib/metamorphic_verification.py](lib/metamorphic_verification.py)
   1. Select the `Env Setup Script` selected above
1. Select the 3 scripts (`Test Dataset Load`, `Model Load`, and `Verification`) selected above on DeepSaucer
   1. Select `Run` - `Run Test Function`
   1. Select `Next`
   1. Press `Select`, and then select `deep_saucer_core/mnist/configs/config_metamorphci.json`
   1. Verification starts with `Run`

### 4. Output
---
* Outputs the number of data for which the comparison result for each Lap becomes NG to the standard output and the log file

```text
---------------------
Summary (NG Count)
---------------------
Lap #0: 10
Lap #1: 18
Lap #2: 23
...
---------------------
````
* The ID of test data that the comparison result became NG at least once, and the comparison result change, are output to the log file
```text
    ID: Result
   150: [OK, OK, NG, ...]
   416: [OK, NG, NG, ...]
  2201: [NG, MG, NG, ...]
  ...
```

* When [_metamorphic_verification()](lib/metamorphic_verification.py#L200) is set to `debug=True`, the value (`x1`) of the test data before conversion, the value `T^N(x1)`of the converted test data, the value (`S(y1)`) obtained by converting the result using `x1`，and the result value (`y2`) using `T^N(x1)` are output to the log file
```text
Lap #0:
Test #1:
x1:
[0, 0.125, ...]
T^1(x1):
[0.13, 0.47, ...]
S(y1)
[3, 5, 6, ...]
y2:
[3, 1, 6, ...]

Test #2:
x1:
[0, 0.125, ...]
T^2(x1):
[0.18, 0.53, ...]

...

Lap: #1
...
```
