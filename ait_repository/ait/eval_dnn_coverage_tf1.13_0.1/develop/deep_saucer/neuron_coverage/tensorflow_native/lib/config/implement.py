# ******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
# ******************************************************************************************
import numpy as np


class FreeEdit:
    """ TODO The class name is the name defined in the json file."""

    def __init__(self):
        pass

    def get_atomic_manipulation(self):
        """
        Genarate atomic_manipulation
        :return: list of ndarray
        """
        return None


class Tutorial_sub:

    """Tutorial (MNIST)"""
    def __init__(self, id):
        self.id = id

    def manipulation_x0(self, x0):
        np.random.seed(self.id)
        mani = np.random.uniform(low=-0.2, high=0.2, size=(784,))
        new_x0 = x0 + mani
        return new_x0

    def manipulation_x1(self, x1):
        np.random.seed(self.id)
        mani = np.random.uniform(low=-0.4, high=0.4, size=(784,))
        new_x1 = x1 + mani
        return new_x1

class Tutorial:
    """Tutorial (MNIST)"""

    @ staticmethod
    def get_atomic_manipulations():
        """ Genarate atomic_manipulation
        :return atomic_manipulations: list of function.
                If there are a number of placeholders for input values,
                'atomic_manipulations includes manipulations corresponding to each placeholders
        :return lower: list of Maximum value of normalization.
        :return upper: list of Minimum value of normalization.
        """
        atomic_manipulations_x0 = []
        # atomic_manipulations_x1 = []
        num_of_manipulations = 1000
        for index in range(num_of_manipulations):
            atm_x0 = Tutorial_sub(index)
            atomic_manipulations_x0.append(atm_x0.manipulation_x0)

            # atm_x1 = Atm(index)
            # atomic_manipulations_x1.append(atm_x1.manipulation_x1)

        # atomic_manipulations = [atomic_manipulations_x0, atomic_manipulations_x1]
        atomic_manipulations = [atomic_manipulations_x0]

        # upper = [1, 1]
        # lower = [0, 0]
        upper = [1]
        lower = [0]

        # returning a list of vectors. Each vector is added to an input vector as an atomic manipulation
        return atomic_manipulations, lower, upper

