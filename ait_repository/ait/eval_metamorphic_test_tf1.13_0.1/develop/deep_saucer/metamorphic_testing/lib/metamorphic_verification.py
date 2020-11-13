# -*- coding: utf-8 -*-
#******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
#******************************************************************************************
import os
import random
import sys
import json
from pprint import pprint

import numpy as np

from pathlib import Path
from datetime import datetime

_root_dir = Path(__file__).absolute().parent.parent
_metamorphic_lib = Path(_root_dir).joinpath('lib')

sys.path.append(str(_root_dir))
sys.path.append(str(_metamorphic_lib))


# Function to transform input
from transformation import T

# Function to transform output
from transformation import S

from utils.structutil import NetworkStruct

_current = Path(os.getcwd()).absolute()

_max_precision = 38

_op_map = {
    '==': lambda a, b: a == b,
    '<=': lambda a, b: a <= b,
    '>=': lambda a, b: a >= b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
}

_msg_map = {
    True: 'OK',
    False: 'NG'
}

NAME_LIST = 'NameList'
COMP_OP = 'CompOp'
LAP = 'Lap'
DECIMALS = 'Decimals'
NUM_TEST = 'NumTest'

_required_conf_keys = [NAME_LIST, COMP_OP, LAP]
_conf_keys = [NAME_LIST, COMP_OP, LAP, DECIMALS, NUM_TEST]

_conf_map = {
    NAME_LIST: lambda a: a[NAME_LIST],
    COMP_OP: lambda a: a[COMP_OP],
    LAP: lambda a: a[LAP],
    DECIMALS: lambda a: a[DECIMALS] if DECIMALS in a else None,
    NUM_TEST: lambda a: a[NUM_TEST] if NUM_TEST in a else None
}


def _hasattr_iter(o):
    return hasattr(o, '__iter__')


def _comp(t_o_y1, y2, comp_op, decimal=None):
    for i, (r1, r2) in enumerate(zip(t_o_y1, y2)):

        # round to even
        v1 = np.round(r1, decimals=decimal) if decimal else r1
        v2 = np.round(r2, decimals=decimal) if decimal else r2

        yield np.all(_op_map[comp_op](v1, v2))


def _check_conf_json_keys(j_data):
    for conf_key in _required_conf_keys:
        if conf_key not in j_data:
            print('Config JSON not defined "{}"'.format(conf_key),
                  file=sys.stderr)
            return False

    return True


def _set_log_path():
    _log_dir = _current.joinpath('logfile')
    if not _log_dir.exists():
        _log_dir.mkdir(parents=True)

    return _log_dir.joinpath('log_{0}.txt'.format(
        datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))


def _get_conf_vals(j_data):
    for conf_key in _conf_keys:
        yield _conf_map[conf_key](j_data)


def _choice_dataset(dataset, input_var_placeholders, sample_num, num_test):
    random.seed(1)
    sample_index = random.sample(range(num_test), k=sample_num)

    test_dataset = []
    for i in range(len(dataset)):
        test_dataset.append([])
        for j in sample_index:
            if _hasattr_iter(dataset[i]):
                test_dataset[i].append(dataset[i][j].tolist())
            else:
                test_dataset[i] = dataset[i]

        if _hasattr_iter(test_dataset[i]):
            test_dataset[i] = np.array(
                test_dataset[i],
                dtype=input_var_placeholders[i].dtype.as_numpy_dtype)

    return test_dataset, sample_index


def _check_shape(dataset, input_var_placeholders):
    for val, p, in zip(dataset, input_var_placeholders):
        if _hasattr_iter(val):
            if val.shape[1] != p.shape[1].value:
                print('{0} shape is {1}, data shape is {2}'.format(
                    p.name, p.shape, val.shape), file=sys.stderr)
                return False

    return True


def main(model, dataset=None, config_path=None):
    """

    :param model: Tensorflow graph session
    :param dataset: List of values given each input placeholder
    :param config_path:
    :return:
    """
    log_file = _set_log_path()

    num_test = max([d.shape[0] for d in dataset if _hasattr_iter(d)])

    # Load Config
    # conf_dir = Path(config_path).parent.absolute()
    # with open(config_path) as fs:
    #     j_data = json.load(fs)
    #
    # if not _check_conf_json_keys(j_data):
    #     return
    j_data = config_path
    name_list_path, comp_op, lap, decimals, sample_num = _get_conf_vals(j_data)
    if not os.path.isabs(name_list_path):
        # name_list_path = str(conf_dir.joinpath(name_list_path).resolve())
        name_list_path = str(name_list_path)

    if not os.path.exists(name_list_path):
        print('[Error]: "{}" is not found'.format(name_list_path),
              file=sys.stderr)
        return

    if comp_op not in _op_map.keys():
        print('Operators that can be used are {0}'.format(
                list(_op_map.keys())), file=sys.stderr)
        return

    if decimals == 0:
        decimals = None

    if sample_num is None or sample_num > num_test:
        sample_num = num_test

    # Load DNN Structure
    network_struct = NetworkStruct()
    ret = network_struct.load_struct(name_list_path)
    if not ret:
        return

    network_struct.set_info_by_session(model)

    # ----- Testing -----
    # Accumulator for Kappa Accuracy for imbalanced data
    input_var_placeholders = []
    for name in network_struct.in_raw_names:
        input_var_placeholders.append(model.graph.get_tensor_by_name(name))

    if sample_num != num_test:
        # choice dataset random
        dataset, choice_indexes = _choice_dataset(
            dataset, input_var_placeholders, sample_num, num_test)
    else:
        choice_indexes = range(len(dataset))

    # check shape
    if not _check_shape(dataset, input_var_placeholders):
        return

    model_output = model.graph.get_tensor_by_name(network_struct.out_raw_name)

    ng_count, result_list = _metamorphic_verification(
        model, dataset, input_var_placeholders, model_output,
        lap, decimals, comp_op, log_file, debug=False)

    # Write Log
    i_format = '{0:%dd}' % len(str(num_test))
    with open(log_file, 'a') as ws:
        print('{0}: Result'.format('ID'.rjust(len(str(num_test)))), file=ws)
        for index, r in sorted(zip(choice_indexes, result_list)):
            if False in r:
                print('{0}: {1}'.format(
                    i_format.format(index),
                    str([_msg_map[v] for v in r]).replace("'", '')), file=ws)

        _print_summary(ng_count, ws)

    print('Log File: {}'.format(str(log_file)))
    return str(log_file)

def _metamorphic_verification(model, dataset, input_var_placeholders,
                              model_output, lap, decimals, comp_op, log_file,
                              debug=False):
    # base predict
    base_dataset, base_pred, _ = _predict(
        model, dataset, input_var_placeholders, model_output)

    # transform base predict
    transform_pred = S(base_pred)

    test_data = dataset.copy()

    ng_count = []
    result_list = []

    print('---------------------')
    print('Summary (NG Count)')
    print('---------------------')

    with open(log_file, 'w') as ws:
        for i in range(lap):
            # Transform dataset and Predict
            transform_dataset, prediction, test_data = _predict(
                model, test_data, input_var_placeholders, model_output, T)

            # check predict
            # Comparison
            result = list(_comp(transform_pred, prediction, comp_op, decimals))

            print('Lap #{0}: {1}'.format(i, result.count(False)))
            result_list.append(result)
            ng_count.append(result.count(False))

            if debug:
                _debug_log(i, base_dataset, transform_dataset, transform_pred,
                           prediction, decimals, comp_op, ws)
        print('---------------------')

    return ng_count,  list(zip(*result_list))


def _print_summary(ng_count, ws):
    print('---------------------', file=ws)
    print('Summary (NG Count)', file=ws)
    print('---------------------', file=ws)
    for i, v in enumerate(ng_count):
        print('Lap #{0}: {1}'.format(i, v), file=ws)
    print('---------------------', file=ws)


def _debug_log(i, base_dataset, transform_dataset, transform_pred, prediction,
               decimals, comp_op, ws):

    _write_log(ws, 'Lap #{} :'.format(i))
    for j, (x1, t_i_x1, t_o_y1, y2) in enumerate(
            zip(base_dataset, transform_dataset, transform_pred,
                prediction)):

        # if not all(list(_comp([t_o_y1], [y2], comp_op, decimals))):
        #     _debug_mnist(x1, t_i_x1)

        _write_log(ws, 'Test #{} :'.format(j + 1))
        _write_log(ws, 'x1 :')
        _write_log(ws, x1, pp=True)
        _write_log(ws, 'T^{}(x1) :'.format(i + 1))
        _write_log(ws, t_i_x1, pp=True)

        # round to even
        _write_log(ws, 'S(y1) :')
        _write_log(ws, t_o_y1, pp=True)
        if decimals:
            _write_log(ws,
                       'S(y1) (Round[decimals={}]):'.format(decimals))
            _write_log(ws, t_o_y1, decimals, pp=True)

        _write_log(ws, 'y2 :')
        _write_log(ws, y2, pp=True)
        if decimals:
            _write_log(ws, 'y2 (Round[decimals={}]):'.format(decimals))
            _write_log(ws, y2, decimals, pp=True)

        _write_log(ws, '')


def _write_log(ws, val, decimals=None, pp=False):

    np.set_printoptions(precision=_max_precision)
    if decimals:
        np.set_printoptions(precision=decimals)
        val = np.round(val, decimals)

    if pp:
        pprint(val, stream=ws)
    else:
        print(val, file=ws)

    np.set_printoptions(precision=_max_precision)


def _predict(sess, dataset, in_placeholders, target_layer, f=None):
    """

    :param sess: graph session
    :param dataset: Test data list for each input_placeholders
    :param in_placeholders:
    :param target_layer:
    :param f: Data Transform function
    :return transform_dataset: Transform data list for each Test
    :return prediction_output: Prediction list for each Test
    :return next_test_data: Transform data list for each input_placeholders
    """
    transform_dataset = []

    # Transform and Save input
    num_data = len(dataset)
    num_test = max([d.shape[0] for d in dataset if _hasattr_iter(d)])

    for i in range(num_test):
        # Split data for each test
        src_data = []
        for j in range(num_data):
            if _hasattr_iter(dataset[j]):
                src_data.append(dataset[j][i])
            else:
                src_data.append(dataset[j])

        # Transform input
        transform_data = src_data
        if f is not None:
            transform_data = f(transform_data)

        transform_dataset.append(transform_data)

    # Restore transform data to its original format
    next_test_data = []
    for i in range(num_data):
        next_test_data.append([])

        for j in range(num_test):
            if _hasattr_iter(transform_dataset[j][i]):
                next_test_data[i].append(transform_dataset[j][i].tolist())
            else:
                next_test_data[i] = transform_dataset[j][i]

        if _hasattr_iter(next_test_data[i]):
            next_test_data[i] = np.array(
                next_test_data[i],
                dtype=in_placeholders[i].dtype.as_numpy_dtype)

    # generate feed_dict
    feed_dict = {}
    for p, d in zip(in_placeholders, next_test_data):
        feed_dict[p] = d

    # start predict
    prediction_output = sess.run(target_layer, feed_dict=feed_dict)

    return transform_dataset, prediction_output, next_test_data


# def _debug_mnist(x1, t_i_x1):
#     from matplotlib import pyplot as plt
#     plt.figure(figsize=(10, 10))
#     plt.subplot(1, 2, 1)
#     plt.imshow(np.array(x1).reshape(28, 28))
#     plt.subplot(1, 2, 2)
#     plt.imshow(np.array(t_i_x1).reshape(28, 28))
#
#     plt.show()
