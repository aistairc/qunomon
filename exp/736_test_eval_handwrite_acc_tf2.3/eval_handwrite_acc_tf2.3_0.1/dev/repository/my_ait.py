# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
#!/usr/bin/env python3.6
# coding=utf-8
from typing import List
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, roc_curve, auc, roc_auc_score
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from functools import partial
from pathlib import Path
from scipy import interp
import random
from itertools import cycle
from os import makedirs

from ait_sdk.utils import get_summary_text
from ait_sdk.utils.mnist import MNIST
from ait_sdk.utils.acc_calculator import ACCCalculator
### ↓標準使用モジュール↓
from ait_sdk.develop.ait_base import AITBase
from ait_sdk.utils.logging import get_logger, log
### ↑標準使用モジュール↑


logger = get_logger()

class MyAIT(AITBase):
    
    @log(logger)
    def pre_process(self) -> None:
        """
        実装が必要な関数その1：前処理
        super().pre_process()実施後に独自処理を記載する。
        
        データ読み込みや加工などの前処理を記載する。
        """
        super().pre_process()

        image_px_size = self._ait_input.get_method_param_value('image_px_size')

        # インベントリのMNISTラベル・画像を読み込み
        mnist = MNIST()
        self.X_test = mnist.load_image(self._ait_input.get_inventory_path('test_set_images'), image_px_size)
        self.y_test = mnist.load_label(self._ait_input.get_inventory_path('test_set_labels'))

        # 前処理として、画像を最大値255で割って0.0 - 1.0に規格化
        self.X_test_normalize = self.X_test / 255

        # モデル読み込み
        self.model = tf.keras.models.load_model(self._ait_input.get_inventory_path('trained_model'))
        logger.info(get_summary_text(self.model))


    @log(logger)
    def main_process(self) -> None:
        """
        実装が必要な関数その2：本処理
        super().main_process()実施後に独自処理を記載する。
        
        推論やその結果取得処理を記載する。
        """
        super().main_process()

        # 推論
        self.y_pred = self.model.predict(self.X_test_normalize)

        # 全体精度評価値(measure)
        accuracy, precision, recall, f_measure = self._calc_acc_all(y_test=self.y_test, 
                                                                    y_pred=self.y_pred)
        self._ait_output.add_measure(name='Accuracy', value=str(accuracy))
        self._ait_output.add_measure(name='Precision', value=str(precision))
        self._ait_output.add_measure(name='Recall', value=str(recall))
        self._ait_output.add_measure(name='F−measure', value=str(f_measure))

        # クラス別精度評価値(measure)
        accuracies, precisions, recalls, f_measures = self._calc_acc_by_class(y_test=self.y_test, 
                                                                              y_pred=self.y_pred)
        self._ait_output.add_measure(name='AccuracyByClass', value=','.join(map(str,accuracies)))
        self._ait_output.add_measure(name='PrecisionByClass', value=','.join(map(str,precisions)))
        self._ait_output.add_measure(name='RecallByClass', value=','.join(map(str,recalls)))
        self._ait_output.add_measure(name='F−measureByClass', value=','.join(map(str,f_measures)))

        # 混同行列(CSV)
        item_name='ConfusionMatrixCSV'
        file_path = self._path_helper.get_output_resource_path(item_name)
        self._save_confusion_matrix_csv(file_path=file_path, 
                                        y_test=self.y_test, 
                                        y_pred=self.y_pred)
        self._ait_output.add_resource(name=item_name, path=file_path)

        # 混同行列(PNG)
        item_name='ConfusionMatrixHeatmap'
        file_path = self._path_helper.get_output_resource_path(item_name)
        self._save_confusion_matrix_heatmap(file_path=file_path, 
                                            y_test=self.y_test, 
                                            y_pred=self.y_pred)
        self._ait_output.add_resource(name=item_name, path=file_path)

        # ROC曲線(PNG)
        item_name='ROC-curve'
        file_path = self._path_helper.get_output_resource_path(item_name)
        self._save_roc_curve(file_path=file_path, 
                             y_test=self.y_test, 
                             y_pred=self.y_pred, 
                             n_classes= self._ait_input.get_method_param_value('class_count'))
        self._ait_output.add_resource(name=item_name, path=file_path)

        # AUC(measure)
        item_name='AUC'
        value = self._calc_auc(y_test=self.y_test, 
                               y_pred=self.y_pred,
                               multi_class=self._ait_input.get_method_param_value('auc_multi_class'),
                               average=self._ait_input.get_method_param_value('auc_average'))
        self._ait_output.add_measure(name=item_name, value=str(value))

        # NG画像(PNG)
        item_name='NGPredictImages'
        file_path = self._path_helper.get_output_resource_path(item_name)
        out_files = self._save_ng_predicts(file_path=file_path, 
                                           X_test=self.X_test,
                                           y_test=self.y_test, 
                                           y_pred=self.y_pred, 
                                           n_classes= int(self._ait_input.get_method_param_value('class_count')))
        for out_file in out_files:
            self._ait_output.add_resource(name=item_name, path=out_file)

        # log(Text)
        item_name='Log'
        file_path = self._path_helper.get_output_download_path(item_name)
        self._ait_output.add_downloads(name=item_name, path=file_path)

        # PredictionResult(CSV)
        item_name='PredictionResult'
        file_path = self._path_helper.get_output_download_path(item_name)
        self._save_prediction_result(file_path=file_path, 
                                     y_test=self.y_test, 
                                     y_pred=self.y_pred)
        self._ait_output.add_downloads(name=item_name, path=file_path)

    @log(logger)
    def _calc_acc_all(self, y_test, y_pred) -> (float, float, float, float):
        calc = ACCCalculator()
        one_hot_y = to_categorical(y_test)

        return calc.average_accuracy(one_hot_y, y_pred).numpy() , \
               calc.macro_precision(one_hot_y, y_pred).numpy() , \
               calc.macro_recall(one_hot_y, y_pred).numpy() , \
               calc.macro_f_measure(one_hot_y, y_pred).numpy()

    def _calc_acc_by_class(self, y_test, y_pred) -> (List[float], List[float], List[float], List[float]):
        calc = ACCCalculator()
        one_hot_y = to_categorical(y_test)

        return calc.all_class_accuracy(one_hot_y, y_pred) , \
               [v.numpy() for v in calc.all_class_precision(one_hot_y, y_pred)] , \
               [v.numpy() for v in calc.all_class_recall(one_hot_y, y_pred)] , \
               [v.numpy() for v in calc.all_class_f_measure(one_hot_y, y_pred)]

    @log(logger)
    def _save_confusion_matrix_csv(self, file_path: str, y_test, y_pred) -> None:
        makedirs(str(Path(file_path).parent), exist_ok=True)

        cmx_data = confusion_matrix(y_test, K.argmax(y_pred))
        logger.info(cmx_data)
        np.savetxt(file_path, cmx_data, fmt='%d', delimiter=',')

    @log(logger)
    def _save_confusion_matrix_heatmap(self, file_path: str, y_test, y_pred) -> None:
        makedirs(str(Path(file_path).parent), exist_ok=True)

        y_pred = K.argmax(y_pred)

        labels = sorted(list(set(y_test)))
        cmx_data = confusion_matrix(y_test, y_pred, labels=labels)

        df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

        fig = plt.figure(dpi=100, figsize=(8,6))
        sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('Predicted class')
        ax.set_ylabel('Actual class')
        ax.set_title('Plot of Confusion Matrix')

        # save as png
        plt.savefig(file_path)

    @log(logger)
    def _save_roc_curve(self, file_path: str, y_test, y_pred, n_classes: int) -> None:
        makedirs(str(Path(file_path).parent), exist_ok=True)

        y_true = to_categorical(y_test)
        y_score = y_pred

        fpr = dict()
        tpr = dict()
        roc_auc = dict()

        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(y_true.ravel(), y_score.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

        # Compute ROC curve and ROC area for each class
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_true[:, i], y_score[:, i], drop_intermediate=False)
            roc_auc[i] = auc(fpr[i], tpr[i])

        # First aggregate all false positive rates
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

        # Then interpolate all ROC curves at this points
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += interp(all_fpr, fpr[i], tpr[i])

        # Finally average it and compute AUC
        mean_tpr /= n_classes

        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

        # Plot all ROC curves
        plt.figure(dpi=100, figsize=(8,6))
        plt.plot(fpr["micro"], tpr["micro"],
                label='micro-average ROC curve (area = {0:0.2f})'
                    ''.format(roc_auc["micro"]),
                color='deeppink', linestyle=':', linewidth=4)

        plt.plot(fpr["macro"], tpr["macro"],
                label='macro-average ROC curve (area = {0:0.2f})'
                    ''.format(roc_auc["macro"]),
                color='navy', linestyle=':', linewidth=4)

        colors = cycle(['#1f77b4',
                        '#ff7f0e',
                        '#2ca02c',
                        '#d62728',
                        '#9467bd',
                        '#8c564b',
                        '#e377c2',
                        '#7f7f7f',
                        '#bcbd22',
                        '#17becf'])

        #colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
        for i, color in zip(range(n_classes), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=2,
                    label='ROC curve of class {0} (area = {1:0.2f})'
                    ''.format(i, roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Some extension of Receiver operating characteristic to multi-class')
        plt.legend(loc="lower right")
        plt.savefig(file_path)

    @log(logger)
    def _calc_auc(self, y_test, y_pred, multi_class: str, average: str) -> float:
        y_true = to_categorical(y_test)
        y_score = y_pred

        return roc_auc_score(y_true, y_score,
                             multi_class=multi_class,
                             average=average)

    @log(logger)
    def _save_ng_predicts(self, file_path: str, X_test, y_test, y_pred, n_classes: int) -> List[str]:
        makedirs(str(Path(file_path).parent), exist_ok=True)

        out_files = []
        y_true = y_test
        y_pred = K.argmax(y_pred)

        # unmach_classes={label:[{predict: index}] }
        unmach_classes={}
        for actual_class_no in range(n_classes):
            unmach_classes[actual_class_no] = {}
            for predict_class_no in range(n_classes):
                unmach_classes[actual_class_no][predict_class_no] = []

        for i in range(y_pred.shape[-1]):
            if y_true[i] != y_pred[i].numpy():
                unmach_classes[y_true[i]][y_pred[i].numpy()].append(i)

        # visualization
        def draw_digit(data, row, col, n, index) -> None:
            ax = plt.subplot(row, col, n)
            ax.axis("off")
            ax.set_title(str(index))
            plt.imshow(data, cmap = "gray")

        def draw_text(text, row, col, n) -> None:
            ax = plt.subplot(row, col, n)
            ax.axis("off")

            # build a rectangle in axes coords
            left, width = .25, .5
            bottom, height = .25, .5
            right = left + width
            top = bottom + height
            ax.text(0.5*(left+right), 0.5*(bottom+top), text,
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=12, color='black',
                transform=ax.transAxes)

        show_size = 10 + 1
        for actual_class_no in range(n_classes):
            fig = plt.figure(figsize=(n_classes,show_size))
            fig.suptitle('actual class.{}'.format(actual_class_no), fontsize=20)
            unmachies = unmach_classes[actual_class_no]
            for predict_class_no in range(n_classes):
                indexes = unmach_classes[actual_class_no][predict_class_no]
                offset = predict_class_no * show_size + 1
                draw_text('predict\nclass\n{}'.format(predict_class_no), n_classes, show_size, offset)

                image_count = 0
                for index in indexes:
                    offset += 1
                    draw_digit(X_test[index], n_classes, show_size, offset, index)
                    # 11枚分以上は読み捨て
                    image_count += 1
                    if image_count >= 10:
                        break

            out_file = file_path.format(actual_class_no)
            out_files.append(out_file)
            plt.savefig(out_file)

        return out_files

    @log(logger)
    def _save_prediction_result(self, file_path: str, y_test, y_pred) -> None:
        makedirs(str(Path(file_path).parent), exist_ok=True)

        # Label + PredictProva
        out_data = np.hstack([y_test.reshape(y_test.shape[0], 1), y_pred])

        index = [str(i) for i in range(1, y_test.shape[0]+1)]
        columns = ['Label']+[f'PredictionProva_Class_{i}' for i in range(1,y_pred.shape[1]+1)]
        df = pd.DataFrame(data=out_data, index=index, columns=columns, dtype='float')

        df.to_csv(file_path)

    @log(logger)
    def post_process(self) -> None:
        """
        実装が必要な関数その3：後処理
        super().post_process()実施後に独自処理を記載する。

        後始末の処理を記載する。
        """
        super().post_process()

    def clean_up(self) -> None:
        """
        最終処理を実装する。
        super().post_process()実施前に独自処理を記載する。
        ログファイルのコピー処理などの後始末をするため、logデコレーションしない。
        """
        super().clean_up()
