import tensorflow as tf
from tensorflow import keras
import pandas as pd

boston_housing = keras.datasets.boston_housing
(train_data, train_labels), (test_data, test_labels) = boston_housing.load_data(path=r'C:\Users\AIQM-07\Documents\qai-testbed\src\dag\regression_model_evaluation_0.1\docker\repository\workdir\inventory\dataset\boston_housing.npz')

column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD',
                'TAX', 'PTRATIO', 'B', 'LSTAT']

df = pd.DataFrame(train_data, columns=column_names)

mean = train_data.mean(axis=0)
std = train_data.std(axis=0)
train_data = (train_data - mean) / std
test_data = (test_data - mean) / std


def build_model():
    model = keras.Sequential([
        keras.layers.Dense(64, activation=tf.nn.relu,
                           input_shape=(train_data.shape[1],)),
        keras.layers.Dense(64, activation=tf.nn.relu),
        keras.layers.Dense(1)
    ])

    optimizer = tf.compat.v1.train.RMSPropOptimizer(0.001)

    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae'])
    return model


model = build_model()
model.summary()
EPOCHS = 500

# Store training stats
history = model.fit(train_data, train_labels, epochs=EPOCHS,
                    validation_split=0.2, verbose=1)

y_pred = model.predict(test_data)
test_labels = test_labels.reshape(102, 1)

# Mean Absolute Error
from sklearn.metrics import mean_absolute_error
print("MAE", mean_absolute_error(test_labels, y_pred))

# Mean Absolute Persentage Error
# 異なるスケール間の誤差を比較できる。
import numpy as np
print("MAPE", np.mean(np.abs((y_pred - test_labels) / test_labels)) * 100)

# Root Mean Squared Error
# MAEに比べ誤差の影響が大きい。
import numpy as np
from sklearn.metrics import mean_squared_error
print("RMSE", np.sqrt(mean_squared_error(test_labels, y_pred)))

# Root Mean Squared Persentage Error
# 誤差の影響を大きく反映し、かつ異なるスケール間の誤差を比較できる。
import numpy as np
print("R2", np.sqrt(np.mean(((y_pred - test_labels) / test_labels)**2))*100)

model_json = model.to_json()
open('./repository/workdir/inventory/tf_model/model.json', 'w').write(model_json)
model.save('./model.h5')
