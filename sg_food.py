#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Food:
    """蛇の餌クラス
    """
    def __init__(self) -> None:
        # ゲーム画面の餌部分の作成
        self.snake_food_char = '+'
