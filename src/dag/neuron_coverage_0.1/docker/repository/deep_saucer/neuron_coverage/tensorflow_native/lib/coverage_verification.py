# -*- coding: utf-8 -*-
#******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
#******************************************************************************************
import sys
from pathlib import Path
_proj_dir = Path(__file__).absolute().parent.parent
_lib_dir = Path(_proj_dir, 'lib')

sys.path.append(str(_proj_dir))
sys.path.append(str(_lib_dir))

from preprocess import get_json
from structutil import NetworkStruct
from function import CoverageFunction


def main_test(model, dataset=None, conf_path=None):
    """
    DNN Coverage (tensorflow native)
    :param model: tensorflow graph session
    :param dataset:
    :param conf_path:
    :return:
    """
    from pathlib import Path
    # Get Config
    determination_on_activation_kw, activation_value_add_neuron_kw, json_data = get_json(conf_path)

    # Network Structure Path
    name_list_path = str(Path(__file__).parent.joinpath(json_data["network_structure_path"]).absolute())

    # Dataset nums
    x_num = json_data["dataset_x_num"]
    y_num = json_data["dataset_y_num"]
    k_num = json_data["dataset_k_num"]

    # Load Network Structure
    network_structure = NetworkStruct()
    ret = network_structure.load_struct(name_list_path)
    if not ret:
        return

    # Set info by graph session
    network_structure.set_info_by_session(model)

    # Get Input Placeholders
    input_placeholders = list(
        [model.graph.get_tensor_by_name(name)
         for name in network_structure.in_raw_names]
    )

    # feed_dict
    feed_dict = {}
    for input_placeholder, value in zip(input_placeholders, dataset):
        feed_dict[input_placeholder] = value

    # Split dataset, placeholder
    d_split_start = json_data["split_dataset_start"]
    d_split_end = json_data["split_dataset_end"]
    start = 0
    end = 0

    if x_num > 0 and len(dataset) >= end + x_num:
        end = x_num
        x_placeholders = input_placeholders[start:end]
        x_input = dataset[start:end]
        x_input = [_[d_split_start:d_split_end] for _ in x_input]
        start += x_num

    if y_num > 0 and len(dataset) >= end + y_num:
        end += y_num
        y_placeholders = input_placeholders[start:end]
        y_input = dataset[start:end]
        y_input = [_[d_split_start:d_split_end] for _ in y_input]
        start += y_num

    if k_num > 0 and len(dataset) >= end + k_num:
        end += k_num
        k_placeholders = input_placeholders[start:end]
        k_input = dataset[start:end]
    else:
        k_placeholders = None
        k_input = None

    del dataset

    feed_dict_xk = {}
    for key, val in zip(x_placeholders, x_input):
        feed_dict_xk[key] = val
    if k_num > 0:
        for key, val in zip(k_placeholders, k_input):
            feed_dict_xk[key] = val

    # Get Instance of CoverageFunction
    fc = CoverageFunction(model, feed_dict_xk, determination_on_activation_kw,
                          activation_value_add_neuron_kw, json_data)

    # MOD Function Args
    # 1, Output coverage ratio
    result_coverage_rate = fc.coverage_rate_output()

    # MOD Function Args
    # 2, Output heat map
    if json_data["heat_map_type"] != 0:
        result_heatmap_output = fc.coverage_heatmap_output()

    # MOD Function Args
    # 3, Output combination coverage
    result_combination_cov_output = None
    if json_data["combination_type"] == 1:
        result_combination_cov_output = fc.combination_cov_output(json_data["combination_first"], json_data["combination_second"])

    # MOD Function Args
    # Dynamic instance creation
    # 4, Generate coverage increase data
    result_test_case_generator, result_abs_dataset_pass = fc.test_case_generator(x_placeholders, y_placeholders, k_placeholders, x_input, y_input, k_input)

    return result_coverage_rate, result_heatmap_output, result_combination_cov_output, result_test_case_generator, result_abs_dataset_pass


if __name__ == '__main__':
    """
    Tutorial (MNIST)
    """
    from pathlib import Path
    import tensorflow as tf
    from tensorflow.examples.tutorials.mnist import input_data

    # neuron_coverage/tensorflow_native
    tf_native_dir = Path(__file__).parent.absolute()

    # Load Session
    # neuron_coverage/tensorflow_native/tutorials/tf_ckpt/model.ckpt
    model_path = tf_native_dir.joinpath(
        'examples', 'tf_ckpt', 'model.ckpt')
    s = tf.Session()
    # neuron_coverage/tensorflow_native/tutorials/tf_ckpt/model.ckpt.meta
    saver = tf.train.import_meta_graph(str(model_path) + '.meta')
    saver.restore(s, str(model_path))

    # dataset
    # neuron_coverage/tensorflow_native/tutorials/MNIST_data
    dataset_path = tf_native_dir.joinpath('examples', 'MNIST_data')
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

    # config file
    # neuron_coverage/tensorflow_native/lib/config/config.json
    c = str(tf_native_dir.joinpath('config', 'config.json'))

    # run coverage verification
    main(s, d, c)
