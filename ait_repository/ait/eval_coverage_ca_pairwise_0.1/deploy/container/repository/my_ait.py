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


# In[ ]:


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


# In[ ]:


#########################################
# area:create requirements and pip install
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator
    requirements_generator = AITRequirementsGenerator()
    requirements_generator.add_package('pandas')
    requirements_generator.add_package(f'./{ait_sdk_name}')
    requirements_path = requirements_generator.create_requirements(current_dir)

    get_ipython().system('pip install -r $requirements_path ')


# In[ ]:


#########################################
# area:import
# should edit
#########################################

# import if you need modules cell
import pandas as pd
import csv
import math
import decimal
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
# area:create manifest
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator
    
    manifest_genenerator = AITManifestGenerator(current_dir)
    manifest_genenerator.set_ait_name('eval_coverage_ca_pairwise')
    manifest_genenerator.set_ait_description('it is calculates that Data-set has how much coverage for the combination of a given pair-wise.\n1.Find out if each pairwise row exists in the dataset\n2.A search pairwise pattern and a matching amount is output to a file.\n3.Calculate what percentage of all pairwise patterns are matched.\nBelow, restrictions\n1.The dataset must have the same columns as the pairwise combination.\n2.It is error if the required column does not exist in dataset.\n3.The dataset may have an extra column.\n4.It does not support regular expression search.\n"*" Is treated as one character "*".\n5.Pairwise and dataset may have null value.\nデータセットが特定のペアワイズの組み合わせに対してどの程度のカバレッジを持っているかを計算する。\n1.ペアワイズの各行が、データセットに存在するか検索する\n2.検索したペアワイズのパターンとマッチした件数をファイル出力する。\n3.マッチした件数が全ペアワイズパターンのうちの何パーセントか計算する。\n以下、制約事項\n1.データセットは、ペアワイズの組み合わせと同じカラムを持っている必要がある。\n2.データセットに、必要なカラムが存在しない場合はエラーになる。\n3.データセットは、余分なカラムを持っていてもよい。\n4.正規表現検索には対応しない。\n”＊”は”＊”という１文字として扱う。\n5.ペアワイズやデータセットにnullは存在してもよい。')
    manifest_genenerator.set_ait_author('AIST')
    manifest_genenerator.set_ait_email('')
    manifest_genenerator.set_ait_version('0.1')
    manifest_genenerator.set_ait_quality('https://airc.aist.go.jp/aiqm/quality/internal/Diversity_of_test_data')
    manifest_genenerator.set_ait_reference('')
    manifest_genenerator.add_ait_inventories('pairwise_list', 'dataset', 'Pairwise_list.csv', ['csv'], 'https://www.sciencedirect.com/topics/computer-science/pairwise-comparison')
    manifest_genenerator.add_ait_inventories('target', 'dataset', 'target.csv', ['csv'], 'https://www.sciencedirect.com/topics/computer-science/pairwise-comparison')
    manifest_genenerator.add_ait_measures('coverage', 'float', 'coverage of all patterns are matched', 'single')
    manifest_genenerator.add_ait_resources('matching_result', 'table', 'pairwise_matching_result')
    manifest_genenerator.add_ait_downloads('Log', 'AIT_run_log')
    manifest_path = manifest_genenerator.write()


# In[ ]:


#########################################
# area:create input
# should edit
#########################################
if not is_ait_launch:
    from ait_sdk.common.files.ait_input_generator import AITInputGenerator
    input_generator = AITInputGenerator(manifest_path)
    input_generator.add_ait_inventories('pairwise_list','pairwise_list/Pairwise_list.csv')
    input_generator.add_ait_inventories('target','target/target.csv')
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


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@measures(ait_output, 'coverage')
def coverage_measures(all_num, match_num):
    
    # 小数点３桁まで出力
    decimal.getcontext().prec = 3
    coverage = decimal.Decimal(match_num) / decimal.Decimal(all_num)
    return coverage


# In[ ]:


#########################################
# area:functions
# should edit
#########################################

@log(logger)
@resources(ait_output, path_helper, 'matching_result', 'Pairwise_list_matching_result.csv')
def save_file(output_lines, file_path: str=None):
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        for buf in output_lines:
            writer.writerow(buf)


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
# area:main
# should edit
#########################################

@log(logger)
@ait_main(ait_output, path_helper)
def main() -> None:
    # ファイルに書き込む情報をためておく
    output_lines = []
    
    # インベントリを読み込み
    pairwise_df = pd.read_csv(ait_input.get_inventory_path('pairwise_list'))
    target_df = pd.read_csv(ait_input.get_inventory_path('target'))
    
    # ヘッダ情報のファイル書き込み
    header_buf = list(pairwise_df.columns)
    header_buf.append('Amount')
    output_lines.append(header_buf)
    
    # ヘッダに半角スペースがあると、検索に使えないので、一時的に'_'へ変換しておく
    pairwise_df.columns = pairwise_df.columns.str.replace(' ', '_')
    target_df.columns = target_df.columns.str.replace(' ', '_')

    # pairwise_df全体のうち、何行マッチするかカウントする
    line_count = 0
    # pairwise_dfを１行づつ読み込み
    for p_index, pan_df in pairwise_df.iterrows():
        tmp_df = target_df
        pan_list = []
        
        # ヘッダのカラム毎に処理
        for head in pairwise_df.columns:
            pan_list.append(pan_df[head])
            # カラム毎にマッチしたものだけ上書き
            tmp_df = tmp_df[tmp_df[head] == pan_df[head]]

        # マッチした件数
        count = len(tmp_df)
        if count > 0:
            line_count = line_count + 1
            
        # マッチした件数を追記してファイル書き込み
        pan_list.append(str(count))
        output_lines.append(pan_list)

    # マッチした件数 / 全件数
    coverage = coverage_measures(len(pairwise_df), line_count)
    # ファイル書き込み
    save_file(output_lines)
    
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




