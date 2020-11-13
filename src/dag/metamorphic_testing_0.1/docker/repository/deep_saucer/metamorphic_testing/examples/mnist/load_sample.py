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
from pathlib import Path

from lib.utils.structutil import NetworkStruct

_proj_dir = Path(__file__).absolute().parent.parent.parent
_lib_dir = Path(_proj_dir, 'lib')
_examples_dir = Path(_proj_dir, 'examples')
_examples_mnist = Path(_examples_dir, 'mnist')

_current = Path(os.getcwd()).absolute()

if __name__ == '__main__':

    ns = NetworkStruct()
    # ret = ns.load(str(_examples_mnist.joinpath('model', 'model_mnist.ckpt')))
    ret = ns.load_struct(
        str(_examples_mnist.joinpath('model', 'model_mnist.ckpt_name.json')))

    if ret:
        ns.print_vars()
