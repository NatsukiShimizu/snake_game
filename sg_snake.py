#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Snake:
    """蛇クラス
    """
    def __init__(self) -> None:
        # ゲーム画面のボディー部分の作成
        self.snake_head_char = '@'
        self.snake_body_char = 'o'
        # 蛇の位置(x, y)
        self.snake_pos       = [22, 4]
        # 蛇の体用変数定義(デフォルトでは蛇の体は頭を含めて3つの部品から構成)
        self.food_body_pos_list = [
            [self.snake_pos[0]-1, self.snake_pos[1]],
            [self.snake_pos[0]-2, self.snake_pos[1]]
        ]
