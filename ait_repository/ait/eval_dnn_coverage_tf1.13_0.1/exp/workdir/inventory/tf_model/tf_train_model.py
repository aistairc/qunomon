#******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
#******************************************************************************************
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import tutorials.tf_model.tf_model as tf_model
from neuron_coverage.tensorflow_native.structutil import NetworkStruct

data_dir = r'C:\Users\yrl-user\Downloads\MNIST_data'
mnist = input_data.read_data_sets(data_dir, one_hot=True)
sess = tf.InteractiveSession()


def loss(logits, labels):

    cross_entropy = -tf.reduce_sum(labels*tf.log(logits))
    tf.summary.scalar("cross_entropy", cross_entropy)
    return cross_entropy

def training(loss, learning_rate):

    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)
    return train_step


if __name__ == "__main__":
    with tf.Graph().as_default():
        network_struct = NetworkStruct()
        x_image = tf.placeholder("float", shape=[None, 784])
        network_struct.set_input(x_image)

        y_label = tf.placeholder("float", shape=[None, 10])
        network_struct.set_input(y_label)

        W = tf.Variable(tf.zeros([784,10]))
        b = tf.Variable(tf.zeros([10]))

        keep_prob = tf.placeholder("float")
        network_struct.set_input(keep_prob)

        logits = tf_model.model_construction.interence(x_image, keep_prob)
        network_struct.set_output(logits)

        loss_value = loss(logits, y_label)
        train_op = training(loss_value,1e-4)
        accur = tf_model.model_construction.accuracy(logits, y_label)
        init_op = tf.global_variables_initializer()
        sess = tf.Session()
        sess.run(init_op)

        summary_op = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter("./tmp/data", graph=sess.graph)

        saver = tf.train.Saver()

        init = tf.global_variables_initializer()
        sess.run(init)

        for step in range(2000):
            batch = mnist.train.next_batch(50)
            if step % 100 == 0:
                train_accury = sess.run(accur, feed_dict={x_image: batch[0], y_label: batch[1], keep_prob: 1.0})
                print("step%d, train_accury : %g"%(step, train_accury))
            sess.run(train_op, feed_dict={x_image: batch[0], y_label: batch[1], keep_prob:0.5})
            summary_str = sess.run(summary_op, feed_dict={x_image: batch[0], y_label: batch[1], keep_prob: 1.0})
            summary_writer.add_summary(summary_str, step)
            summary_writer.flush()

        print("test accuracy : %g" %sess.run(accur, feed_dict={x_image: mnist.test.images[0:1000], y_label: mnist.test.labels[0:1000], keep_prob: 1.0}))
        network_struct.set_info_by_session(sess)
        network_struct.save(sess, "./tf_ckpt/model.ckpt")
