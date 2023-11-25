#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

class Music:
    """ミュージッククラス
    """
    def play_music(self):
        """音楽再生
        """
        try:
            subprocess.call(["./start_bgm.sh"])

        except Exception as e:
            print(f'{e}')

    def stop_music(self):
        """音楽停止
        """
        subprocess.call(["pkill", "-KILL", "-f", "ffplay"])
