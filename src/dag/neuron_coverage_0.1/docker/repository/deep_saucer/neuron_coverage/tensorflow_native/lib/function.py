# ******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
# ******************************************************************************************
from nnutil import Network_tf, Density, Graph_tf, get_outputs_per_input_tf, \
    Coverage, density_to_heatmap_html, get_outputs_per_layer_tf, TestCaseGenerator
import config.implement as implement
import webbrowser
import os


class CoverageFunction:
    def __init__(self, model, feed_dict_xk, determination_on_activation_kw, activation_value_add_neuron_kw, json_data):
        """
        CoverageFunction initialise
        :param model: tensorflow graph session
        :param feed_dict_xk: dict
        :param determination_on_activation_kw: dict
        :param activation_value_add_neuron_kw: dict
        :param json_data: dict
        """
        self.model = model
        self.feed_dict_xk = feed_dict_xk
        self.determination_on_activation_kw = determination_on_activation_kw
        self.activation_value_add_neuron_kw = activation_value_add_neuron_kw
        self.json_data = json_data

    def coverage_rate_output(self):
        """
        Output coverage ratio
        """
        inp = get_outputs_per_layer_tf(self.model, self.feed_dict_xk, self.json_data["target_scope_name"])
        network = Network_tf(inp, self.determination_on_activation_kw, self.activation_value_add_neuron_kw)
        coverage = Coverage()

        # Output the coverage ratio
        print('Coverage rate all layer :  ' + str(coverage.activation_rate(network)))
        # Output the coverage ratio of each layer
        result = []
        for layer in network:
            print('Coverage rate one layer ' + str(layer) + ':  ' + str(coverage.activation_rate(layer)))
            result.append({str(layer): str(coverage.activation_rate(layer))})

        del inp, coverage, network

        return result

    def coverage_heatmap_output(self):
        """
        Output coverage heatmap
        """
        # Generate html of heat map image
        inp = get_outputs_per_input_tf(self.model, self.feed_dict_xk, self.json_data["target_scope_name"])
        graph = Graph_tf(inp, self.determination_on_activation_kw, self.activation_value_add_neuron_kw)
        density = Density(graph)
        density.update(self.activation_value_add_neuron_kw['activation_value'])
        html_file_pass = density_to_heatmap_html(density)
        del inp, graph, density

        # Display heat map image in browser
        webbrowser.open(html_file_pass)
        return html_file_pass

    def combination_cov_output(self, first, second):
        """
        Output combination coverage
        :type first: int
        :type second: int
        """
        inp = get_outputs_per_input_tf(self.model, self.feed_dict_xk, self.json_data["target_scope_name"])
        graph = Graph_tf(inp, self.determination_on_activation_kw, self.activation_value_add_neuron_kw)
        density = Density(graph)
        try:
            multiple_layers_combination_activation_rate, _ = \
                density.multiple_layers_combination_activation_rate(first, second)
        except MemoryError:
            print('Out Of Memory Error')
        else:
            print('Multiple layers combination coverage rate ' + str(first) + ' and '
                  + str(second) + ': ' + str(multiple_layers_combination_activation_rate))

        del inp, graph, density

        result = {str(first) + ' and ' + str(second): str(multiple_layers_combination_activation_rate)}
        return result

    def test_case_generator(self, x_placeholders, y_placeholders, k_placeholders, x_input, y_input, k_input):
        """
        Output increase coverage rate data instance
        :param x_placeholders: list of placeholder
        :param y_placeholders: list of placeholder
        :param k_placeholders: list of placeholder
        :param x_input: list of ndarray
        :param y_input: list of ndarray
        :param k_input: list of ndarray
        :return:
        """
        cls = getattr(implement, self.json_data["implement_class_name"])
        implement_class = cls()

        # get atomic manipulations
        atomic_manipulations, lower, upper = implement_class.get_atomic_manipulations()

        # Get Instance
        tcg = TestCaseGenerator(self.model,
                                x_placeholders,
                                y_placeholders,
                                k_placeholders,
                                x_input,
                                y_input,
                                k_input,
                                self.determination_on_activation_kw,
                                self.activation_value_add_neuron_kw,
                                self.json_data["edit_num"],
                                atomic_manipulations,
                                self.json_data["target_scope_name"],
                                self.json_data["increase_rate"])

        # Main processing
        while tcg.continuous_evaluation(self.json_data["target_rate"]):
            # Generate test cases and recalculate coverage
            tcg.test_case_generator_main(lower, upper)
            # Output coverage ratio
            print("Coverage rate sum layer : %g" % tcg.get_coverage_rate()[-1])

        # Save an atomic operation or a dataset operated with grad
        abs_dataset_pass = tcg.save_data(self.json_data["output_file_name"])
        # Acquire the history of the process of increasing the coverage rate
        coverage_rate = tcg.get_coverage_rate()
        return coverage_rate, abs_dataset_pass