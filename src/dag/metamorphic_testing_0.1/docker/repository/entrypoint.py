import sys
from pathlib import Path
import json
import shutil
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from deep_saucer.metamorphic_testing.lib.metamorphic_verification import main

print('Coverage test-runner')

# check args
index: int = 0
for x in sys.argv:
    print('args[{}]:{}'.format(str(index), x))
    index += 1

if len(sys.argv) != 1:
    args_file = Path(sys.argv[1])
else:
    # args_file
    args_file = Path().cwd() / 'args' / 'args.json'
print('args_file:{}'.format(str(args_file)))

# read args_file
print('{} - args_file:{}'.format(str(args_file.exists()), str(args_file)))
with open(str(args_file), encoding='utf-8') as f:
    args_json = json.load(f)

# inventory
inventory_dir = Path([m['dst_path'] for m in args_json['mounts'] if m['name'] == 'args_dir'][0])
print('inventory_dir:{}'.format(str(inventory_dir)))

# result
result_dir = Path([m['dst_path'] for m in args_json['mounts'] if m['name'] == 'result_dir'][0])
print('result_dir:{}'.format(str(result_dir)))

# 本処理：ここではダミーデータのコピーと結果出力 
src_dir = Path().cwd() / 'dummy_result_data'
print('{} - src_dir:{}'.format(str(src_dir.exists()), str(src_dir)))
print('{} - result_dir:{}'.format(str(result_dir.exists()), str(result_dir)))

## ST ########################################

detaset_save_dir = dataset_path = args_json['inventories'][0]["value"] # Any directory
mnist_dataset = input_data.read_data_sets(detaset_save_dir, one_hot=True)

sess = tf.Session()
# create or restore tensorflow graph session
model_path = args_json['inventories'][1]["value"]
saver = tf.train.import_meta_graph(str(model_path) + '.meta')
saver.restore(sess, str(model_path))

# config_path = 'XXX.json' # Any config file path

# dataset : List of values given each input placeholder
result = main(sess, [mnist_dataset.test.images], args_json['method_params'])

## END ########################################

if src_dir.exists():
    for src_file in src_dir.glob("*"):
        shutil.copy(src=str(src_file), dst=str(result_dir/src_file.name))

summary_json = {"result": "OK"}

shutil.copyfile(result, result_dir / 'result.log')