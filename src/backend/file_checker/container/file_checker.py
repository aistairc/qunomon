# Copyright c 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
import hashlib
import json
from pathlib import Path
import sys
import magic


HOME_DIR = '/usr/local/qai'
INPUT_DIR = HOME_DIR+'/input'
OUTPUT_DIR = HOME_DIR+'/output'


def calc_file_hash_sha256(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def output_json(json_data, id_: str):
    output_dir = OUTPUT_DIR+f'/inventory_check/{id_}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(output_dir+'/result.json', mode='wt', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)


def main(file_name: str, id_: str):
    result = {
        'exists': False,
        'is_directory': False,
        'hash_sha256': '',
        'mime_type': '',
    }

    # インプットファイル存在チェック
    file_path = Path(INPUT_DIR) / file_name
    if not file_path.exists():
        output_json(result, id_)
        return
    result['exists'] = True

    # フォルダの場合、以降の処理をスキップ
    if file_path.is_dir():
        result['is_directory'] = True
        output_json(result, id_)
        return

    result['hash_sha256'] = calc_file_hash_sha256(str(file_path))

    # get mime_type
    with magic.Magic() as m:
        result['mime_type'] = m.from_file(str(file_path))

    output_json(result, id_)
    return


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: file_checker.py {file_name} {id}')
    else:
        main(sys.argv[1], sys.argv[2])
