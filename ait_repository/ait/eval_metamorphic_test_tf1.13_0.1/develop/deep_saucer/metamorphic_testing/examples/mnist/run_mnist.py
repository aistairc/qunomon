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
import sys
import tensorflow as tf
from pathlib import Path

from tensorflow.examples.tutorials.mnist import input_data

_proj_dir = Path(__file__).absolute().parent.parent.parent
_lib_dir = Path(_proj_dir, 'lib')
_examples_dir = Path(_proj_dir, 'examples')
_examples_mnist = Path(_examples_dir, 'mnist')

sys.path.append(str(_proj_dir))
sys.path.append(str(_lib_dir))

os.chdir(str(Path(__file__).parent))
_current = Path(os.getcwd()).absolute()

from lib.metamorphic_verification import main

if __name__ == '__main__':
    mnist_dataset = input_data.read_data_sets(
        str(_examples_mnist.joinpath('data')), one_hot=True)

    model_path = _examples_mnist.joinpath('model', 'model_mnist.ckpt')
    sess = tf.Session()
    saver = tf.train.import_meta_graph(str(model_path) + '.meta')
    saver.restore(sess, str(model_path))

    conf_path = _examples_mnist.joinpath('configs', 'config_mnist.json')

    main(sess, [mnist_dataset.test.images], str(conf_path))
