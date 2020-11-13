#!/usr/bin/env python
# coding: utf-8

# # AIT Development notebook
# 
# ## notebook of structure
# 
# |#|area name|cell num|description|edit or not|
# |---|---|---|---|---|
# |1|flags set|1|setting of launch jupyter or ait flag.|no edit|
# |2|pip install|1|Use only jupyter launch.<br>if you need install modules, write these.|should edit|
# |3|import|1|you should write use import modules.<br>but bottom lines do not edit.|should edit|
# |4|initialize|1|this cell is initialize for ait progress.|no edit|
# |5|functions|N|you defined measures, resources, downloads in ait.manifesit.json. <br>Define any functions to add these.|should edit|
# |6|main|1|Reads the data model or model and calls the function defined in `functions-area`.|should edit|
# |7|entrypoint|1|Call the main function.|no edit|
# |8|prepare deploy|1|Use only notebook launch.<br>Convert to python programs and deploy dag.py.|no edit|

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
# area:pip install
# should edit
# but first 2 row is need. do not remove.
#########################################

if not is_ait_launch:
    ait_sdk_name = 'ait_sdk-0.1.3-py3-none-any.whl'
    get_ipython().system('pip install --upgrade pip  # do not remove')
    get_ipython().system('pip install --force-reinstall ../lib/$ait_sdk_name  # do not remove')
    get_ipython().system('pip install pandas')
    get_ipython().system('pip install seaborn ')


# In[3]:


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


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'mean')
def calc_mean(iris_data, col_name):
    return iris_data.mean()[col_name]


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@resources(ait_output, path_helper, 'pairplot')
def save_pair_plot(iris_data, file_path: str=None) -> None:
    makedirs(str(Path(file_path).parent), exist_ok=True)
    sn.pairplot(iris_data, hue='variety')
    plt.savefig(file_path)


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@downloads(ait_output, path_helper, 'Log')
def move_log(file_path: str=None) -> None:
    makedirs(str(Path(file_path).parent), exist_ok=True)

    shutil.move(get_log_path(), file_path)


# In[ ]:


#########################################
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:
#     image_px_size = ait_input.get_method_param_value('image_px_size')

    # インベントリを読み込み
    iris_data = pd.read_csv(ait_input.get_inventory_path('iris_data'))
    
    calc_mean(iris_data, ait_input.get_method_param_value('mean_column_name'))
    save_pair_plot(iris_data)
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
# area:prepare deproy
# do not edit
#########################################

if not is_ait_launch:
    from ait_sdk.deploy import prepare_deploy
    current_dir = get_ipython().run_line_magic('pwd', '')
    prepare_deploy(ait_manifest, ait_sdk_name, current_dir)


# In[ ]:




