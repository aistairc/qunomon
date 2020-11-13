# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
from datetime import datetime, timezone, timedelta


class Timer:
    """
    AITの実行時間を計測するためのクラス。

    Class for measuring the execution time of AIT.
    """

    def __init__(self):
        """
        コンストラクタ

        constructor
        """
        self._start_dt = None
        self._stop_dt = None

    def start_timer(self) -> None:
        """
        タイマーを開始します。

        Start the timer.
        """
        self._start_dt = datetime.now(timezone(timedelta(hours=9)))
        self._stop_dt = None

    def stop_timer(self) -> None:
        """
        タイマーを停止します。

        Stop the timer.
        """
        self._stop_dt = datetime.now(timezone(timedelta(hours=9)))

    def get_start_dt(self) -> datetime:
        """
        開始日時を取得します。

        Get the start date and time.

        Returns:
            start date and time
        """
        return self._start_dt

    def get_stop_dt(self) -> datetime:
        """
        停止日時を取得します。

        Get the stop date and time.

        Returns:
            stop date and time
        """
        return self._stop_dt
