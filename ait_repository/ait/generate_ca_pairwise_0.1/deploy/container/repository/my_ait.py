#!/usr/bin/env python
# coding: utf-8

# # AIT Development notebook
# 
# ## notebook of structure
# 
# |#|area name|cell num|description|edit or not|
# |---|---|---|---|---|
# | 1|flags set|1|setting of launch jupyter or ait flag.|no edit|
# | 2|ait-sdk install|1|Use only jupyter launch.<br>find ait-sdk and install.|no edit|
# | 3|create requirements and pip install|1|Use only jupyter launch.<br>create requirements.txt.<br>And install by requirements.txt.|should edit|
# | 4|import|1|you should write use import modules.<br>but bottom lines do not edit.|should edit|
# | 5|create manifest|1|Use only jupyter launch.<br>create ait.manifest.json.|should edit|
# | 6|create input|1|Use only jupyter launch.<br>create ait.input.json.|should edit|
# | 7|initialize|1|this cell is initialize for ait progress.|no edit|
# | 8|functions|N|you defined measures, resources, downloads in ait.manifesit.json. <br>Define any functions to add these.|should edit|
# | 9|main|1|Read the data set or model and calls the function defined in `functions-area`.|should edit|
# |10|entrypoint|1|Call the main function.|no edit|
# |11|license attribute set|1|Use only notebook launch.<br>Setting attribute for license.|should edit|
# |12|prepare deploy|1|Use only notebook launch.<br>Convert to python programs and create dag.py.|no edit|

# In[ ]:


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
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator
    requirements_generator = AITRequirementsGenerator()
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -r $requirements_path ')


# In[4]:


#########################################
# area:import
# should edit
#########################################

# import if you need modules cell
import subprocess
import csv
from pathlib import Path
from os import makedirs, path

# must use modules
import shutil  # do not remove
from ait_sdk.common.files.ait_input import AITInput  # do not remove
from ait_sdk.common.files.ait_output import AITOutput  # do not remove
from ait_sdk.common.files.ait_manifest import AITManifest  # do not remove
from ait_sdk.develop.ait_path_helper import AITPathHelper  # do not remove
from ait_sdk.utils.logging import get_logger, log, get_log_path  # do not remove
from ait_sdk.develop.annotation import measures, resources, downloads, ait_main  # do not remove
# must use modules


# In[5]:


#########################################
# area:create manifest
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator
    
    manifest_genenerator = AITManifestGenerator(current_dir)
    manifest_genenerator.set_ait_name('generate_ca_pairwise')
    manifest_genenerator.set_ait_description('''
    The AIT is generate pair-wise combination for PICT.
    ''')
    manifest_genenerator.set_ait_author('AIST')
    manifest_genenerator.set_ait_email('')
    manifest_genenerator.set_ait_version('0.1')
    manifest_genenerator.set_ait_quality('https://airc.aist.go.jp/aiqm/quality/internal/Coverage_for_distinguished_problem_cases')
    manifest_genenerator.set_ait_reference('')
    manifest_genenerator.add_ait_inventories(name='pair_wise_model', 
                                             type_='dataset', 
                                             description='''
                                             Model of pair-wise.
                                             Define factors and constraints.
                                             ''', 
                                             format_=['txt'], 
                                             schema='https://github.com/Microsoft/pict/blob/master/doc/pict.md')
    manifest_genenerator.add_ait_parameters(name='order_combination', 
                                            type_='int', 
                                            description='Order of combinations.', 
                                            default_val='2')
    manifest_genenerator.add_ait_parameters(name='seed', 
                                            type_='int', 
                                            description='''
                                            Randomize generation, N - seed.
                                            if you fix seed, please set it to 1 or more.
                                            ''', 
                                            default_val='-1')
    manifest_genenerator.add_ait_resources(name='generated_paie_wise', 
                                           type_='table', 
                                           description='PICT generate pair-wise.')
    manifest_genenerator.add_ait_downloads(name='Log', 
                                           description='AIT execute log')
    manifest_path = manifest_genenerator.write()


# In[6]:


#########################################
# area:create input
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories('pair_wise_model','pair_wise_model/model.txt')
    input_generator.set_ait_params('order_combination','3')
    input_generator.set_ait_params('seed','25')
    input_generator.write()


# In[7]:


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


# In[8]:


if not is_ait_launch:
    # install pict
    get_ipython().system('apt-get update')
    get_ipython().system('apt-get -y install build-essential git')
    get_ipython().system('git clone https://github.com/microsoft/pict.git')
    get_ipython().run_line_magic('cd', 'pict')
    get_ipython().system('make')
    get_ipython().run_line_magic('cd', '..')


# In[9]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@resources(ait_output, path_helper, 'generated_paie_wise', 'pair-wise.csv')
def generated_paie_wise(model_path:str, order_combination: int, seed: int, file_path: str=None) -> None:
    
    # generate for PICT -> tsv format
    with open(file_path, 'w', encoding='utf-8') as f:
        args=[f'{current_dir}/pict/pict', model_path, f'/o:{order_combination}']
        if seed < 0:
            args.append('/r')
        else:
            args.append(f'/r:{seed}')
        subprocess.call(args=args, stdout=f)
    
    # convert tsv to csv
    with open(file_path, 'r') as fin:
        cr = csv.reader(fin, delimiter='	')
        file_contents = [line for line in cr]
    with open(file_path, 'w') as fou:
        cw = csv.writer(fou, quotechar='"', quoting=csv.QUOTE_ALL, escapechar='\\')
        cw.writerows(file_contents)


# In[10]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'Log', 'ait.log')
def move_log(file_path: str=None) -> None:

    shutil.move(get_log_path(), file_path)


# In[11]:


#########################################
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:
    
    generated_paie_wise(model_path=ait_input.get_inventory_path('pair_wise_model'),
                        order_combination=ait_input.get_method_param_value('order_combination'),
                        seed=ait_input.get_method_param_value('seed'))
    move_log()


# In[12]:


#########################################
# area:entory point
# do not edit
#########################################
if __name__ == '__main__':
    main()


# In[13]:


#########################################
# area:license attribute set
# should edit
#########################################
ait_owner='AIST'
ait_creation_year='2020'


# In[14]:


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




