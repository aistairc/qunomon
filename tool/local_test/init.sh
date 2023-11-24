#!/bin/bash

repo_dir="/workdir/root/deploy/container/repository/"
requirements_file="requirements.txt"
echo "<<START pip install>>"
cd ${repo_dir}
pip3 install -r ${requirements_file}
echo "<<END pip install>>"

exit 0
