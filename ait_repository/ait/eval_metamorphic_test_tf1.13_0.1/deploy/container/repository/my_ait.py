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
    requirements_generator.add_package('bleach','1.5.0')
    requirements_generator.add_package('cycler','0.10.0')
    requirements_generator.add_package('decorator','4.1.2')
    requirements_generator.add_package('h5py','2.9.0')
    requirements_generator.add_package('html5lib','0.9999999')
    requirements_generator.add_package('Keras','2.0.8')
    requirements_generator.add_package('Markdown','2.6.9')
    requirements_generator.add_package('matplotlib','2.0.2')
    requirements_generator.add_package('networkx','1.11')
    requirements_generator.add_package('numpy','1.13.3')
    requirements_generator.add_package('olefile','0.44')
    requirements_generator.add_package('pandas','0.20.3')
    requirements_generator.add_package('Pillow','4.3.0')
    requirements_generator.add_package('protobuf','3.6.1')
    requirements_generator.add_package('pyparsing','2.2.0')
    requirements_generator.add_package('python-dateutil','2.6.1')
    requirements_generator.add_package('pytz','2017.2')
    requirements_generator.add_package('PyWavelets','0.5.2')
    requirements_generator.add_package('PyYAML','3.12')
    requirements_generator.add_package('scikit-image','0.14.2')
    requirements_generator.add_package('scikit-learn','0.19.0')
    requirements_generator.add_package('scipy','0.19.1')
    requirements_generator.add_package('six','1.11.0')
    requirements_generator.add_package('tensorflow','1.13.1')
    requirements_generator.add_package('tensorflow-tensorboard','0.1.6')
    requirements_generator.add_package('Werkzeug','0.12.2')


# In[5]:


#########################################
# area:create requirements and pip install
# do not edit
#########################################
if not is_ait_launch:
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -r $requirements_path ')


# In[6]:


#########################################
# area:import
# should edit
#########################################

# import if you need modules cell
import tensorflow as tf
import zipfile
import sys
import csv
import json
import shutil
from pathlib import Path
from os import makedirs, path
from tensorflow.examples.tutorials.mnist import input_data
from deep_saucer.metamorphic_testing.lib.metamorphic_verification import main as main_deep


# In[7]:


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


# In[8]:


#########################################
# area:create manifest
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator
    
    manifest_genenerator = AITManifestGenerator(current_dir)
    manifest_genenerator.set_ait_name('eval_metamorphic_test_tf1.13')
    manifest_genenerator.set_ait_description('''Metamorphic test.
Make sure can be classified in the same result as the original class be added a little processing to the original data.''')
    manifest_genenerator.set_ait_author('AIST')
    manifest_genenerator.set_ait_email('')
    manifest_genenerator.set_ait_version('0.1')
    manifest_genenerator.set_ait_quality('https://airc.aist.go.jp/aiqm/quality/internal/Robustness_of_trained_model')
    manifest_genenerator.set_ait_reference('')
    manifest_genenerator.add_ait_inventories(name='mnist_dataset', 
                                             type_='dataset', 
                                             description='MNIST_dataset are train image, train label, test image, test label', 
                                             format_=['zip'], 
                                             schema='http://yann.lecun.com/exdb/mnist/')
    manifest_genenerator.add_ait_inventories(name='mnist_model', 
                                             type_='model', 
                                             description='MNIST_model', 
                                             format_=['zip'], 
                                             schema='https://github.com/hitachi-rd-yokohama/deep_saucer')
    manifest_genenerator.add_ait_parameters(name='Lap', 
                                            type_='int', 
                                            description='Input Data Conversion Number', 
                                            default_val='10',
                                            min_value='1')
    manifest_genenerator.add_ait_parameters(name='NumTest', 
                                            type_='int', 
                                            description='Number of Test Data to be Used', 
                                            default_val='500',
                                            min_value='1')
    manifest_genenerator.add_ait_parameters(name='mnist_type', 
                                            type_='str', 
                                            description='train = Training_data, test = test_data, validation = validation_data', 
                                            default_val='train')
    manifest_genenerator.add_ait_measures(name='average', 
                                          type_='float', 
                                          description='Average number of NG output', 
                                          structure='single',
                                          min='0',
                                          max='1')
    manifest_genenerator.add_ait_resources(name='result', 
                                           type_='table', 
                                           description='number of NG output')
    manifest_genenerator.add_ait_downloads(name='Log', 
                                           description='AIT_log')
    manifest_genenerator.add_ait_downloads(name='DeepLog', 
                                           description='deep_saucer_log')
    manifest_path = manifest_genenerator.write()


# In[9]:


#########################################
# area:create input
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories(name='mnist_dataset',
                                        value='mnist_dataset/mnist_dataset.zip')
    input_generator.add_ait_inventories(name='mnist_model',
                                        value='mnist_model/model_mnist.zip')
    input_generator.set_ait_params(name='Lap',
                                   value='10')
    input_generator.set_ait_params(name='NumTest',
                                   value='500')
    input_generator.set_ait_params(name='mnist_type',
                                   value='train')
    input_generator.write()


# In[10]:


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


# In[11]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'average')
def ng_average(cov):
    return cov


# In[12]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@resources(ait_output, path_helper, 'result', 'result.csv')
def save_result(output_list, file_path: str=None) -> None:
    with open(file_path, 'w') as f:
        f.writelines(output_list)
        #writer = csv.writer(f)
        #writer.writerow(output_list)


# In[13]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'Log', 'ait.log')
def move_log(file_path: str=None) -> None:
    shutil.move(get_log_path(), file_path)


# In[14]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'DeepLog', 'deep.log')
def move_deep_log(log_path, file_path: str=None) -> None:
    shutil.copyfile(log_path, file_path)


# In[15]:


#########################################
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:
    
    # インベントリを読み込み
    detaset_save_dir = ait_input.get_inventory_path('mnist_dataset')
    detaset_save_parent_dir = str(Path(detaset_save_dir).parent)
    zipfile.ZipFile(detaset_save_dir).extractall(detaset_save_parent_dir)
    mnist_dataset = input_data.read_data_sets(detaset_save_parent_dir, one_hot=True)
    
    # モデルを読み込み
    model_path = ait_input.get_inventory_path('mnist_model')
    model_parent_path = str(Path(model_path).parent)
    zipfile.ZipFile(model_path).extractall(model_parent_path)
    model_path = model_parent_path + '/model_mnist.ckpt'
    model_name_list = model_parent_path + '/model_mnist.ckpt_name.json'
    
    # パラメータを読み込み
    lap_val = ait_input.get_method_param_value('Lap')
    num_test_val = ait_input.get_method_param_value('NumTest')
    # json形式のパラメータ
    args_json = {
      "NameList": model_name_list,
      "CompOp": "==",
      "Lap": lap_val,
      "NumTest": num_test_val
    }
    
    sess = tf.Session()
    saver = tf.train.import_meta_graph(model_path + '.meta')
    saver.restore(sess, str(model_path))
    
    # 実行
    mnist_type = ait_input.get_method_param_value('mnist_type')
    if mnist_type == 'train':
        result = main_deep(sess, [mnist_dataset.train.images], args_json)
    elif mnist_type == 'test':
        result = main_deep(sess, [mnist_dataset.test.images], args_json)
    elif mnist_type == 'validation':
        result = main_deep(sess, [mnist_dataset.validation.images], args_json)
    else:
        raise Exception('mnist_type error : {} is not define'.format(mnist_type))

    # 実行結果から情報をピックアップ
    ng_count = 0
    output_list = []
    with open(result) as f:
        for s_line in f:
            if 'Lap #' in s_line:
                ng_count = ng_count + int(s_line.split(': ')[1])
                output_list.append(s_line.replace(':', ','))

    cov = ng_count / (num_test_val * lap_val)
    
    output_list.append('Average number of NG output, {}'.format(cov))
    
    # resources
    save_result(output_list)
    # measures
    ng_average(cov)
    # downloads
    move_deep_log(result)
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




