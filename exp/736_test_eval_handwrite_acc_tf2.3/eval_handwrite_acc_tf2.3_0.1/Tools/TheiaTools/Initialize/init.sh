#!/bin/bash

theia_setting_src_dir="/home/project/TheiaTools/.theia"
theia_setting_dst_dir="/home/project"
echo "<<START copy theia_setting>>"
cp -rf ${theia_setting_src_dir} ${theia_setting_dst_dir}
echo "<<END copy theia_setting>>"

repo_dir="/home/project/dev/repository/"
requirements_file="requirements.txt"
echo "<<START pip install>>"
cd ${repo_dir}
pip3 install -r ${requirements_file}
echo "<<END pip install>>"

exit 0