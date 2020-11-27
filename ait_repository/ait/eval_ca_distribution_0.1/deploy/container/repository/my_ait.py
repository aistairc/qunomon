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
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator
    requirements_generator = AITRequirementsGenerator()
    requirements_generator.add_package('pandas')
    requirements_generator.add_package('seaborn')
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -r $requirements_path ')


# In[4]:


#########################################
# area:import
# should edit
#########################################

# import if you need modules cell
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from pathlib import Path
from os import makedirs, path
import itertools
import math
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
    manifest_genenerator.set_ait_name('eval_ca_distribution')
    manifest_genenerator.set_ait_description('Evaluating distribution of dataset with expected distribution')
    manifest_genenerator.set_ait_author('AIST')
    manifest_genenerator.set_ait_email('')
    manifest_genenerator.set_ait_version('0.1')
    manifest_genenerator.set_ait_quality('https://airc.aist.go.jp/aiqm/quality/internal/Distribution_of_training_data')
    manifest_genenerator.set_ait_reference('')
    manifest_genenerator.add_ait_inventories('Data', 'dataset', 'Classification of different attributes related to autonomous driving scenarios', ['csv'], 'https://bdd-data.berkeley.edu/')
    manifest_genenerator.add_ait_parameters('attribute_no', 'int', 'Total number of attribute for distibution analysis', '6')
    manifest_genenerator.add_ait_parameters('dimension', 'int', 'Dimensions of how many attributes to combine for distibution analysis', '2')
    #manifest_genenerator.add_ait_measures('distribution', 'float', 'distribution in percentage for each combination', 'single')
    manifest_genenerator.add_ait_resources('distibution_csv', '/usr/local/qai/resources/1/', 'table', 'Table of distribution for each combination')
    manifest_genenerator.add_ait_resources('distibution_plot', '/usr/local/qai/resources/2/', 'picture', 'Plot of distribution for each combination')
    manifest_genenerator.add_ait_downloads('Log', '/usr/local/qai/downloads/1/ait.log', 'AITLog')
    manifest_path = manifest_genenerator.write()


# In[6]:


#########################################
# area:create input
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories('Data','BDD_data/BDD_labels_2036.csv')
    input_generator.set_ait_params('attribute_no','7')
    input_generator.set_ait_params('dimension','2')
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


#########################################
# area:functions
# should edit
#########################################

BOLD = '\033[1m'
END = '\033[0m'


@log(logger)
def condition_check(data,n,r):
    att_list = list(data.columns.values[1:-1])
    if n> len(att_list):
        print('ERROR: Total number of available attribute is less than total number of given attribute')
        sys.exit() 
    if n<1:
        print('ERROR: No attributes to choose from.')
        sys.exit()
    if r<1:
        print('ERROR: Dimension must be greater than 0')
        sys.exit()
    if n<r:
        print('ERROR: Number of total attributes can not be less than given dimenion.')
        sys.exit()

@log(logger)
@resources(ait_output, path_helper, 'distibution_csv')
def save_distibution_csv(result_df, file_name, file_path: str=None):
    
    makedirs(str(Path(file_path)), exist_ok=True)

    file_name = file_name.replace(' ', '')
    
    csv_path = file_path + file_name +'.csv'
    result_df.to_csv(csv_path, index = False)
    
    return csv_path

@log(logger)
@resources(ait_output, path_helper, 'distibution_plot')
def save_distibution_plot(result_df, att_name, file_path: str=None, is_single: bool=False):
    
    makedirs(str(Path(file_path)), exist_ok=True)

    file_name = att_name.replace(' ', '')
    
    if len(result_df)<60: font_size = 14
    if len(result_df)>60: font_size = 8
    fig = plt.figure(dpi=100, figsize=(25,6))
    if is_single:
        x_name='Attribute values'
    else:
        x_name='Combination name'
    result_df.plot(x = x_name, y = 'Percentage', kind = 'bar', fontsize = font_size, figsize = (25,6))
    plt.yscale('log')
    plt.xlabel(att_name)
    plt.ylabel('Distribution of data in combination')
    for index,_data in enumerate(list(result_df['Percentage'].values)): 
        if _data>1:_data=1
        if _data<0.001: continue
        plt.annotate( str(_data),(index , _data*1.1), va = 'bottom' ,ha = 'center', rotation = 90)
    fig_path = file_path +  file_name +'.jpg'
    plt.savefig(fig_path, bbox_inches="tight")
    
    return fig_path

@log(logger)
def calc_dist_single(data,n):
    att_list = list(data.columns.values[1:-1])
    att_list = att_list[0:n]
    for col_name in att_list:
        count_dict= dict(round(data[col_name].value_counts()/ int(data[col_name].count()),4))
        attr_data= {'Attribute values': list(count_dict.keys()), 'Percentage': list(count_dict.values())}
        result_df = pd.DataFrame(attr_data)
        print(BOLD+'Attribute name:'+END, col_name)
        print(BOLD+'\nResult of analysis:\n'+END, result_df)
        print('\n        ************************************       \n')
        save_distibution_csv(result_df,col_name)
        save_distibution_plot(result_df,col_name, is_single=True)
    return

@log(logger)
def calc_dist_main(data, n,r):
    att_list = list(data.columns.values[1:-1])
    att_list = att_list[0:n]  #Select how many attributes to choose from 
    att_comb = list(itertools.combinations(att_list, r)) #Create possible combination of attributes
    
    condition_check(data,n,r)
    if r==1:
        calc_dist_single(data, n)
        return
    
    ###Updating domain_dict with attribute and attribute values
    ###domain_dict will be a dictionary with attributes as keys and attribute values as values
    domain_dict = {}
    domain_dict.fromkeys(att_list)
    for i,att in enumerate(att_list):
        domain_dict[att] = data[att].unique().tolist()

    ### Updating comb_dict with combinations of attributes
    ### comb_dict is a dictionary with attribute combinations as keys, and list of list of attribute values of each attribute as value
    comb_dict = {}
    comb_dict.fromkeys(att_comb)
    for i, comb in enumerate(att_comb):
        value_list = [domain_dict[list(comb)[j]] for j in range(len(comb))]
        comb_dict[comb] = value_list

    ### Updating value_comb_dict with combinations of attribute_values
    ### value_comb_dict is a dictionary with attribute combinations as keys and list of value combinations for each attribute combination as value
    value_comb_dict = {}
    value_comb_dict.fromkeys(att_comb)
    for i, comb in enumerate(att_comb):
        value_comb_list = []
        list_of_lists = comb_dict[comb]
        for pair in itertools.product(*list_of_lists):
            value_comb_list.append(list(pair))
        value_comb_dict[comb] = value_comb_list

    for ind,comb in enumerate(att_comb):
        result_df = pd.DataFrame(columns = list(comb))   #Create a dataframe with selected attributes as column
        temp_dict = data.groupby(list(att_comb[ind])).groups   # Extract part of dataset based on attribute combination 
        file_name = (' + '.join(list(att_comb[ind]))) 
        for i,(key, values) in enumerate(temp_dict.items()):
            comb_name = []
            for col in range(len(list(comb))):
                result_df.loc[i,list(comb)[col]] = key[col]  #Log value combination in dataframe
                comb_name.append(key[col])
            result_df.loc[i,'Count'] = len(values)           #Log quanity of data per value combination
            result_df.loc[i,'Percentage'] = round(len(values)/len(data),4)
            result_df.loc[i,'Combination name'] = ('+'.join(comb_name))

        value_comb_in_data = list(temp_dict.keys())          #List of value combinations present in data
        value_comb_in_dict = value_comb_dict[att_comb[ind]]  #List of value combinations present in domain

        ### Log absent value combinations with quantity 0 in the dataframe
        for m,val in enumerate(value_comb_in_dict):
            if tuple(val) not in value_comb_in_data:
                curr_ind = len(result_df)
                comb_name = []
                for col in range(len(list(comb))): 
                    result_df.loc[curr_ind,list(comb)[col]] = val[col]
                    comb_name.append(val[col])
                result_df.loc[curr_ind,'Count'] = 0
                result_df.loc[curr_ind,'Percentage'] = 0/len(data)
                result_df.loc[curr_ind,'Combination name'] = ('+'.join(comb_name))
        
        result_df.drop(['Combination name'], axis = 1) 
        save_distibution_csv(result_df, file_name)
        save_distibution_plot(result_df, file_name)
        result_df_ = result_df.drop(['Combination name'], axis = 1) 
        print(BOLD+ 'Selected attributes for analysis:'+END, comb)
        print(BOLD+'\nResult of analysis:\n'+END, result_df_)
        print('\n        ************************************       \n')
        
    return 


# In[9]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'Log')
def move_log(file_path: str=None) -> None:
    makedirs(str(Path(file_path).parent), exist_ok=True)
    shutil.move(get_log_path(), file_path)


# In[10]:


#########################################
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:

    # インベントリを読み込み
    data = pd.read_csv(ait_input.get_inventory_path('Data'))
    total_att = ait_input.get_method_param_value('attribute_no')
    dim = ait_input.get_method_param_value('dimension')
    calc_dist_main(data, total_att, dim)
    move_log()


# In[11]:


#########################################
# area:entory point
# do not edit
#########################################
if __name__ == '__main__':
    main()


# In[12]:


#########################################
# area:license attribute set
# should edit
#########################################
ait_owner='AIST'
ait_creation_year='2020'


# In[13]:


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




