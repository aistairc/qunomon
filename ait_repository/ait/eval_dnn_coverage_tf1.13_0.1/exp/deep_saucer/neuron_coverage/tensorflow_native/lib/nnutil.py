# -*- coding: utf-8 -*-
# ******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
# ******************************************************************************************
import functools
import operator
import types
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
import keras.backend as k
import numpy as np
from keras.layers import Activation
from activations import Activation as Act
import pandas as pd
import shutil
from datetime import datetime as dt
import os
import h5py
import tensorflow as tf
import re


class Density:
    def __init__(self, graph):
        self.graph = graph
        num_layers = len(graph.networks[0])
        self.result = [0] * num_layers

    def update(self, activation_value):
        for network in self.graph:
            weight = network.weight
            for layer in network.layers:
                layer.activated_output = layer.activated_output.astype("float32")

                if activation_value == 1:
                    layer.activated_output = layer.activated_output / weight

        for network in self.graph:
            for index, layer in enumerate(network.layers):
                self.result[index] += layer.activated_output

    def same_layers_combination_activation_rate(self, layer_no):
        # Calculation of Combination Ratio of the same layer
        size = self.graph.networks[0].layers[layer_no].activated_output[0].shape[0]
        all_sum = size * (size - 1) / 2
        combination_map = np.zeros((size, size), dtype=np.float32)
        for idx, network in enumerate(self.graph):
            # Replace activity value with 1
            activated_output = network.layers[layer_no].activated_output[0]
            activated_output[activated_output != 0] = 1
            # Make a map of combinations
            combination_map += np.outer(activated_output, activated_output).astype(np.float32)

        # Combination coverage ratio
        combination_activate_sum = 0
        for i, p in enumerate(combination_map):
            combination_activate_sum += np.count_nonzero(p[0:i])

        combination_coverage_rate = combination_activate_sum / all_sum
        return combination_coverage_rate, combination_map

    def multiple_layers_combination_activation_rate(self, first_layer_no, second_layer_no):

        if first_layer_no == second_layer_no:
            self.same_layers_combination_activation_rate(first_layer_no)

        first_layer_size = self.graph.networks[0].layers[first_layer_no].activated_output[0].shape[0]
        second_layer_size = self.graph.networks[0].layers[second_layer_no].activated_output[0].shape[0]
        all_sum = first_layer_size * second_layer_size

        combination_map = np.zeros((first_layer_size, second_layer_size), dtype=np.float32)

        for idx, network in enumerate(self.graph):
            # Replace activity value with 1
            first_layer_activated_output = network.layers[first_layer_no].activated_output[0]
            second_layer_activated_output = network.layers[second_layer_no].activated_output[0]
            first_layer_activated_output[first_layer_activated_output != 0] = 1
            second_layer_activated_output[second_layer_activated_output != 0] = 1
            # Make a map of combinations
            combination_map += np.outer(first_layer_activated_output, second_layer_activated_output).astype(np.float32)
            combination_map[combination_map != 0] = 1

        combination_coverage_rate = np.count_nonzero(combination_map) / all_sum
        return combination_coverage_rate, combination_map


class Coverage:
    @staticmethod
    def activation_rate(network):
        """
        :type network: Network
        :rtype: np.ndarray
        """
        activation_counters = network.activation_counters
        _counter = 0
        _size = 0
        for counter in activation_counters:
            _counter += np.count_nonzero(counter)
            _size += counter.size
        return _counter / _size

    @staticmethod
    def inactivation_rate(network):
        """
        :type network: Network
        :rtype: np.ndarray
        """
        inactivation_counters = network.inactivation_counters
        _counter = 0
        _size = 0
        for counter in inactivation_counters:
            _counter += np.count_nonzero(counter)
            _size += counter.size
        return np.array([_counter / _size])


class IActivationResult(metaclass=ABCMeta):
    @abstractmethod
    def activation_counters(self):
        """ return at least one non_activated counters per layer.
        :rtype: np.ndarray
        """
        pass

    @abstractmethod
    def inactivation_counters(self):
        """ return at least one non_activated counters per layer.
        :rtype: np.ndarray
        """
        pass

    @abstractmethod
    def get_input_count(self):
        """ return the number of input shapes.
        :rtype: int
        """
        pass

    @abstractmethod
    def get_unit_count(self):
        """ return the number of all units.
        :rtype: int
        """
        pass


class Graph(Sequence):
    def __init__(self, model, layer_filters, inputs, determination_on_activation_kw, activation_value_add_neuron_kw):
        """
        :type model: keras.model
        :type layer_filters: list[keras.core.layers]
        :type inputs: np.ndarray or list[np.ndarray]
        """
        self.layer_filters = layer_filters
        # self.input = inp
        self.networks = [Network(model, layer_filters, inp, determination_on_activation_kw,
                                 activation_value_add_neuron_kw) for inp in inputs]

    def __len__(self):
        return len(self.networks)

    def __getitem__(self, index):
        return self.networks[index]


class Graph_tf(Sequence):
    def __init__(self, inputs, determination_on_activation_kw, activation_value_add_neuron_kw):
        # self.layer_filters = layer_filters
        # self.input = inp

        self.networks = [Network_tf(inp, determination_on_activation_kw, activation_value_add_neuron_kw)
                         for inp in inputs]

    def __len__(self):
        return len(self.networks)

    def __getitem__(self, index):
        return self.networks[index]


class Network(IActivationResult, Sequence):
    def __init__(self, model, layer_filters, model_input, determination_on_activation_kw,
                 activation_value_add_neuron_kw):
        """
        :type model: keras.model
        :type layer_filters: list[keras.core.layers]
        :type model_input: np.ndarray or list[np.ndarray]
        """
        if isinstance(model_input, np.ndarray):
            pass
        elif isinstance(model_input, types.GeneratorType):
            pass
        elif isinstance(model_input, list):
            self.input_shape = model_input[0].shape[0]
        else:
            raise TypeError()
        self.all_units = []
        self.layer_filters = layer_filters
        self.input = model_input
        self.layers = [self.set_layer(layer, determination_on_activation_kw, activation_value_add_neuron_kw)
                       for layer in model.layers
                       if is_any_layer(layer, self.layer_filters)]
        self.update()
        self.weight = np.sum([layer.weight for layer in self.layers])

    @staticmethod
    def set_layer(layer, determination_on_activation_kw, activation_value_add_neuron_kw):
        activation_func_name = layer.activation.__name__
        _layer = Layer(layer.name, activation_func_name, layer.output_shape)
        _layer.activation_func = Act(activation_func_name, determination_on_activation_kw,
                                     activation_value_add_neuron_kw).activation
        return _layer

    def update(self):
        """
        Update input value of model and layers
        """
        self.all_units = []
        for layer, output in zip(self.layers, self.input):
            layer.update(output)
            self.all_units.append(layer.units_num)

    @property
    def activation_counters(self):
        return self.get_activation_counters_per_layers

    @property
    def inactivation_counters(self):
        return self.get_inactivation_counters_per_layers

    @property
    def get_activation_counters_per_layers(self):
        """ return at least one activated counters per layer.
        :rtype: tuple(np.ndarray)
        """
        return ((np.sum(layer.activated_output, axis=0)
                 for layer in self.layers))

    @property
    def get_inactivation_counters_per_layers(self):
        """ return at least one non_activated counters per layer.
        :rtype: tuple(np.ndarray)
        """
        return ((self.input_shape - np.sum(layer.activated_output, axis=0)
                 for layer in self.layers))

    def get_unit_count(self):
        pass

    def get_input_count(self):
        pass

    def __getitem__(self, index):
        return self.layers[index]

    def __len__(self):
        return len(self.layers)


class Network_tf(IActivationResult, Sequence):
    def __init__(self, inp, determination_on_activation_kw, activation_value_add_neuron_kw):
        """
        :type model_input: np.ndarray or list[np.ndarray]
        """
        model_input = inp["layer_outputs"]
        layer_name = inp["scope_name"]
        layer_shapes = inp["layer_shapes"]

        if isinstance(model_input, list):
            self.input_shape = model_input[0].shape[0]
        else:
            raise TypeError()
        self.all_units = []
        # self.layer_filters = layer_filters
        self.input = model_input
        self.layers = [
            self.set_layer(layer, layer_shapes[i], determination_on_activation_kw, activation_value_add_neuron_kw)
            for i, layer in enumerate(layer_name)]
        self.update()
        self.weight = np.sum([layer.weight for layer in self.layers])

    @staticmethod
    def set_layer(layer, layer_shape, determination_on_activation_kw, activation_value_add_neuron_kw):
        activation_func_name = layer[-1]

        # _layer = Layer(layer.name, activation_func_name, layer.output_shape)
        _layer = Layer(layer[0], activation_func_name, layer_shape)
        _layer.activation_func = Act(activation_func_name, determination_on_activation_kw,
                                     activation_value_add_neuron_kw).activation
        return _layer

    def update(self):
        """
        Update input value of model and layers
        """
        self.all_units = []
        for layer, output in zip(self.layers, self.input):
            layer.update(output)
            self.all_units.append(layer.units_num)

    @property
    def activation_counters(self):
        return self.get_activation_counters_per_layers

    @property
    def inactivation_counters(self):
        return self.get_inactivation_counters_per_layers

    @property
    def get_activation_counters_per_layers(self):
        """ return at least one activated counters per layer.
        :rtype: tuple(np.ndarray)
        """
        return ((np.sum(layer.activated_output, axis=0)
                 for layer in self.layers))

    @property
    def get_inactivation_counters_per_layers(self):
        """ return at least one non_activated counters per layer.
        :rtype: tuple(np.ndarray)
        """
        return ((self.input_shape - np.sum(layer.activated_output, axis=0)
                 for layer in self.layers))

    def get_unit_count(self):
        pass

    def get_input_count(self):
        pass

    def __getitem__(self, index):
        return self.layers[index]

    def __len__(self):
        return len(self.layers)


class ALayer(object):
    pass


class HiddenLayer(ALayer):
    pass


class OutputLayer(ALayer):
    pass


class Layer(IActivationResult):
    def __init__(self, layer_name, activation_function_name, output_shapes):
        """
        :type layer_name: str
        :type activation_function_name: str
        :type output_shapes: tuple
        """
        self.name = layer_name
        self.activation = activation_function_name
        self.output_shapes = output_shapes
        self.input_shapes = 0
        self.units_num = functools.reduce(operator.mul, output_shapes[1:], 1)
        self.activation_func = None
        self.activated_output = None
        self.weight = 0

    def update(self, model_input):
        """ Execute this class method each time input changes.
        It will be set activated_outputs.
        When the layer name is "conv",
        activated_outputs is reshaped to flatten outputs.

        ex: input_shape (1, 32, 32, 32) -> output_shape (1, 32768)

        :type model_input: np.ndarray
        """
        self.input_shapes = model_input.shape[0]
        if self.activation_func:
            activated_output = self.activation_func(model_input)
            if 'conv' in self.name.lower():
                activated_output = activated_output.reshape(
                    [self.input_shapes, self.units_num])
                # channel first
                self.activated_output = activated_output
            else:
                # channel first
                self.activated_output = activated_output

        else:
            raise TypeError

        self.weight = np.sum(activated_output)

    @property
    def activation_counters(self):
        return np.sum(self.activated_output, axis=0)

    @property
    def inactivation_counters(self):
        return self.input_shapes - np.sum(self.activated_output, axis=0)

    def get_unit_count(self):
        return self.input_shapes

    def get_input_count(self):
        return self.input_shapes

    def __str__(self):
        return self.name


class TestCaseGenerator:

    def __init__(self,
                 sess,
                 x_placeholders,
                 y_placeholders,
                 k_placeholders,
                 x_input,
                 y_input,
                 k_input,
                 determination_on_activation_kw,
                 activation_value_add_neuron_kw,
                 edit_num,
                 atomic_manipulations,
                 target_scope_name=None,
                 increase_rate=None):
        """
        :param sess: tensorflow graph session
        :param x_placeholders: list of placeholder
        :param y_placeholders: list of placeholder
        :param k_placeholders: list of placeholder
        :param x_input: list of ndarray
        :param y_input: list of ndarray
        :param k_input: list of ndarray
        :param determination_on_activation_kw: dict
        :param activation_value_add_neuron_kw: dict
        :param edit_num: int, which is the number of data to be converted at a time to increase coverage
        :param atomic_manipulations: list of function
        :param target_scope_name: dict
        """
        # Argument check
        x_check = x_input[0].shape[0]
        y_check = y_input[0].shape[0]

        for _ in x_input:
            if _.shape[0] != x_check:
                raise Exception("The total number of data of input and label must match")
            if _.shape[0] != y_check:
                raise Exception("The total number of data of input and label must match")

        for _ in y_input:
            if _.shape[0] != x_check:
                raise Exception("The total number of data of input and label must match")

        if atomic_manipulations is None:
            raise Exception("atomic_manipulations is undefined")

        if len(atomic_manipulations) != len(x_input):
            raise Exception("The number of arrays of input and atomic_manipulations must match")

        self.sess = sess
        self.x_placeholders = x_placeholders  # Place folder(input)
        self.y_placeholders = y_placeholders  # Place folder(label)
        self.k_placeholders = k_placeholders  # Place folder(keep prob)
        self.mnp_x = x_input  # image data set
        self.mnp_y = y_input  # label data set
        self.mnp_k = k_input  # keep prob data set
        self.edit_num = edit_num  # Number of sheets to be processed per one time
        self.determination_on_activation_kw = determination_on_activation_kw  # option data
        self.activation_value_add_neuron_kw = activation_value_add_neuron_kw  # option data
        self.target_scope_name = target_scope_name  # target scope name
        self.counta = 0  # loop counta
        self.mnp_activity_status = None  # coverage status
        self.origin_atomic_manipulations = atomic_manipulations
        self.atomic_manipulations = atomic_manipulations
        self.grad_graph = self.__get_grad_graph()  # Get gradient of coverage increase graph
        self.base_activity_status = self.__get_activity_status()  # Set value to mnp_activity_status
        self.coverage_rate = [
            np.count_nonzero(self.base_activity_status) / self.base_activity_status.size]  # coverage rate
        self.used_mnp = []  # Keep used atomic manipulation index
        self.increase_rate = increase_rate

    def test_case_generator_main(self, lower, upper):
        """ Generate the input operated by atomic_manipulations and recalculate the coverage
        :param lower: list
        :param upper: list
        """
        # Argument check
        if len(self.mnp_x) != len(lower):
            raise Exception("The number of arrays of lower and x_input must match")
        if len(self.mnp_x) != len(upper):
            raise Exception("The number of arrays of upper and x_input must match")

        # You can manipulate deq_x using select mnp or grad.
        mnp_x = self.__get_edit_data(self.increase_rate)

        add_mnp_x = []
        # Because the tutorial uses MNIST data, each element of the input vector should be leq than 1, and geq than 0
        for _x, _up, _lo in zip(mnp_x, upper, lower):
            _x[_x > upper] = _up
            _x[_x < lower] = _lo
            add_mnp_x.append(_x)

        self.__set_edit_data(add_mnp_x)

    def save_data(self, file_pass='output.h5'):
        """Function to save new dataset
        :type file_pass: String
        :rtype bool
        """

        # Save
        from pathlib import Path
        tf_native_dir = Path(__file__).parent.absolute()
        pass_ = tf_native_dir.joinpath(file_pass)
        with h5py.File(pass_, 'w') as f:
            f.create_dataset('value', data=self.mnp_x)
            f.create_dataset('label', data=self.mnp_y)
        return pass_

    def continuous_evaluation(self, target_rate=None):
        """Function for determining continuation
        :type target_rate: float
        """

        # Set the evaluation value
        max_counta = self.mnp_x[0].shape[0]
        target_rate = target_rate if target_rate is not None else 100

        # Add atomic manipulation to all images and exit
        if self.counta >= max_counta:
            return False
        # Goal achievement and exit
        elif self.coverage_rate[-1] >= target_rate:
            return False
        # continue
        else:
            self.counta = self.counta + self.edit_num
            remaining_data_num = max_counta - self.counta
            if remaining_data_num < 0:
                self.edit_num = self.edit_num + remaining_data_num

            return True

    def get_coverage_rate(self):
        """Function for get coverage rate
        :rtype:float
        """
        return self.coverage_rate

    def get_feed_dict(self, set_label=None):
        """Function for acquiring feed_dict operated with atomic manipulation.
        If set_value is 1, then set x and y and k(if it is not None) to feed_dict.
        else, then set x and k(if it is not None) to feed_dict.
        :type set_label: int
        :rtype feed_dict: dict
        """
        feed_dict = {}
        for input_placeholder, value in zip(self.x_placeholders, self.get_mnp_x()):
            feed_dict[input_placeholder] = value

        if set_label == 1:
            for input_placeholder, value in zip(self.y_placeholders, self.get_mnp_y()):
                feed_dict[input_placeholder] = value

        if self.k_placeholders is not None:
            for input_placeholder, value in zip(self.k_placeholders, self.get_mnp_k()):
                feed_dict[input_placeholder] = value

        return feed_dict

    def get_mnp_x(self):
        """Get operation x_input
        :rtype list of ndarray
        """
        return self.mnp_x

    def get_mnp_y(self):
        """Get operation y_input
        :rtype list of ndarray
        """
        return self.mnp_y

    def get_mnp_k(self):
        """Get operation k_input
        :rtype list
        """
        return self.mnp_k

    def __get_edit_data(self, st_increase_rate=None):
        """Return x_input to be updated and atomic manipulation and grad corresponding to x_input
        :rtype mnp_x: list of ndarray
        """

        # Calculate and choose mnp that is close to the slope
        grad = self.sess.run(self.grad_graph, feed_dict=self.get_feed_dict())
        grad = [_[0:self.edit_num] for _ in grad]
        dequeue_x = [_[0:self.edit_num] for _ in self.mnp_x]

        # Monitor the last 5 coverage increase rates
        self.__growth_rate_check_process(st_increase_rate)

        # Select the optimum atomic manipulation
        # mnp_info[0] indicates input after optimal atomic operation
        mnp_info = [self.__search_similarity_mnp(_g[0:self.edit_num], _m, _x[0:self.edit_num]) for _g, _m, _x in
                    zip(grad, self.atomic_manipulations, dequeue_x)]
        mnp_x = [_[0] for _ in mnp_info]

        # Hold the used A subscript
        if len(self.used_mnp) == 0:
            self.used_mnp = [np.unique(_[1]) for _ in mnp_info]
        else:
            self.used_mnp = [np.unique(np.append(ori, new[1])) for ori, new in zip(self.used_mnp, mnp_info)]

        return mnp_x

    def __set_edit_data(self, mnp_x):
        """Calculate the coverage and calculate the total value with the original coverage.
        :type mnp_x: list of ndarray
        """
        # Enqueue mnp_x
        slice_x = [_[self.edit_num:] for _ in self.mnp_x]
        self.mnp_x = [np.append(_slice_x, _mnp_x, axis=0) for _mnp_x, _slice_x in zip(mnp_x, slice_x)]

        # Enqueue mnp_y
        slice_y = [_[self.edit_num:] for _ in self.mnp_y]
        inq_y = [_[:self.edit_num] for _ in self.mnp_y]
        self.mnp_y = [np.append(_slice_y, _inq_y, axis=0) for _slice_y, _inq_y in zip(slice_y, inq_y)]

        # Get Activity status
        self.mnp_activity_status = self.__get_activity_status()

        # Calculate coverage rate sum
        self.__set_add_coverage_rate(self.base_activity_status, self.mnp_activity_status)

    def __growth_rate_check_process(self, st_increase_rate=None):

        if st_increase_rate is not None and len(self.coverage_rate) >= 5 and self.coverage_rate[-1] - \
                self.coverage_rate[-5] < st_increase_rate:
            # Delete used atomic manipulation once
            self.atomic_manipulations = [list(np.delete(a, b, axis=0)) for a, b in
                                         zip(self.atomic_manipulations, self.used_mnp)]

            # If atomic_manipulations is None, restore the original atomic_manipulations
            for i, atomic_manipulation in enumerate(self.atomic_manipulations):
                if len(atomic_manipulation) == 0:
                    self.atomic_manipulations[i] = self.origin_atomic_manipulations[i]

            # Initialize
            self.used_mnp = []

    def __get_activity_status(self):

        # Use tensorFlow model
        feed_dict = self.get_feed_dict()
        inp = get_outputs_per_layer_tf(self.sess, feed_dict, self.target_scope_name)
        network = Network_tf(inp, self.determination_on_activation_kw, self.activation_value_add_neuron_kw)

        del inp

        activity_status = np.array([])
        for _ in network.activation_counters:
            activity_status = np.append(activity_status, _)

        return activity_status

    def __set_add_coverage_rate(self, counters1, counters2):

        self.base_activity_status = counters1 + counters2
        self.coverage_rate.append(np.count_nonzero(self.base_activity_status) / self.base_activity_status.size)

    def __get_grad_graph(self):

        # Access graph
        target_tensor_list = []
        graph = tf.get_default_graph()
        operations = graph.get_operations()

        for operation in operations:
            # Supports sigmoid, relu and elu
            sigmoid = True if "Sigmoid" == operation.op_def.name else False
            relu = True if "Relu" == operation.op_def.name else False
            elu = True if "Elu" == operation.op_def.name else False
            if sigmoid or relu or elu:
                if self.target_scope_name is not None:
                    for target_scope_name in self.target_scope_name:
                        if re.match(".*" + target_scope_name, operation.name):
                            target_tensor_list.append(tf.reshape(operation.outputs[0], [-1]))
                else:
                    target_tensor_list.append(tf.reshape(operation.outputs[0], [-1]))

        # Combine neurons of all layers
        all_layer = tf.concat(target_tensor_list, 0)
        # Let the neurons below the threshold be true(Boolean)
        mask = tf.less(all_layer, self.determination_on_activation_kw["lower_bound"])
        # Extracts the inactive layer, and calculates the total value
        mask_layer_sum = tf.reduce_sum(tf.boolean_mask(all_layer, mask))
        # Calculate gradient with input data for inactive layer
        st = tf.stop_gradient(self.k_placeholders)
        return tf.gradients(mask_layer_sum, self.x_placeholders, stop_gradients=st)

    @staticmethod
    def __search_similarity_mnp(h_grad_data, h_mmp_data, h_deq_x):

        used_mnp = np.asarray([])
        mnp_x = []

        # Choose the smallest atomic manipulation from the inner product of gradient and atomic manipulation list
        for g_data, deq_x in zip(h_grad_data, h_deq_x):
            # Get atomic manipulation
            mmp_data = np.array([_(deq_x) - deq_x for _ in h_mmp_data])
            # Select atomic manipulation which is the minimum angle with gradient
            sim = [np.dot(g_data.reshape(-1), (mnp / np.linalg.norm(mnp)).reshape(-1)) for mnp in mmp_data]
            # Get input data operated by atomic manipulation
            mnp_x.append(h_mmp_data[sim.index(max(sim))](deq_x))
            # Hold the used atomic manipulations subscript
            used_mnp = np.append(used_mnp, sim.index(max(sim)))

        mnp_x = np.asarray(mnp_x)

        return mnp_x, used_mnp


def is_any_layer(layer, layer_filters):
    """
    :type layer: object
    :type layer_filters: list[keras.layers, ]
    :rtype: bool

    >>> from keras.layers import Activation, Conv2D, Dense
    >>> is_any_layer(Dense(64), [Activation, Conv2D, Dense])
    True
    >>> is_any_layer(Dense(64), [Activation, Conv2D])
    False
    """

    if {type(layer)} & set(layer_filters):
        return True
    else:
        return False


def validate_not_include_in_activation_layer(model):
    """ Check whether model includes in activation layer or not.

    :type model: keras.model
    """
    for layer in model.layers:
        if is_any_layer(layer, [Activation]):
            raise AttributeError("This model includes in activation layer!!"
                                 "Try to use a model that includes "
                                 "the activation function as an argument")


def get_outputs_per_layer(model, layer_filters, model_inputs):
    """ Calculate the output of all layers using
     the weights and biases of existing learned models.

    :type model: keras.model
    :type layer_filters: list[keras.layers,]
    :type model_inputs: np.ndarray
    :rtype: list[np.ndarray]
    """
    # check model
    validate_not_include_in_activation_layer(model)

    funcs, model_multi_inputs_cond = get_intermediate_funcs(model,
                                                            layer_filters)

    if model_multi_inputs_cond:
        list_inputs = []
        list_inputs.extend(model_inputs)
        list_inputs.append(0.)
    else:
        list_inputs = [model_inputs, 0.]

    # Learning phase. 0 = Test mode (no dropout or batch normalization)
    # layer_outputs = [func([model_inputs, 0.])[0] for func in funcs]

    layer_outputs = [func(list_inputs)[0] for func in funcs]

    return layer_outputs


def get_outputs_per_layer_tf(sess, feed_dict_xk, target_scope_name_list=None):
    """ Calculate the output of all layers using
     the weights and biases of existing learned models of tensorFlow.

    :type sess: tensorFlow.InteractiveSession()
    :type feed_dict_xk: placeholder
    :type target_scope_name_list: List
    """
    graph = tf.get_default_graph()
    operations_list = graph.get_operations()

    target_tensor_list = []
    target_tensor_name_list = []
    for operation in operations_list:
        sigmoid = True if "Sigmoid" == operation.op_def.name else False
        relu = True if "Relu" == operation.op_def.name else False
        elu = True if "Elu" == operation.op_def.name else False
        softmax = True if "Softmax" == operation.op_def.name else False

        if sigmoid or relu or softmax or elu:
            target_tensor_list.append(graph.get_tensor_by_name(operation.name + ":0"))
            target_tensor_name_list.append([operation.name.split('/')[0], operation.op_def.name])

    if not target_tensor_list:
        raise TypeError("Available only with sigmoid, relu, or softmax")

    # Layer specification
    if target_scope_name_list is not None:
        target_one_tensor_list = []
        target_one_tensor_name_list = []
        for i, operation in enumerate(target_tensor_list):

            for target_scope_name in target_scope_name_list:
                layer_name = re.match(".*" + target_scope_name, operation.name)
                if layer_name:
                    target_one_tensor_list.append(operation)
                    target_one_tensor_name_list.append(target_tensor_name_list[i])

        target_tensor_list = target_one_tensor_list
        target_tensor_name_list = target_one_tensor_name_list

    if not target_tensor_list:
        raise TypeError("Scope of argument does not exist")

    layer_outputs = []
    layer_tensor_shapes = []
    for operation in target_tensor_list:
        layer_outputs.append(sess.run(operation, feed_dict=feed_dict_xk))
        layer_tensor_shapes.append([_.value for _ in tuple(operation.shape)])

    inp = {"layer_outputs": layer_outputs, "scope_name": target_tensor_name_list, "layer_shapes": layer_tensor_shapes}

    return inp


def get_outputs_per_input(model, layer_filters, model_inputs):
    """ Calculate the output of all layers using
    the weights and biases of existing learned models.

    :type model: keras.model
    :type layer_filters: list[keras.layers,]
    :type model_inputs: np.ndarray
    :rtype: list[np.ndarray]
    """

    validate_not_include_in_activation_layer(model)

    funcs, model_multi_inputs_cond = get_intermediate_funcs(model,
                                                            layer_filters)

    list_inputs = []
    if not model_multi_inputs_cond:
        for model_input in model_inputs:
            list_inputs.append([[model_input], 0.])

    # Learning phase. 0 = Test mode (no dropout or batch normalization)
    # layer_outputs = [func([model_inputs, 0.])[0] for func in funcs]
    layer_outputs = []
    for list_input in list_inputs:
        layer_outputs.append([func(list_input)[0] for func in funcs])

    return layer_outputs


def get_outputs_per_input_tf(model, feed_dict_xk, target_scope_name_list, ):
    """ Calculate the output of all layers using
     the weights and biases of existing learned models of tensorFlow.

    :type sess: tensorFlow.InteractiveSession()
    :type x_image: placeholder
    :type keep_prob: flote32
    :type x_input: np.ndarray
    :type target_scope_name_list: List
    """
    graph = tf.get_default_graph()
    operations = graph.get_operations()

    target_tensor_list = []
    target_tensor_name_list = []
    for operation in operations:
        sigmoid = True if "Sigmoid" == operation.op_def.name else False
        relu = True if "Relu" == operation.op_def.name else False
        elu = True if "Elu" == operation.op_def.name else False
        softmax = True if "Softmax" == operation.op_def.name else False

        if sigmoid or relu or softmax or elu:
            target_tensor_list.append(graph.get_tensor_by_name(operation.name + ":0"))
            target_tensor_name_list.append([operation.name.split('/')[0], operation.op_def.name])

    if not target_tensor_list:
        raise TypeError("Available only with sigmoid, relu, or softmax layers")

    # Layer specification
    if target_scope_name_list is not None:
        target_one_tensor_list = []
        target_one_tensor_name_list = []
        for i, operation in enumerate(target_tensor_list):

            for target_scope_name in target_scope_name_list:
                layer_name = re.match(".*" + target_scope_name, operation.name)
                if layer_name:
                    target_one_tensor_list.append(operation)
                    target_one_tensor_name_list.append(target_tensor_name_list[i])

        target_tensor_list = target_one_tensor_list
        target_tensor_name_list = target_one_tensor_name_list

    if not target_tensor_list:
        raise TypeError("Scope of argument does not exist")

    layer_outputs = []
    layer_tensor_shapes = []
    layer_tensor_name_list = []

    de_per_outputs = []
    de_per_tensor_shapes = []
    for operation in target_tensor_list:
        ov = model.run(operation, feed_dict=feed_dict_xk)
        de_per_outputs.append([_[np.newaxis] for _ in ov])
        de_per_tensor_shapes.append([_.value for _ in tuple(operation.get_shape())])

    for i, _ in enumerate(de_per_outputs[0]):
        wr = []
        for p, _ in enumerate(de_per_outputs):
            wr.append(de_per_outputs[p][i])

        layer_outputs.append(wr)

    for i in range(len(layer_outputs)):
        layer_tensor_shapes.append(tuple(de_per_tensor_shapes))
        layer_tensor_name_list.append(target_tensor_name_list)
    # debug test

    inp = []
    key = ["layer_outputs", "scope_name", "layer_shapes"]
    for val in zip(layer_outputs, layer_tensor_name_list, layer_tensor_shapes):
        inp.append(dict(zip(key, val)))

    return inp


def get_intermediate_funcs(model, layer_filters):
    """ Generate a function that outputs calculation result of middle layer.

    :type model: keras.model
    :type layer_filters: list[keras.layers,]
    :rtype: list[keras.backend.tensorflow_backend.Function], bool
    """
    inp = model.input
    model_multi_inputs_cond = True
    if not isinstance(inp, list):
        # only one input! let's wrap it in a list.
        inp = [inp]
        model_multi_inputs_cond = False

    outputs = [layer.output for layer in model.layers
               if is_any_layer(layer, layer_filters)]

    # evaluation functions
    funcs = [k.function(inp + [k.learning_phase()], [out])
             for out in outputs]

    return funcs, model_multi_inputs_cond


def density_to_heatmap_html(density):
    dfs = []
    # Get file path
    file_pass = os.path.dirname(__file__)
    # Generate file name
    timestamp = dt.now().strftime('%Y%m%d%H%M%S%f')
    file_name = "coverage_" + timestamp + ".html"

    for layer_no, layer in enumerate(density.result, 1):
        layer_name = density.graph.networks[0].layers[layer_no - 1].name
        layer_name_str = "\'" + layer_name + "\'"
        d = pd.DataFrame({"layer": [layer_no for j in range(layer.size)],
                          "layer_name": [layer_name_str for i in range(layer.size)],
                          "unit": [u for u in range(layer.size)],
                          "value": [unit for unit in layer[0]]})
        d["value"] = d["value"].round(10)
        dfs.append(d)

    master_df = pd.concat(dfs, ignore_index=True)
    pd.DataFrame(master_df).to_csv(file_name, index=False)

    # Write CSV format data to html file
    f = open(file_name)
    reline = f.readlines()
    f.close()
    new_val = []
    first_str = "\t\t\tvar in_data = [\n"
    last_str = "\t\t\t];\n"
    for idx, val in enumerate(reline, 0):
        val = val.replace('\n', '')
        if len(reline) == idx + 1:
            new_val_st = "\t\t\t[" + val + "]\n"
        else:
            new_val_st = "\t\t\t[" + val + "],\n"
        new_val.append(new_val_st)
    new_val[0] = first_str
    new_val.append(last_str)

    t = open(file_pass + '/heatMap/temp/templeate.html')
    html_str = t.readlines()
    t.close()

    w = open(file_name, "w")
    for idx1, val1 in enumerate(html_str, 0):

        if val1 == "\t\t\t// @Data setting position\n":
            for idx2, val2 in enumerate(new_val, 0):
                w.write(val2)
        else:
            w.write(val1)
    w.close()

    # Move files to the heatmap storage folder
    shutil.move(file_name, file_pass + '/heatMap')
    # Return the html file path of the created heatmap
    return file_pass + "/heatMap/" + file_name
