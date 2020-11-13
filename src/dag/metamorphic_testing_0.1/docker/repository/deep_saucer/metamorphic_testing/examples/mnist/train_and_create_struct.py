# -*- coding: utf-8 -*-
#******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
#******************************************************************************************
"""
# 1. Automatic output tutorial of information
"""
import math

from pathlib import Path

from six.moves import xrange
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data

from lib.utils.structutil import NetworkStruct

_proj_dir = Path(__file__).absolute().parent.parent.parent
_lib_dir = Path(_proj_dir, 'lib')
_examples_dir = Path(_proj_dir, 'examples')
_examples_mnist = Path(_examples_dir, 'mnist')


def training(out_path):
    # 2.
    ns = NetworkStruct()

    dataset = input_data.read_data_sets(
        str(_examples_mnist.joinpath('data')), False)

    x_placeholder = tf.placeholder(tf.float32, shape=(None, 28 * 28))
    y_placeholder = tf.placeholder(tf.int32, shape=(None, ))

    # 3.
    ns.set_input(placeholder=x_placeholder)

    w1 = tf.Variable(
        tf.truncated_normal(
            [28 * 28, 128], stddev=1.0 / math.sqrt(float(28 * 28))),
        name='weights1')
    b1 = tf.Variable(tf.zeros([128]), name='biases1')
    h1 = tf.nn.relu(tf.matmul(x_placeholder, w1) + b1)

    w2 = tf.Variable(
        tf.truncated_normal(
            [128, 32], stddev=1.0 / math.sqrt(float(128))),
        name='weights2')
    b2 = tf.Variable(tf.zeros([32]), name='biases2')
    h2 = tf.nn.relu(tf.matmul(h1, w2) + b2)

    w3 = tf.Variable(
        tf.truncated_normal([32, 10], stddev=1.0 / math.sqrt(float(32))),
        name='weights3')
    b3 = tf.Variable(tf.zeros([10]), name='biases3')

    logits = tf.matmul(h2, w3) + b3
    loss = tf.losses.sparse_softmax_cross_entropy(
        labels=tf.to_int64(y_placeholder),
        logits=logits
    )

    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train_op = optimizer.minimize(loss)

    correct_prediction = tf.nn.in_top_k(logits, y_placeholder, 1)
    accuracy = tf.reduce_sum(tf.cast(correct_prediction, tf.int32))

    max_prob = tf.argmax(logits, axis=1)
    # 4.
    ns.set_output(node=max_prob)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)

        # training
        for step in xrange(2000):
            x_feed, y_feed = dataset.train.next_batch(100, False)
            feed_dict = {
                x_placeholder: x_feed,
                y_placeholder: y_feed,
            }
            _, loss_value = sess.run([train_op, loss],
                                     feed_dict=feed_dict)

        true_count = accuracy.eval(
            feed_dict={
                x_placeholder: dataset.test.images,
                y_placeholder: dataset.test.labels
            })

        precision = float(true_count) / dataset.test.num_examples
        print('Test accuracy %0.04f' % precision)

        # 5.
        ns.set_info_by_session(sess=sess)
        # 6.
        ns.save(sess=sess, path=str(out_path.joinpath('model_mnist.ckpt')))

        # 7.
        # std out
        ns.print_vars()
        # File output
        with open(str(out_path.joinpath('vars_list.txt')), 'w') as ws:
            ns.print_vars(ws=ws)


if __name__ == '__main__':
    o_path = Path(_examples_mnist, 'model')

    training(o_path)
