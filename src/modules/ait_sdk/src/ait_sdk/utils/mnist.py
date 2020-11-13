# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
import gzip
import numpy as np


class MNIST:
    """
    MNISTの画像をラベルを読み込むクラスです。

    Class to read labels from MNIST images.
    """

    def load_image(self, file_path: str, image_size: int) -> np.ndarray:
        """
        MNISTの画像を読み込みます。

        Load an MNIST image.

        Args:
            file_path (str) :
                MNISTの画像ファイル(gz)パスを指定します。

                Specify the image file (gz) path for MNIST.

            image_size (str) :
                MNISTの1辺の画像ピクセルサイズを指定します。

                Specifies the image pixel size of one side of MNIST.

        Returns:
            np.ndarray
        """
        with gzip.open(file_path, 'rb') as f:
            data = np.frombuffer(f.read(), np.uint8, offset=16)
        data = data.reshape(-1, image_size, image_size)
        return data

    def load_label(self, file_path: str) -> np.ndarray:
        """
        MNISTのラベルを読み込みます。

        Load an MNIST label.

        Args:
            file_path (str) :
                MNISTのラベルファイル(gz)パスを指定します。

                Specify the label file (gz) path for MNIST.

        Returns:
            np.ndarray
        """
        with gzip.open(file_path, 'rb') as f:
            labels = np.frombuffer(f.read(), np.uint8, offset=8)
        return labels
