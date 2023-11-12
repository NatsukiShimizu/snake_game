#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sg_snake import Snake

class Food:
    """蛇の餌クラス
    """
    def __init__(self) -> None:
        """コンストラクタ
        """
        # ゲーム画面の餌部分の作成
        self.snake_food_char = '+'
        # 蛇の餌位置 [x, y]
        self.food_pos =[0, 0]
        self.update_random_pos()
        # self.is_feed = False

    def get_x(self) -> int:
        """蛇の餌のx座標を取得

        Returns:
            int: 蛇の餌のx座標
        """
        return self.food_pos[0]
    
    def get_y(self) -> int:
        """蛇の餌のy座標を取得

        Returns:
            int: 蛇の餌のy座標
        """
        return self.food_pos[1]
    
    def get_pos(self) -> list:
        """蛇の餌の位置を取得

        Returns:
            list: 蛇の餌の位置
        """
        return self.food_pos

    def update_random_pos(self) -> None:
        """餌の位置をランダム更新
        """
        self.food_pos[0] = random.randint(2, 46)
        self.food_pos[1] = random.randint(1, 8)

    def get_food_char(self) -> str:
        """蛇の餌を取得

        Returns:
            str: 蛇の餌
        """
        return self.snake_food_char

    # def __set_enable_food(self, enable:bool) -> None:
    #     """蛇の餌の配置状態を設定
    #     """
    #     self.is_feed = enable

    # def get_is_feed(self) -> bool:
    #     """蛇の餌の配置状態を取得
    #     """
    #     return self.is_feed