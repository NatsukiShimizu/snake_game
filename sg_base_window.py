#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class BaseWindow:
    """windowクラス(基底クラス)
        NOTE: 各ウィンドウクラスが継承すべきクラス
    """
    def __init__(self, stdscr, header:list, main_contents:list, footer:list) -> None:
        """コンストラクタ

        Args:
            stdscr (any): 標準スクリーン
            header (list): ヘッダー情報
            main_contents (list): メインコンテンツ情報
            footer (list): フッター情報
        """
        self.stdscr         = stdscr
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