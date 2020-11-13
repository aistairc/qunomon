# ******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
# ******************************************************************************************
import tensorflow as tf

NUM_CLASSES = 10


class model_construction:

    def interence(imegs_placeholder, keep_prob):
        def weight_variable(shape):
            inital = tf.truncated_normal(shape, stddev=0.1)
            return tf.Variable(inital)

        def bias_variable(shape):
            inital = tf.constant(0.1, shape=shape)
            return tf.Variable(inital)

        def conv2d(x, W):
            return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding="SAME")

        def max_pool_2x2(x):
            return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding="SAME")

        x_image = tf.reshape(imegs_placeholder, [-1, 28, 28, 1])

        with tf.name_scope("conv1") as scope:
            W_conv1 = weight_variable([3,3,1,16])
            b_conv1 = bias_variable([16])
            h_conv1 = tf.nn.sigmoid(conv2d(x_image, W_conv1) + b_conv1, name="debug_test_name")

        with tf.name_scope("conv2") as scope:
            W_conv2 = weight_variable([3,3,16,16])
            b_conv2 = bias_variable([16])
            h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2) + b_conv2)

        with tf.name_scope("pool1") as scope:
            h_pool1 = max_pool_2x2(h_conv2)

        with tf.name_scope("conv3") as scope:
            W_conv3 = weight_variable([3,3,16,32])
            b_conv3 = bias_variable([32])
            h_conv3 = tf.nn.relu(conv2d(h_pool1, W_conv3) + b_conv3)

        with tf.name_scope("conv4") as scope:
            W_conv4 = weight_variable([3,3,32,32])
            b_conv4 = bias_variable([32])
            h_conv4 = tf.nn.relu(conv2d(h_conv3, W_conv4) + b_conv4)

        with tf.name_scope("pool2") as scope:
            h_pool2 = max_pool_2x2(h_conv4)

        with tf.name_scope("conv5") as scope:
            W_conv5 = weight_variable([3,3,32,64])
            b_conv5 = bias_variable([64])
            h_conv5 = tf.nn.relu(conv2d(h_pool2, W_conv5) + b_conv5)

        with tf.name_scope("conv6") as scope:
            W_conv6 = weight_variable([3,3,64,64])
            b_conv6 = bias_variable([64])
            h_conv6 = tf.nn.relu(conv2d(h_conv5, W_conv6) + b_conv6)

        with tf.name_scope("pool3") as scope:
            h_pool3 = max_pool_2x2(h_conv6)

        with tf.name_scope("fc1") as scope:
            W_fc1 = weight_variable([4*4*64, 1024])
            b_fc1 = bias_variable([1024])
            h_pool3_flat = tf.reshape(h_pool3, [-1, 4*4*64])
            h_fc1 = tf.nn.relu(tf.matmul(h_pool3_flat, W_fc1) + b_fc1)
            h_fc_1_drop = tf.nn.dropout(h_fc1, keep_prob)

        with tf.name_scope("softmax") as scope:
            W_fc2 = weight_variable([1024, NUM_CLASSES])
            b_fc2 = bias_variable([NUM_CLASSES])
            y_conv = tf.nn.softmax(tf.matmul(h_fc_1_drop, W_fc2) + b_fc2)

        return y_conv

    def accuracy(logits, labels):

        correct_prediction = tf.equal(tf.argmax(logits, 1), tf.arg_max(labels, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        tf.summary.scalar("accuracy", accuracy)
        return accuracy

    def correct_prediction(logits, labels):

        correct_prediction = tf.equal(tf.argmax(logits, 1), tf.arg_max(labels, 1))
        return correct_prediction
