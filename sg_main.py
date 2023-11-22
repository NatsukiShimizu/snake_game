#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import time

from curses import wrapper
from typing import Any

from sg_food import Food
from sg_game_window import GameWindow
from sg_input_key_manager import KeyData, InputKeyManager
from sg_setting_window import SettingWindow, SubMenuState
from sg_snake import Snake
from sg_speed import Speed
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
        self.sub_menu_state  = SubMenuState.SPEED
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
        food = Food()
        snake = Snake()
        speed = Speed()

        # 現在のメニュー状態がゲームスタート状態じゃなければ以下の処理をスキップ
        if self.menu_state != MenuState.GAME_START:
            return

        self.stdscr.nodelay(True)

        # ゲーム画面を持続させるためのループ
        while True:
            # ヘッダー情報取得
            header = self.game_window.get_header()
            for h in header:
                self.stdscr.addstr(h)

            # コンテンツ情報取得
            main_contents = self.game_window.get_main_contents()

            # 蛇の体情報をソート
            snake.sort_body_pos()
            # 蛇の体の配列の要素数を取得
            body_pos_idx_cnt = 0

            for y, contents in enumerate(main_contents):
                new_text = ''

                # 1つずつ配列を取り出し、1つの配列の中の1文字を取り出す
                for x, char in enumerate(contents):
                    # 食べ物が食べられたかor配置されていないかの判定
                    if snake.get_head_x() == food.get_x() and \
                       snake.get_head_y() == food.get_y():
                        while True:
                            food.update_random_pos()
                            # 餌の位置と蛇の頭の位置が一緒の場合はこれ以降の処理を行わずwhile文のブロックの先頭に戻る
                            if food.get_pos() == snake.get_head_pos():
                                continue
                            # 餌の位置と蛇の体の位置が一緒の場合も同様
                            elif snake.is_exists_body(food.get_pos()):
                                continue
                            else:
                                snake.add_body_pos()
                                speed.set_speed(speed.get_speed() * 1.05)
                                break
                    
                    # ゲームオーバー
                    if snake.is_exists_body(snake.get_head_pos()):
                        self.stdscr.clear()
                        self.stdscr.nodelay(False)
                        
                        # ヘッダー情報取得
                        header = self.game_window.get_header()
                        for h in header:
                            self.stdscr.addstr(h)
                        
                        # コンテンツ情報取得
                        game_over_wnd, game_over_footer = self.game_window.get_game_over_wnd()
                        for g in game_over_wnd:
                            self.stdscr.addstr(g)
                        
                        # フッター情報取得
                        for f in game_over_footer:
                            self.stdscr.addstr(f)
                        
                        # 画面更新
                        self.stdscr.refresh()
                        self.input_key_mng.getch()
                        self.stdscr.clear()
                        return
                        

                    # 蛇の餌配置判定
                    if x == food.get_x() and \
                       y == food.get_y():
                        new_text += food.get_food_char()
                        continue

                    # 蛇の頭配置判定
                    if x == snake.get_head_x() and \
                       y == snake.get_head_y():
                        # new_textに追加することにより空白を文字に置き換える
                        new_text += snake.get_head_char()
                        continue

                    # 蛇の体配置判定
                    # 配列にアクセスする時の要素数を超えないようにする判定
                    # NOTE:test_list = [1, 2] -> test_list[2]のような範囲外のアクセスを防ぐ
                    if body_pos_idx_cnt < snake.get_length_body_pos():
                        if x == snake.get_body_x(body_pos_idx_cnt) and \
                           y == snake.get_body_y(body_pos_idx_cnt):
                            # new_textに追加することにより空白を文字に置き換える
                            new_text += snake.get_body_char()
                            body_pos_idx_cnt += 1
                            continue

                    new_text += char

                self.stdscr.addstr(new_text)

            # フッター情報取得
            footer = self.game_window.get_footer()
            for f in footer:
                self.stdscr.addstr(f)

            key = self.input_key_mng.getch()

            # エンター/esc入力
            if key == KeyData.ENTER or key == KeyData.ESC:
                # ゲーム画面を終了
                # 標準出力画面の情報をクリアする
                self.stdscr.clear()
                # NOTE: [ESC], [Enter]キーで終了
                self.stdscr.nodelay(False)
                break
            elif key == KeyData.UP:
                snake.move_up()
            elif key == KeyData.DOWN:
                snake.move_down()
            elif key == KeyData.RIGHT:
                snake.move_right()
            elif key == KeyData.LEFT:
                snake.move_left()
            # 上記で指定したキー以外が入力されるとここの処理に入る
            else:
                # NOTE: 自動移動
                snake.auto_move()
            
            # 蛇の速度設定
            time.sleep(0.1 / speed.get_speed())
            # 標準出力画面の情報をクリアする
            self.stdscr.clear()
            # 画面更新
            self.stdscr.refresh()

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

            # 設定画面のメニュー情報取得
            setting_menu = self.setting_window.select_menu(self.sub_menu_state)
            for menu in setting_menu:
                if menu[3] is None:
                    self.stdscr.addstr(menu[0], menu[1], menu[2])
                else:
                    self.stdscr.addstr(menu[0], menu[1], menu[2], menu[3])

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
                # サブメニュー状態がステータスクラスの最小値なら最小値の状態を設定する
                if self.sub_menu_state <= SubMenuState.SPEED:
                    self.sub_menu_state = SubMenuState.SPEED
                else:
                    self.sub_menu_state -= 1

            elif key == KeyData.DOWN:
                # サブメニュー状態がステータスクラスの最大値なら最大値の状態を設定する
                if SubMenuState.AUDIO <= self.sub_menu_state:
                    self.sub_menu_state = SubMenuState.AUDIO
                else:
                    self.sub_menu_state += 1
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
