#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sg_base_window import BaseWindow

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

        self.game_over_footer_list = [
            '\n',
            '\t      <--  何かキーを押してください  -->\n',
        ]

        # 親クラス呼び出し
        super().__init__(stdscr, header_list, main_contents_list, footer_list)

    def get_game_over_wnd(self) -> list:
        """ゲーム画面のゲームオーバー情報を取得する

        Returns:
            list: ゲーム画面のゲームオーバー情報
        """
        return self.game_over_list, self.game_over_footer_list
