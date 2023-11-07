#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sg_base_window import BaseWindow

class SettingWindow(BaseWindow):
    """設定画面クラス
    """
    def __init__(self, stdscr) -> None:
        """コンストラクタ

        Args:
            stdscr (any): 標準スクリーン
        """
        # 設定画面文字列
        header_list = [
            '\n',
            '\n',
            '\t<<<<                 設定                  >>>>\n'
        ]

        main_contents_list = [
            '\t-----------------------------------------------\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t-----------------------------------------------\n'
        ]

        # 親クラス呼び出し
        super().__init__(stdscr, header_list, main_contents_list, [])
