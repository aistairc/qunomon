#!/bin/bash
#******************************************************************************************
# Copyright (c) 2019 Hitachi, Ltd.
# All rights reserved. This program and the accompanying materials are made available under
# the terms of the MIT License which accompanies this distribution, and is available at
# https://opensource.org/licenses/mit-license.php
#
# March 1st, 2019 : First version.
#******************************************************************************************
pip install --upgrade pip
conda create -n neuron_coverage_tensorflow_native python=3.6 -y
source activate neuron_coverage_tensorflow_native
pip install bleach==1.5.0
pip install cycler==0.10.0
pip install decorator==4.1.2
pip install h5py==2.9.0
pip install html5lib==0.9999999
pip install Keras==2.0.8
pip install Markdown==2.6.9
pip install matplotlib==2.0.2
pip install networkx==1.11
pip install numpy==1.13.1
pip install olefile==0.44
pip install pandas==0.20.3
pip install Pillow==4.2.1
pip install protobuf==3.4.0
pip install pyparsing==2.2.0
pip install python-dateutil==2.6.1
pip install pytz==2017.2
pip install PyWavelets==0.5.2
pip install PyYAML==3.12
pip install scikit-image==0.14.2
pip install scikit-learn==0.19.0
pip install scipy==0.19.1
pip install six==1.11.0
pip install tensorflow==1.12.0
pip install tensorflow-tensorboard==0.1.6
pip install Werkzeug==0.12.2
