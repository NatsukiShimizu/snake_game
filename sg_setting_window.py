#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from sg_base_window import BaseWindow

class SubMenuState:
    """ステータスクラス
    """
    SPEED   = 0
    KEYBOARD  = 1
    AUDIO     = 2

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
            '\t===============================================\n',
            '\t<<<<                 設定                  >>>>\n',
            '\t===============================================\n',
            '\n'
        ]

        self.selected_game_speed_menu = [
            [4, 20, '<-- ゲーム速度 -->\n',curses.A_STANDOUT],
            [6, 20, '<-- キーボード -->\n', None],
            [8, 20, '<-- オーディオ -->\n', None]
        ]

        self.selected_game_keyboard_menu = [
            [4, 20, '<-- ゲーム速度 -->\n', None],
            [6, 20, '<-- キーボード -->\n',curses.A_STANDOUT],
            [8, 20, '<-- オーディオ -->\n', None]
        ]

        self.selected_game_audio_menu = [
            [4, 20, '<-- ゲーム速度 -->\n', None],
            [6, 20, '<-- キーボード -->\n', None],
            [8, 20, '<-- オーディオ -->\n',curses.A_STANDOUT]
        ]

        # 親クラス呼び出し
        super().__init__(stdscr, header_list, [], [])

    def select_menu(self, menu_state: SubMenuState) -> list:
        """選択しているメニューをハイライトする

        Args:
            menu_state (SubMenuState): ステータス情報
        """
        if menu_state == SubMenuState.SPEED:
            return self.selected_game_speed_menu
        
        elif menu_state == SubMenuState.KEYBOARD:
            return self.selected_game_keyboard_menu

        else:
            return self.selected_game_audio_menu