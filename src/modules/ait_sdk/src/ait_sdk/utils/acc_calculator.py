# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

import keras.backend as K
import numpy as np


class ACCCalculator:
    """
    精度を計算する

    accuracy calculator
    """

    def normalize_y_pred(self, y_pred):
        return K.one_hot(K.argmax(y_pred), y_pred.shape[-1])

    def class_true_positive(self, class_label, y_true, y_pred):
        y_pred = self.normalize_y_pred(y_pred)
        return K.cast(K.equal(y_true[:, class_label] + y_pred[:, class_label], 2),
                    K.floatx())

    def true_positive(self, y_true, y_pred):
        y_pred = self.normalize_y_pred(y_pred)
        return K.cast(K.equal(y_true + y_pred, 2),
                    K.floatx())

    def class_precision(self, class_label, y_true, y_pred):
        y_pred = self.normalize_y_pred(y_pred)
        return K.sum(self.class_true_positive(class_label, y_true, y_pred)) / (K.sum(y_pred[:, class_label]) + K.epsilon())

    def micro_precision(self, y_true, y_pred):
        y_pred = self.normalize_y_pred(y_pred)
        return K.sum(self.true_positive(y_true, y_pred)) / (K.sum(y_pred) + K.epsilon())

    def all_class_precision(self, y_true, y_pred):
        return [self.class_precision(i, y_true, y_pred) for i in range(y_pred.shape[-1])]

    def macro_precision(self, y_true, y_pred):
        class_count = y_pred.shape[-1]
        return K.sum([self.class_precision(i, y_true, y_pred) for i in range(class_count)]) \
            / K.cast(class_count, K.floatx())

    def class_recall(self, class_label, y_true, y_pred):
        return K.sum(self.class_true_positive(class_label, y_true, y_pred)) / (K.sum(y_true[:, class_label]) + K.epsilon())

    def micro_recall(self, y_true, y_pred):
        return K.sum(self.true_positive(y_true, y_pred)) / (K.sum(y_true) + K.epsilon())

    def all_class_recall(self, y_true, y_pred):
        return [self.class_recall(i, y_true, y_pred) for i in range(y_pred.shape[-1])]

    def macro_recall(self, y_true, y_pred):
        class_count = y_pred.shape[-1]
        return K.sum([self.class_recall(i, y_true, y_pred) for i in range(class_count)]) \
            / K.cast(class_count, K.floatx())

    def class_accuracy(self, class_label, y_true, y_pred):
        y_pred = self.normalize_y_pred(y_pred)
        return K.cast(K.equal(y_true[:, class_label], y_pred[:, class_label]),
                    K.floatx())

    def all_class_accuracy(self, y_true, y_pred):
        return [np.mean(self.class_accuracy(i, y_true, y_pred)) for i in range(y_pred.shape[-1])]

    def average_accuracy(self, y_true, y_pred):
        class_count = y_pred.shape[-1]
        class_acc_list = [self.class_accuracy(i, y_true, y_pred) for i in range(class_count)]
        class_acc_matrix = K.concatenate(class_acc_list, axis=0)
        return K.mean(class_acc_matrix, axis=0)

    def class_f_measure(self, class_label, y_true, y_pred):
        precision = self.class_precision(class_label, y_true, y_pred)
        recall = self.class_recall(class_label, y_true, y_pred)
        return (2 * precision * recall) / (precision + recall + K.epsilon())

    def all_class_f_measure(self, y_true, y_pred):
        return [self.class_f_measure(i, y_true, y_pred) for i in range(y_pred.shape[-1])]

    def micro_f_measure(self, y_true, y_pred):
        precision = self.micro_precision(y_true, y_pred)
        recall = self.micro_recall(y_true, y_pred)
        return (2 * precision * recall) / (precision + recall + K.epsilon())

    def macro_f_measure(self, y_true, y_pred):
        precision = self.macro_precision(y_true, y_pred)
        recall = self.macro_recall(y_true, y_pred)
        return (2 * precision * recall) / (precision + recall + K.epsilon())
