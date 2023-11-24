# Copyright c 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
#!/usr/bin/env python3.6
# coding=utf-8
import os
import requests
import time
from pprint import pprint
from pathlib import Path

from ait_sdk.test.hepler import Helper
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


backend_entry_point = 'https://host.docker.internal:443/qai-testbed/api/0.0.1'
ip_entry_point = 'https://host.docker.internal:443/qai-ip/api/0.0.1'
AIT_DIR='./ait'
WAIT_LIMIT=100


def get_zippath(basedir):
	# ディレクトリ配下のzipファイルパスとファイル名(拡張子なし)を取得
	for file in os.listdir(basedir):
		_ , ext = os.path.splitext(file)
		if ext == '.zip':
			return basedir+'/'+file
	return 'none'

def main():
    helper = Helper(backend_entry_point=backend_entry_point, 
                    ip_entry_point=ip_entry_point,
                    ait_dir=AIT_DIR,
                    ait_full_name='dummy')

    for i in range(WAIT_LIMIT):
        try:
            print(f'WAIT backend service start...[{i}]')
            response_bk=helper.get_bk('/health-check', is_print_json=False)
            response_ip=helper.get_ip('/health-check', is_print_json=False)
            if response_bk.status_code == 200 and response_ip.status_code == 200:
                break
        except Exception as e:
            print(e)
        finally:
            time.sleep(3)

    if i==WAIT_LIMIT-1:
        print('ERROR: Backend and integration-provider is not started.')
        return -1

    files = os.listdir(AIT_DIR)
    dirs = [f for f in files if os.path.isdir(os.path.join(AIT_DIR, f))]

    print(f'install targets:{dirs}')

    for dir in dirs:
        try:
            print(f'start install:{dir}')

            json_path = AIT_DIR+'/'+dir+'/'+'ait.manifest.json'

            if os.path.isfile(json_path)==False:
                raise Exception("ERROR: file not found. ({})".format(json_path))

            print(f'post_manifest:{json_path}')
            response = helper.post_manifest(json_path)
            if response.status_code != 200:
                # 重複登録以外のエラーは処理を中断
                if not (response.status_code == 400 and response.json()['Code'] == 'A01400'):
                    raise Exception("ERROR: "+str(response))

            print(f'complete install:{dir}')
        except Exception as e:
            print(e)
            print("Registration failure. ({})".format(dir))
            return -1

if __name__ == '__main__':
    main()