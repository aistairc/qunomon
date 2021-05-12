#!/usr/bin/env python
# coding: utf-8

# # AIT Development notebook
# 
# 
# ## notebook of structure
# 
# |#|area name|cell num|description|edit or not|
# |---|---|---|---|---|
# | 1|flags set|1|setting of launch jupyter or ait flag.|no edit|
# | 2|ait-sdk install|1|Use only jupyter launch.<br>find ait-sdk and install.|no edit|
# | 3|create requirements and pip install|3|Use only jupyter launch.<br>create requirements.txt.<br>And install by requirements.txt.|should edit(second cell, you set use modules.)|
# | 4|import|2|you should write use import modules.<br>but bottom lines do not edit.|should edit(first cell, you import your moduel.)|
# | 5|create manifest|1|Use only jupyter launch.<br>create ait.manifest.json.|should edit|
# | 6|create input|1|Use only jupyter launch.<br>create ait.input.json.|should edit|
# | 7|initialize|1|this cell is initialize for ait progress.|no edit|
# | 8|functions|N|you defined measures, resources, downloads in ait.manifesit.json. <br>Define any functions to add these.|should edit|
# | 9|main|1|Read the data set or model and calls the function defined in `functions-area`.|should edit|
# |10|entrypoint|1|Call the main function.|no edit|
# |11|license attribute set|1|Use only notebook launch.<br>Setting attribute for license.|should edit|
# |12|prepare deploy|1|Use only notebook launch.<br>Convert to python programs and create dag.py.|no edit|
# 
# ## notebook template revision history
# 
# ### 1.0.1 2020/10/21
# 
# * add revision history
# * separate `create requirements and pip install` editable and noeditable
# * separate `import` editable and noeditable
# 
# ### 1.0.0 2020/10/12
# 
# * new cerarion

# In[1]:


#########################################
# area:flags set
# do not edit
#########################################

# Determine whether to start AIT or jupyter by startup argument
import sys
is_ait_launch = (len(sys.argv) == 2)


# In[2]:


#########################################
# area:ait-sdk install
# do not edit
#########################################
if not is_ait_launch:
    # get ait-sdk file name
    from pathlib import Path
    from glob import glob
    import re

    def numericalSort(value):
        numbers = re.compile(r'(\d+)')
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts
    latest_sdk_file_path=sorted(glob('../lib/*.whl'), key=numericalSort)[-1]

    ait_sdk_name = Path(latest_sdk_file_path).name
    
    # copy to develop dir
    import shutil
    current_dir = get_ipython().run_line_magic('pwd', '')
    shutil.copyfile(f'../lib/{ait_sdk_name}', f'{current_dir}/{ait_sdk_name}')

    # install ait-sdk
    get_ipython().system('pip install --upgrade pip')
    get_ipython().system('pip install --force-reinstall ./$ait_sdk_name')


# In[3]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator
    requirements_generator = AITRequirementsGenerator()


# In[4]:


#########################################
# area:create requirements and pip install
# should edit
#########################################
if not is_ait_launch:
    requirements_generator.add_package('Cython', '0.29.21')
    requirements_generator.add_package('bleach','1.5.0')
    requirements_generator.add_package('cycler','0.10.0')
    requirements_generator.add_package('decorator','4.1.2')
    requirements_generator.add_package('h5py','2.9.0')
    requirements_generator.add_package('html5lib','0.9999999')
    requirements_generator.add_package('Keras','2.0.8')
    requirements_generator.add_package('Markdown','2.6.9')
    requirements_generator.add_package('matplotlib','2.0.2')
    requirements_generator.add_package('networkx','1.11')
    requirements_generator.add_package('numpy','1.19.2')
    requirements_generator.add_package('olefile','0.44')
    requirements_generator.add_package('pandas','0.20.3')
    requirements_generator.add_package('Pillow','4.3.0')
    requirements_generator.add_package('protobuf','3.6.1')
    requirements_generator.add_package('pyparsing','2.2.0')
    requirements_generator.add_package('python-dateutil','2.6.1')
    requirements_generator.add_package('pytz','2017.2')
    requirements_generator.add_package('PyWavelets','1.1.1')
    requirements_generator.add_package('PyYAML','3.12')
    requirements_generator.add_package('scikit-image','0.14.2')
    requirements_generator.add_package('scikit-learn','0.19.0')
    requirements_generator.add_package('scipy','0.19.1')
    requirements_generator.add_package('six','1.11.0')
    requirements_generator.add_package('tensorflow','1.13.1')
    requirements_generator.add_package('tensorflow-tensorboard','0.1.6')
    requirements_generator.add_package('Werkzeug','0.12.2')


# In[ ]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -r $requirements_path ')


# In[ ]:


#########################################
# area:import
# should edit
#########################################

# import if you need modules cell
import sys
from pathlib import Path
import json
import shutil
import tensorflow as tf
import numpy as np
from os import makedirs, path
from glob import glob
import csv
from deep_saucer.neuron_coverage.tensorflow_native.lib.coverage_verification import main_test
from ait_sdk.utils.mnist import MNIST


# In[ ]:


#########################################
# area:import
# do not edit
#########################################

# must use modules
import shutil  # do not remove
from ait_sdk.common.files.ait_input import AITInput  # do not remove
from ait_sdk.common.files.ait_output import AITOutput  # do not remove
from ait_sdk.common.files.ait_manifest import AITManifest  # do not remove
from ait_sdk.develop.ait_path_helper import AITPathHelper  # do not remove
from ait_sdk.utils.logging import get_logger, log, get_log_path  # do not remove
from ait_sdk.develop.annotation import measures, resources, downloads, ait_main  # do not remove
# must use modules


# In[ ]:


#########################################
# area:create manifest
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator
    
    manifest_genenerator = AITManifestGenerator(current_dir)
    manifest_genenerator.set_ait_name('eval_dnn_coverage_tf1.13')
    manifest_genenerator.set_ait_description('''
    Calculate the neuron coverage for the input dataset given by the user, and display it in the form of a heat map. After that, a gradient for the input dataset is computed by backpropagation. Based on the gradient, the most efficient manipulation to input values in order for the neuron coverage to increase is selected. A number of data is removed from the dataset, and these removed data are converted to new data by the selected manipulation. Then, the new data is added to the dataset, and the coverage is recalculated by running the model with the updated dataset. Similarly, a gradient for the updated dataset is computed. These processes are repeated until the target coverage rate is achieved. Data manipulation algorithm is implemented by the user in Python.
    ''')
    manifest_genenerator.set_ait_author('AIST')
    manifest_genenerator.set_ait_email('')
    manifest_genenerator.set_ait_version('0.1')
    manifest_genenerator.set_ait_quality('https://airc.aist.go.jp/aiqm/quality/internal/Robustness_of_trained_model')
    manifest_genenerator.set_ait_reference('')
    manifest_genenerator.add_ait_inventories(name='image_data', 
                                             type_='dataset', 
                                             description='MNIST image data', 
                                             format_=['gz'], 
                                             schema='http://yann.lecun.com/exdb/mnist/')
    manifest_genenerator.add_ait_inventories(name='label', 
                                             type_='dataset', 
                                             description='MNIST label data', 
                                             format_=['gz'], 
                                             schema='http://yann.lecun.com/exdb/mnist/')
    manifest_genenerator.add_ait_inventories(name='tf_ckpt', 
                                             type_='model', 
                                             description='''Tensorflow model datas.\n
                                             This is loaded by `tf.train.import_meta_graph`.''', 
                                             format_=['*'], 
                                             schema='https://github.com/tensorflow/models/tree/master/official')
    manifest_genenerator.add_ait_parameters(name='mnist_image_px_size', 
                                            type_='int', 
                                            description='''
                                            MNIST Imagge pixel size.
                                            ''', 
                                            default_val='28',
                                            min_value='28',
                                            max_value='28')
    manifest_genenerator.add_ait_parameters(name='determination_on_activation', 
                                            type_='int', 
                                            description='''
                                            Neuron Activity/Inactivity\n
                                            Determination Type\n
                                            0: Threshold Determination\n
                                            1: Upper/Lower Limit Determination\n
                                            2: N Cases of Maximum Value Determination
                                            ''', 
                                            default_val='0',
                                            min_value='0',
                                            max_value='2')
    manifest_genenerator.add_ait_parameters(name='threshold', 
                                            type_='float', 
                                            description='''
                                            Threshold\n
                                            Valid only for threshold determination
                                            ''', 
                                            default_val='0',
                                            min_value='0',
                                            max_value='1')
    manifest_genenerator.add_ait_parameters(name='lower_bound', 
                                            type_='float', 
                                            description='''
                                            Lower Limit\n
                                            No default value\n
                                            (Valid only for upper/lower limit determination)
                                            ''')
    manifest_genenerator.add_ait_parameters(name='upper_bound', 
                                            type_='float', 
                                            description='''
                                            Upper Limit\n
                                            No default value\n
                                            (Valid only for upper/lower limit determination
                                            ''')
    manifest_genenerator.add_ait_parameters(name='activation_filter_no', 
                                            type_='int', 
                                            description='''
                                            Number of Cases N\n
                                            The default value is 1\n
                                            (Valid only for N Cases of maximum value determination)
                                            ''', 
                                            default_val='1',
                                            min_value='0')
    manifest_genenerator.add_ait_parameters(name='heat_map_type', 
                                            type_='int', 
                                            description='''
                                            Heat Map Generation Method Type\n
                                            The default value is 1\n
                                            0: Generation Not Necessary\n
                                            1: 0/1 Table\n
                                            2: Simple Increment\n
                                            3: Density Coverage\n
                                            ''', 
                                            default_val='1',
                                            min_value='0',
                                            max_value='3')
    manifest_genenerator.add_ait_parameters(name='combination_type', 
                                            type_='int', 
                                            description='''
                                            Combination Type\n
                                            The default value is 0\n
                                            0: Implementation Not Necessary\n
                                            1: Execute
                                            ''', 
                                            default_val='0',
                                            min_value='0',
                                            max_value='1')
    manifest_genenerator.add_ait_parameters(name='combination_first', 
                                            type_='int', 
                                            description='''
                                            One Layer of Combination Coverage Target\n
                                            No default value\n
                                            (Valid and mandatory only for combination type execution)
                                            ''')
    manifest_genenerator.add_ait_parameters(name='combination_second', 
                                            type_='int', 
                                            description='''
                                            The Other Layer of Combination Coverage Target\n
                                            No default value\n
                                            (Valid and mandatory only for combination type execution)
                                            ''')
    manifest_genenerator.add_ait_parameters(name='target_scope_name', 
                                            type_='list[str]', 
                                            description='''
                                            Names of tensorflow scopes in which neural networks are defined\n
                                            No default value (Mandatory)\n
                                            List items are separate by ",".
                                            ''')
    manifest_genenerator.add_ait_parameters(name='edit_num', 
                                            type_='int', 
                                            description='''
                                            Number of data manipulated at a time\n
                                            The default value is 100
                                            ''', 
                                            default_val='100',
                                            min_value='1')
    manifest_genenerator.add_ait_parameters(name='target_rate', 
                                            type_='float', 
                                            description='''
                                            Target Coverage Rate (Execution terminates when the coverage reaches Target Coverage Rate)\n
                                            The default value is 1.0
                                            ''', 
                                            default_val='1.0',
                                            min_value='0',
                                            max_value='1.0')
    manifest_genenerator.add_ait_parameters(name='increase_rate', 
                                            type_='float', 
                                            description='''
                                            Expected Coverage Growth Rate (if the coverage growth rage compared to 5 times before is less than Expected Coverage Growth Rate, unused manipulations are preferentially selected)\n
                                            The default value is 0.0
                                            ''', 
                                            default_val='0',
                                            max_value='0')
    manifest_genenerator.add_ait_parameters(name='dataset_x_num', 
                                            type_='int', 
                                            description='''
                                            Number of Input Data Placeholders (in the given dataset)\n
                                            No default value (Mandatory)
                                            ''',
                                            min_value='1')
    manifest_genenerator.add_ait_parameters(name='dataset_y_num', 
                                            type_='int', 
                                            description='''
                                            Number of Label Data Placeholders (in the given dataset)\n
                                            No default value (Mandatory)
                                            ''',
                                            min_value='1')
    manifest_genenerator.add_ait_parameters(name='dataset_k_num', 
                                            type_='int', 
                                            description='''
                                            Number of Constant Data Placeholders (in the given dataset)\n
                                            No default value (Mandatory)
                                            ''',
                                            min_value='1')
    manifest_genenerator.add_ait_parameters(name='split_dataset_start', 
                                            type_='int', 
                                            description='''
                                            Dataset Division Start Position (Data from Start Position to End Position of the given dataset are used for coverage testing)\n
                                            The default value is 0
                                            ''', 
                                            default_val='0',
                                            min_value='0')
    manifest_genenerator.add_ait_parameters(name='split_dataset_end', 
                                            type_='int', 
                                            description='''
                                            Dataset Division End Position (Data from Start Position to End Position of the given dataset are used for coverage testing)\n
                                            The default value is the size of the given dataset
                                            ''', 
                                            default_val='100',
                                            min_value='1')
    manifest_genenerator.add_ait_parameters(name='implement_class_name', 
                                            type_='str', 
                                            description='''
                                            Class Name in which function 'get_atomic_manipulations' is implemented\n
                                            No default value (Mandatory)
                                            ''')
    manifest_genenerator.add_ait_measures(name='coverage_rate_all_layer', 
                                          type_='float', 
                                          description='coverage of the model as a whole.', 
                                          structure='single',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='coverage_rate_each_layer', 
                                          type_='float', 
                                          description='coverage of each layer in the model.', 
                                          structure='sequence',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_measures(name='coverage_rate_combination', 
                                          type_='float', 
                                          description='coverage of select combination.', 
                                          structure='single',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_resources(name='test_case_generator',  
                                           type_='table', 
                                           description='generate coverage increase data.')
    manifest_genenerator.add_ait_downloads(name='heatmap', 
                                           description='the heat map of the coverage as an HTML file.')
    manifest_genenerator.add_ait_downloads(name='abs_dataset', 
                                           description='the created input data by the manipulation as h5 file.')
    manifest_genenerator.add_ait_downloads(name='Log', 
                                           description='AITLog')
    manifest_path = manifest_genenerator.write()


# In[ ]:


#########################################
# area:create input
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories(name='image_data',
                                        value='MNIST_data/image/train-images-idx3-ubyte.gz')
    input_generator.add_ait_inventories(name='label',
                                        value='MNIST_data/label/train-labels-idx1-ubyte.gz')
    input_generator.add_ait_inventories(name='tf_ckpt',
                                        value='tf_ckpt')
    input_generator.set_ait_params(name='mnist_image_px_size',
                                   value='28')
    input_generator.set_ait_params(name='determination_on_activation',
                                   value='0')
    input_generator.set_ait_params(name='threshold',
                                   value='0.5')
    input_generator.set_ait_params(name='lower_bound',
                                   value='0.5')
    input_generator.set_ait_params(name='upper_bound',
                                   value='1')
    input_generator.set_ait_params(name='activation_filter_no',
                                   value='10')
    input_generator.set_ait_params(name='heat_map_type',
                                   value='1')
    input_generator.set_ait_params(name='combination_type',
                                   value='1')
    input_generator.set_ait_params(name='combination_first',
                                   value='4')
    input_generator.set_ait_params(name='combination_second',
                                   value='5')
    input_generator.set_ait_params(name='target_scope_name',
                                   value='conv1,conv2,conv3,conv4,conv5,conv6,fc1')
    input_generator.set_ait_params(name='edit_num',
                                   value='10')
    input_generator.set_ait_params(name='target_rate',
                                   value='1.0')
    input_generator.set_ait_params(name='increase_rate',
                                   value='0.0')
    input_generator.set_ait_params(name='dataset_x_num',
                                   value='1')
    input_generator.set_ait_params(name='dataset_y_num',
                                   value='1')
    input_generator.set_ait_params(name='dataset_k_num',
                                   value='1')
    input_generator.set_ait_params(name='split_dataset_start',
                                   value='0')
    input_generator.set_ait_params(name='split_dataset_end',
                                   value='100')
    input_generator.set_ait_params(name='implement_class_name',
                                   value='Tutorial')
    input_generator.write()


# In[ ]:


#########################################
# area:initialize
# do not edit
#########################################

logger = get_logger()

ait_manifest = AITManifest()
ait_input = AITInput(ait_manifest)
ait_output = AITOutput(ait_manifest)

if is_ait_launch:
    # launch from AIT
    current_dir = path.dirname(path.abspath(__file__))
    path_helper = AITPathHelper(argv=sys.argv, ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)
else:
    # launch from jupyter notebook
    # ait.input.json make in input_dir
    input_dir = '/usr/local/qai/mnt/ip/job_args/1/1'
    current_dir = get_ipython().run_line_magic('pwd', '')
    path_helper = AITPathHelper(argv=['', input_dir], ait_input=ait_input, ait_manifest=ait_manifest, entry_point_dir=current_dir)

ait_input.read_json(path_helper.get_input_file_path())
ait_manifest.read_json(path_helper.get_manifest_file_path())

### do not edit cell


# In[ ]:


def get_value_list(list_dict):
    return [float(list(l.values())[0]) for l in list_dict]

def add_config_json(name, ait_input, config_json) -> None:
    value = ait_input.get_method_param_value(name)
    config_json[name] = value

def create_config_json(ait_input):
    config_json = {}

    add_config_json('determination_on_activation', ait_input, config_json)
    add_config_json('threshold', ait_input, config_json)
    add_config_json('lower_bound', ait_input, config_json)
    add_config_json('upper_bound', ait_input, config_json)
    add_config_json('heat_map_type', ait_input, config_json)
    add_config_json('activation_filter_no', ait_input, config_json)
    add_config_json('combination_type', ait_input, config_json)
    add_config_json('combination_first', ait_input, config_json)
    add_config_json('combination_second', ait_input, config_json)
    add_config_json('target_scope_name', ait_input, config_json)
    add_config_json('edit_num', ait_input, config_json)
    add_config_json('target_rate', ait_input, config_json)
    add_config_json('increase_rate', ait_input, config_json)
    config_json['output_file_name'] = 'examples/output.h5'
    config_json['network_structure_path'] = 'examples/tf_ckpt/model.ckpt_name.json'
    add_config_json('dataset_x_num', ait_input, config_json)
    add_config_json('dataset_y_num', ait_input, config_json)
    add_config_json('dataset_k_num', ait_input, config_json)
    add_config_json('split_dataset_start', ait_input, config_json)
    add_config_json('split_dataset_end', ait_input, config_json)
    add_config_json('implement_class_name', ait_input, config_json)
    
    return config_json


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'coverage_rate_all_layer')
def calc_coverage_rate_all_layer(coverage_rate):
    return np.mean(get_value_list(coverage_rate))


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'coverage_rate_each_layer', is_many=True)
def calc_coverage_rate_each_layer(coverage_rate):
    return get_value_list(coverage_rate)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'coverage_rate_combination')
def calc_coverage_rate_combination(combination_cov):
    return list(combination_cov.values())[0]


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'heatmap', 'heatmap.html')
def save_heatmap(result_heatmap_output, file_path: str=None) -> None:
    shutil.copyfile(result_heatmap_output, file_path)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@resources(ait_output, path_helper, 'test_case_generator', 'test_case_generator.csv')
def save_test_case_generator(result_test_case_generator, file_path: str=None) -> None:
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(result_test_case_generator)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'Log', 'ait.log')
def move_log(file_path: str=None) -> None:
    shutil.move(get_log_path(), file_path)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'abs_dataset', 'output.h5')
def save_abs_dataset(result_abs_dataset_pass, file_path: str=None) -> None:
    shutil.copyfile(result_abs_dataset_pass, file_path)


# In[ ]:


#########################################
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:

    image_px_size = ait_input.get_method_param_value('mnist_image_px_size')
    
    mnist = MNIST()
    X_test = mnist.load_image(ait_input.get_inventory_path('image_data'), image_px_size)
    y_test = mnist.load_label(ait_input.get_inventory_path('label'))
    
    # reshape for dnn coverage
    X_test = X_test.reshape([X_test.shape[0], image_px_size*image_px_size])
    
    # onehot for dnn coverage
    class_num = len(np.unique(y_test))
    y_test = np.identity(class_num)[y_test]
    
    data_set = [
        # x_input
        X_test,
        # y_input
        y_test,
        # k_input
        1.0
    ]
    
    session = tf.Session()

    tf_ckpt_path = ait_input.get_inventory_path('tf_ckpt')
    model_meta_path = glob(f'{tf_ckpt_path}/*.meta')[0]
    model_path = '{}/{}'.format(tf_ckpt_path, str(Path(model_meta_path).stem))
    
    saver = tf.train.import_meta_graph(model_meta_path)
    saver.restore(session, str(model_path))

    conf_json = create_config_json(ait_input)
    
    # run coverage verification
    result_coverage_rate, result_heatmap_output, result_combination_cov_output, result_test_case_generator, result_abs_dataset_pass =         main_test(session, data_set, conf_json)
    
    calc_coverage_rate_all_layer(result_coverage_rate)
    calc_coverage_rate_each_layer(result_coverage_rate)
    calc_coverage_rate_combination(result_combination_cov_output)
    
    save_test_case_generator(result_test_case_generator)
    
    save_heatmap(result_heatmap_output)
    save_abs_dataset(result_abs_dataset_pass)
    move_log()


# In[ ]:


#########################################
# area:entory point
# do not edit
#########################################
if __name__ == '__main__':
    main()


# In[ ]:


#########################################
# area:license attribute set
# should edit
#########################################
ait_owner='AIST'
ait_creation_year='2020'


# In[ ]:


#########################################
# area:prepare deproy
# do not edit
#########################################

if not is_ait_launch:
    from ait_sdk.deploy import prepare_deploy
    from ait_sdk.license.license_generator import LicenseGenerator
    
    current_dir = get_ipython().run_line_magic('pwd', '')
    prepare_deploy(ait_manifest, ait_sdk_name, current_dir, requirements_path, is_remote_deploy=True)
    
    # output License.txt
    license_generator = LicenseGenerator()
    license_generator.write('../top_dir/LICENSE.txt', ait_creation_year, ait_owner)


# In[ ]:




