import math
import numpy as np
from tensorflow.keras import models
import pickle
import json

from runnertools import runner_io

# モデル読み込み
model_path = runner_io.inventory('model_inventory_bbb').explore()[0]
model = models.load_model(model_path)

# データ読み込み
data_path = runner_io.inventory('data_inventory_aaa').explore()[0]
f = open(data_path, 'rb')
(x_train, y_train), (x_test, y_test) = pickle.load(f)
f.close()

# 推論
result_list = model.predict(x_test)

# データ計測
## 度数分布計測
sections = 25
y_max = max(max(result_list), max(y_test))
sec_width = y_max/sections
sec_typicals = []
for i in range(sections):
    typical = (i+0.5)*sec_width
    sec_typicals.append(typical)
sec_typicals = np.array(sec_typicals)
actual_freq = np.zeros(sections)
result_freq = np.zeros(sections)
def sec_index(y):
    if y==y_max:
        return (sections-1)
    index = int(y/sec_width)
    return index
for y in y_test:
    index = sec_index(y)
    actual_freq[index] += 1
for result in result_list:
    index = sec_index(result)
    result_freq[index] += 1
actual_freq /= len(y_test)
result_freq /= len(result_list)


## MSE(Mean Squared Error, 平均二乗誤差), MAE(Mean Absolute Error, 平均絶対誤差)
mse, mae = model.evaluate(x_test, y_test, verbose=0)

## カルバック・ライブラー情報量
kl_div = 0.0
for i in range(sections):
    f_i = float(result_freq[i])
    g_i = float(actual_freq[i])
    if not(f_i<=0) and not(g_i<=0):
        kl_div += f_i*math.log(f_i/g_i)

# 数値表示
print('  MSE=' + str(mse))
print('  MAE=' + str(mae))
print('  KL divergence(f,g)=' + str(kl_div))
with open('result/result.txt', 'w') as f:
    f.write('  MSE=' + str(mse))
    f.write('  MAE=' + str(mae))
    f.write('  KL divergence(f,g)=' + str(kl_div))
with open('result/result.json', 'w') as f:
    result_json = {
                    "MSE":    float(mse),
                    "MAE":    float(mae),
                    "KL_div": float(kl_div)
                }
    json.dump(result_json, f)
        

# グラフ化
import matplotlib.pyplot as plt
marker='o'
markersize=5
fillstyle="none"
graph_label = {
                'actual':     r'$f$: actual', 
                'regression': r'$g$: regression'
              }
title=r'Price Distribution (${\it Boston \ Housing \ Regression}$)'
xlabel=r'$x$ = Price [\$]'
ylabel=r'Prob($x$)'
plt.plot(sec_typicals, actual_freq, marker=marker, markersize=markersize ,fillstyle=fillstyle, label=graph_label['actual'])
plt.plot(sec_typicals, result_freq, marker=marker, markersize=markersize ,fillstyle=fillstyle, label=graph_label['regression'])
plt.title(title)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.legend()
plt.savefig('result/regression_result_distribution.png')
plt.savefig('result/regression_result_distribution.svg')
plt.savefig('result/regression_result_distribution.pdf')


# 散布図
plt.figure()
xlabel=r'Actual Price [\$]'
ylabel=r'Regressioned Price [\$]'
marker='o'
markersize=8
fillstyle="none"
g = plt.subplot()
plt.xlabel(xlabel)
plt.ylabel(ylabel)
g.set_aspect('equal')
g.scatter(y_test, result_list.T[0], marker=marker)
plt.savefig('result/scatter.png')
plt.savefig('result/scatter.svg')
plt.savefig('result/scatter.pdf')


