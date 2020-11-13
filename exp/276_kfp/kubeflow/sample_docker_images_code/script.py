from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import sys
import gzip
import numpy as np


def mnist_load(h_dir):
    print("START：mnist_load")
    key_file = {
        'train_img': h_dir[2],
        'train_label': h_dir[3],
        'test_img': h_dir[4],
        'test_label': h_dir[5]
    }

    file_path = h_dir[1] + '/' + key_file['train_img']
    with gzip.open(file_path, 'rb') as f:
        train_img = np.frombuffer(f.read(), np.uint8, offset=16)
    train_img = train_img.reshape(-1, 28, 28)

    file_path = h_dir[1] + '/' + key_file['train_label']
    with gzip.open(file_path, 'rb') as f:
        train_label = np.frombuffer(f.read(), np.uint8, offset=8)

    file_path = h_dir[1] + '/' + key_file['test_img']
    with gzip.open(file_path, 'rb') as f:
        test_img = np.frombuffer(f.read(), np.uint8, offset=16)
    test_img = test_img.reshape(-1, 28, 28)

    file_path = h_dir[1] + '/' + key_file['test_label']
    with gzip.open(file_path, 'rb') as f:
        test_label = np.frombuffer(f.read(), np.uint8, offset=8)

    dataset = {}
    dataset['train_img'] = train_img
    dataset['train_label'] = train_label
    dataset['test_img'] = test_img
    dataset['test_label'] = test_label
    print("END：mnist_load")
    return train_img, train_label, test_img, test_label


def ml(h_args):
    print("START：main")
    x_train, y_train, x_test, y_test = mnist_load(h_args)
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=5)

    model.evaluate(x_test, y_test, verbose=2)
    print("END：main")
    return model


if __name__ == '__main__':
    args = sys.argv

    # TODO dockerの環境変数から値を取得お願いします　to 岩瀬さん

    # 機械学習モジュールの実行テスト
    model = ml(args)

    # 機械学習モデルの保存テスト＝マウントしたボリュームに保存した時の挙動確認
    model.save(args[1])

    # コマンドライン引数のチェック
    print("第1引数：" + args[1])
    print("第2引数：" + args[2])
    print("第3引数：" + args[3])
    print("第4引数：" + args[4])
    print("第5引数：" + args[5])
    print("END")

