import sys
from pathlib import Path
import json
import shutil
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from deep_saucer.neuron_coverage.tensorflow_native.lib.coverage_verification import main_test

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
# dataset
dataset_path = args_json['inventories'][0]["value"]
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

model_path = args_json['inventories'][1]["value"]
s = tf.Session()

saver = tf.train.import_meta_graph(str(model_path) + '.meta')
saver.restore(s, str(model_path))

# run coverage verification
result_coverage_rate, result_heatmap_output, result_combination_cov_output, result_test_case_generator, result_abs_dataset_pass = \
    main_test(s, d, args_json['method_params'])

## END ########################################

# 以下結果をresultに出力する
print("result_coverage_rate", result_coverage_rate)  # json
print("result_heatmap_output", result_heatmap_output)   # pass
print("result_combination_cov_output", result_combination_cov_output)  # json
print("result_test_case_generator", result_test_case_generator)  # list
print("result_abs_dataset_pass", result_abs_dataset_pass)  # pass

if src_dir.exists():
    for src_file in src_dir.glob("*"):
        shutil.copy(src=str(src_file), dst=str(result_dir/src_file.name))

summary_json = {"result": "OK"}

# write result json
summary_json_path = result_dir/'summary.json'
with open(str(summary_json_path), 'w', encoding='utf-8') as f:
    json.dump(summary_json, f, indent=4, ensure_ascii=False)

summary_json_path = result_dir / 'coverage_rate.json'
with open(str(summary_json_path), 'w') as f:
    json.dump(result_coverage_rate, f, indent=4)

summary_json_path = result_dir / 'combination_cov_output.json'
with open(str(summary_json_path), 'w') as f:
    json.dump(result_combination_cov_output, f, indent=4)

# file copy
shutil.copyfile(result_heatmap_output, result_dir / 'heatmap.html')
shutil.copyfile(result_abs_dataset_pass, result_dir / 'output.h5')

# list
summary_list_path = result_dir / 'up_cov.csv'
with open(summary_list_path, 'wt') as f:
    for ele in result_test_case_generator:
        f.write(str(ele) + '\n')
