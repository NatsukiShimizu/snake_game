#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from sg_base_window import BaseWindow

class MenuState:
    """ステータスクラス
    """
    CLOSE_APP   = -1
    GAME_START  = 1
    SETTING     = 2

class TopWindow(BaseWindow):
    """トップ画面クラス
       TOP画面ボタン選択状態(1:スタートボタン点滅/2:設定ボタン点滅)
    """    
    def __init__(self, stdscr) -> None:
        """コンストラクタ

        Args:
            stdscr (any): 標準スクリーン
        """
        # TOP画面文字列
        header_list = [
            '\t===============================================\n',
            '\t<<<<            スネークゲーム             >>>>\n',
            '\t===============================================\n',
            '\n'
        ]

        self.selected_game_start_menu = [
            [4, 20, '<-- ゲームスタート -->\n', curses.A_STANDOUT],
            [6, 20, '<--      設定      -->', None]
        ]

        self.selected_setting_menu = [
            [4, 20, '<-- ゲームスタート -->\n', None],
            [6, 20, '<--      設定      -->', curses.A_STANDOUT]
        ]

        # 親クラス呼び出し
        super().__init__(stdscr, header_list, [], [])

    def select_menu(self, menu_state: MenuState) -> list:
        """選択しているメニューをハイライトする

        Args:
            menu_state (MenuState): ステータス情報
        """
        if menu_state == MenuState.GAME_START:
            return self.selected_game_start_menu
        
        else:
            return self.selected_setting_menu
        
