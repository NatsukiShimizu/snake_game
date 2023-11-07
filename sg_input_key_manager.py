#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class KeyData:
    """キーデータクラス
    """
    ENTER   = 10
    ESC     = 27
    DOWN    = 258
    UP      = 259
    LEFT    = 260
    RIGHT   = 261

class InputKeyManager:
    """キー入力管理クラス
    """
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr

    def getch(self) -> int:
        return self.stdscr.getch()
