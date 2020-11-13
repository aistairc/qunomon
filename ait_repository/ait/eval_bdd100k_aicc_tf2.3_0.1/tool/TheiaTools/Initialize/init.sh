#!/bin/bash

theia_setting_src_dir="/home/project/TheiaTools/.theia"
theia_setting_dst_dir="/home/project"
echo "<<START copy theia_setting>>"
cp -rf ${theia_setting_src_dir} ${theia_setting_dst_dir}
echo "<<END copy theia_setting>>"

repo_dir="/home/project/deploy/container/repository/"
requirements_file="requirements.txt"
echo "<<START pip install>>"
cd ${repo_dir}
pip3 install -r ${requirements_file}
echo "<<END pip install>>"


apt update && apt install -y python3-pip
apt-get update
apt-get install gcc make -y
apt-get install python-lxml -y
apt-get install python-dev libxml2 libxml2-dev libxslt-dev curl -y

export PYTHONPATH=$PYTHONPATH:/tensorflow/models/research:/tensorflow/

echo "<<START protoc install>>"
cd /tmp
apt-get install -y unzip
curl -OL https://github.com/google/protobuf/releases/download/v3.9.0/protoc-3.9.0-linux-x86_64.zip
unzip -d protoc3 protoc-3.9.0-linux-x86_64.zip
mv protoc3/bin/* /usr/local/bin/
mv protoc3/include/* /usr/local/include/
rm -rf protoc-3.9.0-linux-x86_64.zip protoc3
echo "<<END protoc install>>"

echo "<<START cocoapi install>>"
apt-get install git -y
git clone https://github.com/cocodataset/cocoapi.git
cd /tmp/cocoapi/PythonAPI
python3 setup.py build_ext --inplace
rm -rf build
python3 setup.py build_ext install
rm -rf build
echo "<<END cocoapi install>>"

echo "<<START tensorflow_model install>>"
mkdir -p /tensorflow
cd /tensorflow
git clone https://github.com/tensorflow/models.git
cd /tensorflow/models/research
protoc object_detection/protos/*.proto --python_out=.
echo "<<END tensorflow_model install>>"


exit 0