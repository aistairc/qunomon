import sys
from pathlib import Path
import shutil
import json
import pandas as pd
import numpy as np
from tensorflow.keras.datasets import boston_housing
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

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
(train_data, train_labels), (test_data, test_labels) = boston_housing.load_data(
    path=args_json['inventories'][0]["value"])

model = load_model(args_json['inventories'][1]["value"])

column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD',
                'TAX', 'PTRATIO', 'B', 'LSTAT']

df = pd.DataFrame(train_data, columns=column_names)

mean = train_data.mean(axis=0)
std = train_data.std(axis=0)
train_data = (train_data - mean) / std
test_data = (test_data - mean) / std

y_pred = model.predict(test_data)
test_labels = test_labels.reshape(102, 1)

# Mean Absolute Error
mae = mean_absolute_error(test_labels, y_pred)
print("MAE", mae)

# Mean Absolute Persentage Error
# 異なるスケール間の誤差を比較できる。
mape = np.mean(np.abs((y_pred - test_labels) / test_labels)) * 100
print("MAPE", mape)

# Root Mean Squared Error
# MAEに比べ誤差の影響が大きい。
rmse = np.sqrt(mean_squared_error(test_labels, y_pred))
print("RMSE", rmse)

# Root Mean Squared Persentage Error
# 誤差の影響を大きく反映し、かつ異なるスケール間の誤差を比較できる。
r2 = np.sqrt(np.mean(((y_pred - test_labels) / test_labels) ** 2)) * 100
print("R2", r2)
## END ########################################

if src_dir.exists():
    for src_file in src_dir.glob("*"):
        shutil.copy(src=str(src_file), dst=str(result_dir / src_file.name))

summary_json = {"regression_model_evaluation": {"MAE": mae, "MAPE": mape, "RMSE": rmse, "R2": r2}}

# write result json
summary_json_path = result_dir / 'summary.json'
with open(str(summary_json_path), 'w', encoding='utf-8') as f:
    json.dump(summary_json, f, indent=4, ensure_ascii=False)
