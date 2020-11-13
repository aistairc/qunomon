# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

import shutil
from pathlib import Path
from nbconvert.exporters import PythonExporter, export
from nbformat import read, NO_CONVERT

from ..common.files.ait_manifest import AITManifest


def prepare_deploy(ait_manifest: AITManifest, ait_sdk_name: str, base_dir: str, requirements_path: str,
                   is_remote_deploy: bool = False):
    """
    デプロイ準備をします。

    Prepare for deployment.

    Args:
        ait_manifest (AITManifest) :
            ait_manifestを指定します。

            Specify the ait_manifest.

        ait_sdk_name (str) :
            ait_sdk_nameを指定します。

            Specify ait_sdk_name.

        base_dir (str) :
            基点フォルダパスを指定します。

            Specifies the base folder path.

        requirements_path (str) :
            requirements_pathを指定します。

            Specify requirements_path.

        is_remote_deploy (bool) :
            aitのコンテナイメージをリモートから取得するか、ローカルでビルドするかを指定します。

            Specifies whether the ait container image should be obtained remotely or built locally.

    """
    base_path = Path(base_dir)

    # convert my_ait.py
    exporter = PythonExporter()
    with open(str(base_path/'my_ait.ipynb'), encoding='utf-8') as f:
        nb = read(f, NO_CONVERT)
        result = export(exporter, nb)

    with open(str(base_path/'my_ait.py'), mode='w', encoding='utf-8') as f:
        f.write(result[0])

    # move to deploy dir
    shutil.move(str(base_path/'my_ait.py'),
                str(base_path/'../deploy/container/repository/my_ait.py'))

    # copy ait.manifest to deploy dir
    shutil.copyfile(str(base_path/'ait.manifest.json'),
                    str(base_path/'../deploy/container/repository/ait.manifest.json'))

    # copy ait-sdk to deploy dir
    shutil.copyfile(str(base_path/f'./{ait_sdk_name}'),
                    str(base_path/f'../deploy/container/repository/{ait_sdk_name}'))

    # copy requirements to deploy dir
    requirements_file_name = Path(requirements_path).name
    shutil.copyfile(requirements_path,
                    str(base_path/f'../deploy/container/repository/{requirements_file_name}'))

    if is_remote_deploy:
        keyword = 'remote'
    else:
        keyword = 'local'

    # dag deploy
    src_file = str(base_path/f'../template/dag_{keyword}.py')
    dst_file = str(base_path/'../deploy/dag.py')
    shutil.copyfile(src_file, dst_file)
    _replace_template(ait_manifest.get_name(), ait_manifest.get_version(), dst_file, 'utf-8')

    # deploy script
    src_file = str(base_path/f'../template/docker_deploy_{keyword}.bat')
    dst_file = str(base_path/'../tool/docker_deploy.bat')
    shutil.copyfile(src_file, dst_file)
    _replace_template(ait_manifest.get_name(), ait_manifest.get_version(), dst_file, 'shift-jis')

    # license dockerfile
    src_file = str(base_path/f'../template/dockerfile_license')
    dst_file = str(base_path/'../deploy/container/dockerfile_license')
    shutil.copyfile(src_file, dst_file)
    _replace_template(ait_manifest.get_name(), ait_manifest.get_version(), dst_file, 'utf-8')

    # license script
    src_file = str(base_path/f'../template/generate_thirdparty_notices.bat')
    dst_file = str(base_path/'../tool/generate_thirdparty_notices.bat')
    shutil.copyfile(src_file, dst_file)
    _replace_template(ait_manifest.get_name(), ait_manifest.get_version(), dst_file, 'shift-jis')


def _replace_template(ait_name, ait_version, dst_file, encoding):
    with open(dst_file, encoding=encoding) as f:
        data_lines = f.read()
    data_lines = data_lines.replace('{AIT_NAME}', ait_name)
    data_lines = data_lines.replace('{AIT_VERSION}', ait_version)
    with open(dst_file, mode='w', encoding=encoding, newline="\r\n") as f:
        f.write(data_lines)
