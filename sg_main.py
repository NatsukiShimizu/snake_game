#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import random
import time

from curses import wrapper
from typing import Any

from sg_game_window import GameWindow
from sg_input_key_manager import KeyData, InputKeyManager
from sg_setting_window import SettingWindow
from sg_snake import Snake
from sg_top_window import MenuState, TopWindow


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
        # インスタンス化
        snake = Snake()
        # 現在のメニュー状態がゲームスタート状態じゃなければ以下の処理をスキップ
        if self.menu_state != MenuState.GAME_START:
            return

        # ゲーム画面を持続させるためのループ
        while True:
            # ヘッダー情報取得
            header = self.game_window.get_header()
            for h in header:
                self.stdscr.addstr(h)

            # コンテンツ情報取得
            main_contents = self.game_window.get_main_contents()
            for y, contents in enumerate(main_contents):
                new_text = ''

                # 1つずつ配列を取り出し、1つの配列の中の1文字を取り出す
                for x, char in enumerate(contents):
                    # 蛇の頭配置判定
                    if x == snake.get_x() and \
                       y == snake.get_y():
                        # new_textに追加することにより空白を文字に置き換える
                        new_text += snake.get_snake_head()
                        continue
                    else:
                        new_text += char

                self.stdscr.addstr(new_text)
            

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
                snake.move_up()
            elif key == KeyData.DOWN:
                snake.move_down()
            elif key == KeyData.RIGHT:
                snake.move_right()
            elif key == KeyData.LEFT:
                snake.move_left()
            elif key == KeyData.ENTER or key == KeyData.ESC:
                # NOTE: [ESC], [Enter]キーで終了
                self.stdscr.nodelay(False)
            # 上記で指定したキー以外が入力されるとここの処理に入る
            else:
                # NOTE: デバック用
                self.stdscr.addstr(f'{key}')

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
            header = self.setting_window.get_header()
            for h in header:
                self.stdscr.addstr(h)

            # コンテンツ情報取得
            main_contents = self.setting_window.get_main_contents()
            for contents in main_contents:
                self.stdscr.addstr(contents)

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