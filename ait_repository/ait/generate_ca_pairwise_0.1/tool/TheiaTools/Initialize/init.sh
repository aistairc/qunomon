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

echo "<<START PICT install>>"
cd ${repo_dir}
apt-get update
apt-get -y install build-essential git
git clone https://github.com/microsoft/pict.git
cd pict
make
echo "<<END PICT install>>"

exit 0