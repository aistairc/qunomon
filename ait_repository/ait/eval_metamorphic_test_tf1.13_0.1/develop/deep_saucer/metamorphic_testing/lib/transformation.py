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
import random


def T(x):
    t_x = np.copy(x)
    random.seed(1)
    for i in range(len(t_x)):
        for j in range(len(t_x[i])):
            r = random.randint(0, 5) / 100
            t_x[i][j] = x[i][j] + r

    return t_x


def S(y):
    t_y = y
    return t_y
