import os
import sys
import shutil
import glob
from pathlib import Path
import json
import yaml

# init
QAI_USER_HOME = os.environ['QAI_USER_HOME']
inventory_dir = os.path.join(QAI_USER_HOME, 'inventory/')

# check args
args_file = os.path.join(QAI_USER_HOME, 'args', 'args.json')
if os.path.exists(args_file):
    print('args_file:{}'.format(str(args_file)))
    with open(str(args_file), encoding='utf-8') as f:
        args = json.load(f)


def inventory(inventory_name):
    match = inventory_dir + inventory_name + '/**/*'
    file_paths = [p.replace('\\', '/') for p in glob.glob(match, recursive=True) if os.path.isfile(p)]
    return file_paths

def arg(arg_name):
    return args[arg_name]

def output(path):
    copy_path = os.path.join(os.environ['QAI_USER_HOME'], 'result/') + os.path.basename(path)
    shutil.copyfile(path, copy_path)

