#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import curses
import random
import time
from curses import wrapper
from typing import Any
from sg_base_window import BaseWindow

class SnakeGame:
    """スネークゲームクラス
    """
    def __init__(self, stdscr) -> None:
        """コンストラクタ
            コンストラクタ：クラス内で使う変数を定義するため
            NOTE:この関数を引数として[wrapper]関数に渡す必要がある

        Args:
            stdscr (obj): 標準画面出力インスタンス
                    NOTE:ターミナルに何かを表示するためにこの引数が必要
                        stdscrの引数を使って色々と画面に表示するものを作る
        """
        if stdscr is None:
            raise Exception()

        self.stdscr         = stdscr
        self.input_key_mng  = InputKeyManager(stdscr)
        self.top_window     = TopWindow(stdscr)
        self.game_window    = GameWindow(stdscr)
        self.setting_window = SettingWindow(stdscr)
        self.menu_state     = MenuState.GAME_START
        # self.stdscr = WindowManager(stdscr)
        # self.window_state = WindowState.GAME_WINDOW

    def initialise(self) -> None:
        """初期化処理
        """
        # カーソルを不可視に設定
        curses.curs_set(0)
        # 標準出力画面の情報をクリアする
        self.stdscr.clear()

    def main(self) -> None:
        """メイン処理
        """
        try:
            # アプリ機能を持続させるためのループ
            while True:
                # TOP画面のヘッダー情報取得
                self.top_window_proc()
                # ゲーム画面のヘッダー情報取得
                self.game_window_proc()
                # 設定画面のヘッダー情報取得
                self.setting_window_proc()

                if self.menu_state == MenuState.CLOSE_APP:
                    break

        except curses.error:
            pass
            # curses.beep()

        except KeyboardInterrupt:
            pass

    def top_window_proc(self) -> None:
        """トップ画面処理
        """
        # トップ画面を持続させるためのループ
        while True:
            # TOP画面のヘッダー情報取得
            top_header = self.top_window.get_header()
            for header in top_header:
                self.stdscr.addstr(header)

            # TOP画面のメニュー情報取得
            top_menu = self.top_window.select_menu(self.menu_state)
            for menu in top_menu:
                if menu[3] is None:
                    self.stdscr.addstr(menu[0], menu[1], menu[2])
                
                else:
                    self.stdscr.addstr(menu[0], menu[1], menu[2], menu[3])

            # 画面更新
            self.stdscr.refresh()
            key = self.input_key_mng.getch()

            # エンター入力で
            if key == KeyData.ENTER:
                # TOP画面を終了
                # 標準出力画面の情報をクリアする
                self.stdscr.clear()
                break
            elif key == KeyData.UP:
                self.menu_state = MenuState.GAME_START
            elif key == KeyData.DOWN:
                self.menu_state = MenuState.SETTING
            elif key == KeyData.ESC:
                self.menu_state = MenuState.CLOSE_APP
                # 標準出力画面の情報をクリアする
                self.stdscr.clear()
                break
            else:
                pass

            # 標準出力画面の情報をクリアする
            self.stdscr.clear()

    def game_window_proc(self) -> None:
        """ゲーム画面処理
        """
        # 現在のメニュー状態がゲームスタート状態じゃなければ以下の処理をスキップ
        if self.menu_state != MenuState.GAME_START:
            return

        # ゲーム画面を持続させるためのループ
        while True:
            # ヘッダー情報取得
            top_header = self.game_window.get_header()
            for header in top_header:
                self.stdscr.addstr(header)

            # コンテンツ情報取得
            main_contents = self.game_window.get_main_contents()
            for contents in main_contents:
                self.stdscr.addstr(contents)

            # 画面更新
            self.stdscr.refresh()
            key = self.input_key_mng.getch()

            # エンター/esc入力
            if key == KeyData.ENTER or key == KeyData.ESC:
                # ゲーム画面を終了
                # 標準出力画面の情報をクリアする
                self.stdscr.clear()
                break
            elif key == KeyData.UP:
                pass
            elif key == KeyData.DOWN:
                pass
            else:
                pass

            # 標準出力画面の情報をクリアする
            self.stdscr.clear()
    
    def setting_window_proc(self) -> None:
        """設定画面処理
        """
        # 現在のメニュー状態が設定状態じゃなければ以下の処理をスキップ
        if self.menu_state != MenuState.SETTING:
            return
        
        # 設定画面を持続させるためのループ
        while True:
            # ヘッダー情報取得
            top_header = self.setting_window.get_header()
            for header in top_header:
                self.stdscr.addstr(header)

            # 画面更新
            self.stdscr.refresh()
            key = self.input_key_mng.getch()

            # エンター/esc入力
            if key == KeyData.ENTER or key == KeyData.ESC:
                # 設定画面を終了
                # 標準出力画面の情報をクリアする
                self.stdscr.clear()
                break
            elif key == KeyData.UP:
                pass
            elif key == KeyData.DOWN:
                pass
            else:
                pass

            # 標準出力画面の情報をクリアする
            self.stdscr.clear()

class KeyData:
    """キーデータクラス
    """
    ENTER = 10
    ESC = 27
    DOWN = 258
    UP = 259
    LEFT = 260
    RIGHT = 261

class InputKeyManager:
    """キー入力管理クラス
    """
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr

    def getch(self) -> int:
        return self.stdscr.getch()

class Speed:
    """ゲーム速度クラス
    """
    pass

class Food:
    """蛇の餌クラス
    """
    pass

class Snake:
    """蛇クラス
    """
    pass

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
            [5, 20, '<--      設定      -->', None]
        ]

        self.selected_setting_menu = [
            [4, 20, '<-- ゲームスタート -->\n', None],
            [5, 20, '<--      設定      -->', curses.A_STANDOUT]
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

        

class GameWindow(BaseWindow):
    """ゲーム画面クラス
    """
    def __init__(self, stdscr) -> None:
        """コンストラクタ

        Args:
            stdscr (any): 標準スクリーン
        """
        # ゲーム画面文字列
        header_list = [
            '\n',
            '\n',
            '\t<<<<            スネークゲーム             >>>>\n'
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

        footer_list = [
            '\n',
            '\t\t<--      上移動 ↑ キー     -->\n',
            '\t\t<--      下移動 ↓ キー     -->\n',
            '\t\t<--      左移動 ← キー     -->\n',
            '\t\t<--      右移動 → キー     -->\n',
            '\t\t<--     ESC,Enterで終了    -->\n',
            '\n'
        ]

        self.game_over_list = [
            '\t-----------------------------------------------\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                  GAME OVER                  |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t|                                             |\n',
            '\t-----------------------------------------------\n'
        ]

        # 親クラス呼び出し
        super().__init__(stdscr, header_list, main_contents_list, footer_list)

    def get_game_over_wnd(self) -> list:
        """ゲーム画面のゲームオーバー情報を取得する

        Returns:
            list: ゲーム画面のゲームオーバー情報
        """
        return self.game_over_list

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

        # 親クラス呼び出し
        super().__init__(stdscr, header_list, [], [])


class WindowManager:
    """画面管理クラス
    """
    def __init__(self, stdscr) -> None:
        """コンストラクタ

        Args:
            stdscr (any): 標準スクリーン
        """
        self.stdscr = stdscr

    def addstr(self, text:str, arg = None) -> None:
        """画面出力文字の追加

        Args:
            text (str): 画面出力文字
        """
        if arg is None:
            self.stdscr.addstr(text)
        
        else:
            self.stdscr.addstr(text, arg)

    def refresh(self) -> None:
        """画面を更新
        """
        

    def clear(self) -> None:
        """画面をクリア
        """
        

def main(stdscr):
    ## インスタンス生成 ###
    snake_game = SnakeGame(stdscr)
    ### 初期化処理 ###
    snake_game.initialise()
    snake_game.main()


if __name__ == "__main__":
    # 以下のwrapper関数は必ず呼び出す必要がある
    try:
        wrapper(main)
    except curses.error:
        print('異常終了')
    print('終了')