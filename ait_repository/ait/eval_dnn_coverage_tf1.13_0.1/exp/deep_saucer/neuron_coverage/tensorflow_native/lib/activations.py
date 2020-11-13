# -*- coding: utf-8 -*-
#******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
#******************************************************************************************
import numpy as np
from keras.activations import (softmax,
                               elu,
                               relu,
                               sigmoid,
                               serialize)


class Activation:
    def __init__(self, activation_func_name, determination_on_activation_kw, activation_value_add_neuron_kw):

        support_names = {serialize(activation) for activation
                         in (softmax, elu, relu, sigmoid)}

        if not isinstance(activation_func_name, str):
            raise TypeError(
                "unsupported type : {}.".format(type(activation_func_name)))

        activation_func_name = activation_func_name.lower()

        if not {activation_func_name}.issubset(support_names):
            raise TypeError(
                "unsupported activation_function : {}.".format(
                    activation_func_name))

        self.name = activation_func_name

        # set activation function
        if activation_func_name == "sigmoid":
            self.activation = lambda x: replace(x, determination_on_activation_kw, activation_value_add_neuron_kw)
        elif activation_func_name == "relu" or activation_func_name == "elu":
            self.activation = lambda x: replace(x, determination_on_activation_kw, activation_value_add_neuron_kw)
        elif activation_func_name == "softmax":
            self.activation = lambda x: np.array([_softmax(_) for _ in x])
        else:
            self.activation = None

    # def __set__(self, instance, value):
    #     self.activation = value

    def __str__(self):
        return self.name


def replace(x, determination_on_activation_kw, activation_value_add_neuron_kw):

    # If it is greater than or equal to the threshold (lower_bound), make it active.
    if determination_on_activation_kw["determination_on_activation"] == 0:
        if activation_value_add_neuron_kw["replace_num"] == 1:
            x[x >= determination_on_activation_kw["lower_bound"]] = 1
            x[x < determination_on_activation_kw["lower_bound"]] = 0
        else:
            x[x < determination_on_activation_kw["lower_bound"]] = 0

    # When it is equal to or larger than the lower limit (lower_bound)
    # and equal to or smaller than the upper limit (upper_bound), it is made active.
    elif determination_on_activation_kw["determination_on_activation"] == 1:
        x[x < determination_on_activation_kw["lower_bound"]] = 0
        x[x > determination_on_activation_kw["upper_bound"]] = 0
        if activation_value_add_neuron_kw["replace_num"] == 1:
            x[x != 0] = 1

    # Activate the upper μ-th value.
    elif determination_on_activation_kw["determination_on_activation"] == 2:
        # Acquire the upper μ-th value for each network
        for i, x_copy in enumerate(x):
            # Acquire upper μ(superior_columns) value
            unique_x = np.unique(np.reshape(x_copy,-1))
            superior_columns = np.sort(unique_x)[::-1][0:determination_on_activation_kw["activation_filter_no"]]

            # Initialize the result
            result = np.zeros(x_copy.shape)
            # Replace the neuron value of the upper μ-th(superior_column) value
            for superior_column in superior_columns:
                # Initialize x_work with original value
                x_work = np.copy(x_copy)

                # Replacement process
                x_work[x_work != superior_column] = 0
                if activation_value_add_neuron_kw["replace_num"] == 1:
                    x_work[x_work == superior_column] = 1

                # A value is set to the neuron judged to be activated
                result = np.add(result, x_work)

            # Replace with neuron value after replacement
            x[i] = np.copy(result)

    return x


def _softmax(x):
    """
    :type x: np.ndarray
    :rtype: np.ndarray

    >>> import numpy as np
    >>> np.random.seed(1)
    >>> x = np.random.randn(2, 2)
    >>> _softmax(x)
    array([[ 1.,  0.],
           [ 0.,  0.]])
    """

    max_value = x.max()
    x[x != max_value] = 0
    x[x == max_value] = 1

    return x
