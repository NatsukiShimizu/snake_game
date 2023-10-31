#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import random
import copy
import time
from curses import wrapper

def main(stdscr) -> None:
    ### インスタンス生成 ###
    snake_game = SnakeGame(stdscr)
    ### 初期化処理 ###
    snake_game.initialise()

class SnakeGame:
    """スネークゲームクラス
    """
    def __init__(self, stdscr) -> None:
        """コンストラクタ
            NOTE:この関数を引数として[wrapper]関数に渡す必要がある

        Args:
            stdscr (obj): 標準画面出力インスタンス
                    NOTE:ターミナルに何かを表示するためにこの引数が必要
                        stdscrの引数を使って色々と画面に表示するものを作る
        """
        if stdscr is None:
            raise Exception()

        self.stdscr = stdscr
        self.top_window = TopWindow()

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
                top_header = self.top_window.get_header()
                for header in top_header:
                    self.stdscr.addstr(header)

                # TOP画面のメニュー情報取得
                top_menu = self.top_window.get_main_contents()
                for menu in top_menu:
                    self.stdscr.addstr(menu)

        except curses.error:
            print('異常終了')
            # curses.beep()

        except KeyboardInterrupt:
            print('正常に終了しました')

class Key:
    """キークラス
    """
    ENTER = 10
    ESC = 27
    DOWN = 258
    UP = 259
    LEFT = 260
    RIGHT = 261

    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr

    def get_current(self) -> int:
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

class WindowStatus:
    """画面メニュークラス
       画面メニュー状態用(1:TOP画面/2:スタート画面/3:設定画面)
       NOTE: TOP画面状態で初期化
    """
    def __init__(self) -> None:
        self.window_state = 1

class BaseWindow:
    """windowクラス(基底クラス)
        NOTE: 各ウィンドウクラスが継承すべきクラス
    """
    def __init__(self, header:list, main_contents:list, footer:list) -> None:
        """コンストラクタ

        Args:
            header (list): ヘッダー情報
            main_contents (list): メインコンテンツ情報
            footer (list): フッター情報
        """
        self.header         = header
        self.main_contents  = main_contents
        self.footer         = footer

    def get_header(self) -> list:
        """ヘッダー情報を取得する

        Returns:
            list: ヘッダー情報
        """
        return self.header
    
    def get_main_contents(self) -> list:
        """メイン情報を取得する

        Returns:
            list: メイン情報
        """
        return self.main_contents
    
    def get_footer(self) -> list:
        """フッター情報を取得する

        Returns:
            list: フッター情報
        """
        return self.footer

class TopWindow(BaseWindow):
    """トップ画面クラス
       TOP画面ボタン選択状態(1:スタートボタン点滅/2:設定ボタン点滅)
    """    
    def __init__(self) -> None:
        """コンストラクタ
        """
        # TOP画面文字列
        self.header_list = [
            '\t===============================================\n',
            '\t<<<<            スネークゲーム             >>>>\n',
            '\t===============================================\n',
            '\n'
        ]

        self.main_contents_list = [
            '\t\t   <-- ゲームスタート -->\n',
            '\t\t   <--      設定      -->'
        ]

        # 親クラス呼び出し
        super().__init__(self.header_list, self.main_contents_list, [])

class GameWindow(BaseWindow):
    """ゲーム画面クラス
    """
    def __init__(self) -> None:
        """コンストラクタ
        """
        # ゲーム画面文字列
        self.header_list = [
            '\n',
            '\n',
            '\t<<<<            スネークゲーム             >>>>\n'
        ]

        self.main_contents_list = [
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

        self.footer_list = [
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
        super().__init__(self.header_list, self.main_contents_list, self.footer_list)

    def get_game_over_wnd(self) -> list:
        """ゲーム画面のゲームオーバー情報を取得する

        Returns:
            list: ゲーム画面のゲームオーバー情報
        """
        return self.game_over_list

class SettingWindow:
    """設定画面クラス
    """
    pass

if __name__ == "__main__":
    # 以下のwrapper関数は必ず呼び出す必要がある
    try:
        wrapper(main)
    except curses.error:
        print('異常終了')
    print('終了')