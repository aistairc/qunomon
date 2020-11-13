# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
#!/usr/bin/env python3.6
# coding=utf-8
import sys
from os import path
import subprocess

from ait_sdk.utils.logging import set_log_dir


def main() -> None:
    entrypoint_dir = path.dirname(path.abspath(__file__))
    set_log_dir(entrypoint_dir)
    subprocess.call(['python3', f'{entrypoint_dir}/my_ait.py', sys.argv[1]])


if __name__ == '__main__':
    main()
