# -*- coding: utf-8 -*-
# ******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
# ******************************************************************************************
import h5py
import json


def load_dataset(filename):
    """
    :type filename: str
    """
    try:
        with h5py.File(filename, "r") as hf:
            x, y = hf['images'][:], hf['labels'][:]
        print("Loaded images from {0}".format(filename))
        print("shape: {0}".format(x.shape))
        print("dtype: {0}".format(x.dtype))
        return x, y
    except (IOError, OSError, KeyError):
        print("Couldn't load dataset from hdf5 file")


# Method of argument error handling
def argument_exception_trow(error_message):
    raise ValueError("Argument exception：" + error_message)


def default_value_setting(config):
    # Required item check
    if "lower_bound" not in config and config.get("determination_on_activation", 0) == 1:
        argument_exception_trow("lower_bound is a required item in the config.json")
    elif "upper_bound" not in config and config.get("determination_on_activation", 0) == 1:
        argument_exception_trow("upper_bound is a required item in the config.json")
    elif "combination_first" not in config and config.get("combination_type", 0) == 1:
        argument_exception_trow("combination_first is a required item in the config.json")
    elif "combination_second" not in config and config.get("combination_type", 0) == 1:
        argument_exception_trow("combination_second is a required item in the config.json")
    elif "target_scope_name" not in config:
        argument_exception_trow("target_scope_name is a required item in the config.json")
    elif "network_structure_path" not in config:
        argument_exception_trow("network_structure_path is a required item in the config.json")
    elif "dataset_x_num" not in config:
        argument_exception_trow("dataset_x_num is a required item in the config.json")
    elif "dataset_y_num" not in config:
        argument_exception_trow("dataset_y_num is a required item in the config.json")
    elif "dataset_k_num" not in config:
        argument_exception_trow("dataset_k_num is a required item in the config.json")
    elif "implement_class_name" not in config:
        argument_exception_trow("implement_class_name is a required item in the config.json")

    # Create internal use data
    set_default_data = {
        "determination_on_activation": config.get("determination_on_activation", 0),
        "threshold": config.get("threshold", 0),
        "lower_bound": config.get("lower_bound", 0),
        "upper_bound": config.get("upper_bound", 0),
        "heat_map_type": config.get("heat_map_type", 1),
        "activation_filter_no": config.get("activation_filter_no", 1),
        "combination_type": config.get("combination_type", 0),
        "combination_first": config.get("combination_first", 0),
        "combination_second": config.get("combination_second", 0),
        "target_scope_name": config.get("target_scope_name", None),
        "edit_num": config.get("edit_num", 100),
        "target_rate": config.get("target_rate", 1.0),
        "increase_rate": config.get("increase_rate", 0.0),
        "output_file_name": config.get("output_file_name", "output.h5"),
        "network_structure_path": config.get("network_structure_path", 0),
        "dataset_x_num": config.get("dataset_x_num", 0),
        "dataset_y_num": config.get("dataset_y_num", 0),
        "dataset_k_num": config.get("dataset_k_num", 0),
        "split_dataset_start": config.get("split_dataset_start", 0),
        "split_dataset_end": config.get("split_dataset_end", None),
        "implement_class_name": config.get("implement_class_name", 0)
    }

    return set_default_data


def get_json(file_pass):
    # f = open(file_pass, 'r')
    # json_data = json.load(f)

    # defalt check
    json_data = default_value_setting(file_pass)

    # Method for determining activation
    determination_on_activation = json_data["determination_on_activation"]

    # A method for determining an activation value to be added to a neuron
    heat_map_type = json_data["heat_map_type"]

    # Method for determining activation
    if determination_on_activation == 0:  # 0:Threshold or more active
        lower_bound = json_data["threshold"]  # Threshold (lower_bound)
        if lower_bound == "":
            # Setting default values
            lower_bound = 0.0
        upper_bound = ""
        activation_filter_no = ""

    elif determination_on_activation == 1:  # 1:Activate within lower_bound or more upper_bound
        lower_bound = json_data["lower_bound"]  # Lower limit (lower_bound)
        upper_bound = json_data["upper_bound"]  # Upper limit (upper_bound)
        activation_filter_no = ""

        # Argument check
        if type(lower_bound) is str:
            argument_exception_trow("The value of lower_bound is not set. Or it is not a numeric type.")
        if type(upper_bound) is str:
            argument_exception_trow("The value of upper_bound is not set. Or it is not a numeric type.")
        if lower_bound > upper_bound:
            argument_exception_trow("The value of upper_bound must be greater than lower_bound.")

    elif determination_on_activation == 2:  # 2: Activate up to μ μth layer in each layer
        lower_bound = 0
        upper_bound = 0
        activation_filter_no = json_data["activation_filter_no"]  # Upper μ-number(activation_filter_no)

        if type(activation_filter_no) is int:
            if activation_filter_no < 1:
                argument_exception_trow(
                    "The value of activation_filter_no must be an integer greater than or equal to 1.")
        else:
            argument_exception_trow("The value of activation_filter_no must be an integer greater than or equal to 1.")
    else:
        argument_exception_trow("The value of determination_on_activation must be 0 or 1 or 2.")

    # # A method for determining an activation value to be added to a neuron
    # A：Simple increment
    if heat_map_type == 1 or heat_map_type == 0:
        replace_num = 1  # １：Activity should be 1. The inactivity is set to 0
        activation_value = 0  # 0：Add the value of activated neurons
    # B：Concentration coverage
    elif heat_map_type == 2:
        replace_num = 1  # １：Activity should be 1. The inactivity is set to 0
        activation_value = 1  # 1：We add the value that divides the value of activated neurons by weight
    # C1：Concentration based on activity value
    elif heat_map_type == 3:
        replace_num = 0  # 0：Activity is a value through activation function, inactivity is set to 0
        activation_value = 0  # 0：Add the value of activated neurons
    # C2：Concentration based on activity value
    elif heat_map_type == 4:
        replace_num = 0  # 0：Activity is a value through activation function, inactivity is set to 0
        activation_value = 1  # 1：We add the value that divides the value of activated neurons by weight
    else:
        argument_exception_trow("The value of heat_map_type must be 0 or 1 or 2 or 3 or 4.")

    # Generate arguments
    determination_on_activation_kw = {'determination_on_activation': determination_on_activation,
                                      'lower_bound': lower_bound,
                                      'upper_bound': upper_bound,
                                      'activation_filter_no': activation_filter_no}
    activation_value_add_neuron_kw = {'activation_value_add_neuron_variation': heat_map_type,
                                      'replace_num': replace_num,
                                      'activation_value': activation_value}

    return determination_on_activation_kw, activation_value_add_neuron_kw, json_data
