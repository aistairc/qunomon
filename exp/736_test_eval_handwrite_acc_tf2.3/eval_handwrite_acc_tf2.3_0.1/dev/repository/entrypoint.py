# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
#!/usr/bin/env python3.6
# coding=utf-8
import sys
from os import path

from ait_sdk.utils.logging import set_log_dir


def main() -> None:
    entrypoint_dir = path.dirname(path.abspath(__file__))
    set_log_dir(entrypoint_dir)
    from my_ait import MyAIT  # ログフォルダを設定後にget_loggerしたいため、遅延import
    ait = MyAIT()
    ait.execute(sys.argv, entrypoint_dir)


if __name__ == '__main__':
    main()
