# DNN Coverage

Calculate the neuron coverage for the input dataset given by the user, and display it in the form of a heat map.
After that, a gradient for the input dataset is computed by backpropagation. Based on the gradient, the most efficient manipulation to input values
in order for the neuron coverage to increase is selected. A number of data is removed from the dataset, and
these removed data are converted to new data by the selected manipulation. Then, the new data is added to the dataset,
and the coverage is recalculated by running the model with the updated dataset. Similarly, a gradient for the updated dataset is computed.
These processes are repeated until the target coverage rate is achieved. Data manipulation algorithm is implemented by the user in Python.

## Requirement

- Python 3.6
- See [neuron_coverage_tensorflow_native.sh](neuron_coverage_tensorflow_native.sh)


## Tutorial
* There are 2 ways to use this function: importing as a module and invoking from DeepSaucer.

* When used as a module: [1. Common operation](#1-common-operation) → [2. Direct execution](#2-direct-execution) → [4. Output](#4-output)
* When invoked from DeepSaucer: [1. Common operation](#1-common-operation) → [3. Invoking from DeepSaucer](#3-invoking-from-deepsaucer) → [4. Output](#4-output)

### 1. Common Operation
1. Implement a class and its method 'get_atomic_manipulations' in [/config/implement.py](lib/config/implement.py), which manipulates a given input value

1. Create the config file
  * Set the coverage function setting information in json format ([lib/config/config.json](lib/config/config.json))

  | Setting Items | Key | Type | Setting Value |
  | ---- | ---- | ----| ---- |
  | Neuron Activity/Inactivity<br>Determination Type | `determination_on_activation` | Number Value | The default value is `0`<br> `0`: Threshold Determination<br>`1`: Upper/Lower Limit Determination<br>`2`: N Cases of Maximum Value Determination |
  | Threshold | `threshold` | Number Value | The default value is `0`<br>(Valid only for `threshold determination`)|
  | Lower Limit | `lower_bound` | Number Value | No default value<br>(Valid only for `upper/lower limit determination`) |
  | Upper Limit | `upper_bound` | Number Value | No default value<br>(Valid only for `upper/lower limit determination`) |
  | Number of Cases N | `activation_filter_no` | Number Value | The default value is `1`<br>(Valid only for `N Cases of maximum value determination`) |
  | Heat Map Generation Method Type | `heat_map_type` | Number Value | The default value is `1`<br>`0`: Generation Not Necessary<br>`1`: 0/1 Table<br>`2`: Simple Increment<br>`3`: Density Coverage<br> |
  | Combination Type | `combination_type` | Number Value | The default value is `0`<br>`0`: Implementation Not Necessary<br>`1`: Execute |
  | One Layer of Combination Coverage Target | `combination_first` | Number Value | No default value<br> (Valid and mandatory only for combination type `execution`)|
  | The Other Layer of Combination Coverage Target | `combination_second` | Number Value | No default value<br> (Valid and mandatory only for combination type `execution`)|
  | Names of tensorflow scopes in which neural networks are defined | `target_scope_name` | List of String | No default value (Mandatory) |
  | Number of data manipulated at a time | `edit_num` | Number Value | The default value is `100` |
  | Target Coverage Rate (Execution terminates when the coverage reaches Target Coverage Rate) | `target_rate` | Number Value | The default value is `1.0` |
  | Expected Coverage Growth Rate (if the coverage growth rage compared to 5 times before is less than Expected Coverage Growth Rate, unused manipulations are preferentially selected) | `increase_rate` | Number Value | The default value is `0.0` |
  | Location where manipulated data is saved | `output_file_name` | String | The default value is `output.h5` |
  | File Path of Tensorflow Model| `network_structure_path` | String | No default value (Mandatory) |
  | Number of Input Data Placeholders (in the given dataset) | `dataset_x_num` | Number Value | No default value (Mandatory) |
  | Number of Label Data Placeholders (in the given dataset) | `dataset_y_num` | Number Value | No default value (Mandatory) |
  | Number of Constant Data Placeholders (in the given dataset) | `dataset_k_num` | Number value | No default value (Mandatory) |
  | Dataset Division Start Position (Data from Start Position to End Position of the given dataset are used for coverage testing) | `split_dataset_start` | Number Value | The default value is `0` |
  | Dataset Division End Position (Data from Start Position to End Position of the given dataset are used for coverage testing) | `split_dataset_end` | Number Value | The default value is the size of the given dataset |
  | Class Name in which function 'get_atomic_manipulations' is implemented| `implement_class_name` | Number Value | No default value (Mandatory) |

### 2. Direct Execution
```python
from neuron_coverage.tensorflow_native.lib.coverage_verification import main
from pathlib import Path
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# .../neuron_coverage/tensorflow_native/lib
tf_native_dir = Path(__file__).parent.absolute()

model_path = tf_native_dir.joinpath('tutorials', 'tf_ckpt', 'model.ckpt')
s = tf.Session()

saver = tf.train.import_meta_graph(str(model_path) + '.meta')
saver.restore(s, str(model_path))

dataset_path = tf_native_dir.joinpath('tutorials', 'MNIST_data')
mnist = input_data.read_data_sets(str(dataset_path), one_hot=True)

# x: 1, y: 1, k: 1
d = [
    # x_input
    mnist.test.images,
    # y_input
    mnist.test.labels,
    # k_input
    1.0
]

c = str(tf_native_dir.joinpath('config', 'config.json'))

main(s, d, c)

```

ex ) [neuron_coverage/tensorflow_native/lib/coverage_verification.py](lib/coverage_verification.py)

### 3. Invoking from DeepSaucer

Execute from DeepSaucer assuming the following directory structure
```text
Any Directory
|-- deep_saucer_core
|   |-- downloaded_data
|   |   `-- mnist_tensorflow_neuron_coverage
|   `-- mnist
|       |-- data
|       |   `-- dataset_neuron_coverage_tensorflow_native.py
|       |-- model
|       |   `-- model_neuron_coverage_tensorflow_native.py
`-- neuron_coverage
    `-- lib
    |   `--tensorflow_native
    |      |-- examples
    |      |   |-- tf_ckpt
    |      |   |-- checkpoint
    |      |   |-- model.ckpt_name.json
    |      |   |-- model.ckpt.data-00000-of-00001
    |      |   |-- model.ckpt.index
    |      |   |-- model.ckpt.meta
```

1. Start `DeepSaucer`
1. Select `File` - `Add Env Setup Script`
    1. Select [neuron_coverage_tensorflow_native.sh](lib/neuron_coverage_tensorflow_native.sh)
1. Select`File` - `Add Test Dataset Load Script`
   1. Select `deep_saucer_core/mnist/data/dataset_neuron_coverage_tensorflow_native.py`
   1. Select the `Env Setup Script` selected above
1. Select `File` - `Add Model Load Script`
   1. Select `deep_saucer_core/mnist/model/model_neuron_coverage_tensorflow_native.py`
   1. Select the `Env Setup Script` selected above
1. Select `File` - `Add Verification Script`
   1. Select [lib/coverage_verification.py](lib/coverage_verification.py)
   1. Select the `Env Setup Script` selected above
1. Select the 3 scripts (`Test Dataset Load`, `Model Load`, and `Verification`) selected above on DeepSaucer
   1. Select `Run` - `Run Test Function`
   1. Select `Next`
   1. Press`Select` and select [lib/config/config.json](lib/config/config.json)
   1. Verification starts with `Run`

### 4. Output
1. Display coverage of the model as a whole, and coverage of each layer in the model, in the standard output.
1. Output the heat map of the coverage as an HTML file.
1. Display the combination coverage between any two layers in the standard output.
1. Display coverage increased by creating input data by manipulating the given input data, in the standard output.
1. Output the created input data by the manipulation as h5 file.
1. Output the graph with the history of the coverage rise rate, by the manipulation.
```text
Coverage rate all layer :  0.4702190170940171
Coverage rate one layer conv1:  1.0
Coverage rate one layer conv2:  0.25741390306122447
...
Multiple layers combination coverage rate 4 and 5: 0.07888650318226781
Coverage rate sum layer : 0.471532
Coverage rate sum layer : 0.471688
Coverage rate sum layer : 0.471844
...
