#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Speed:
    """ゲーム速度クラス
    """
    def __init__(self, speed: int = 1) -> None:
        """コンストラクタ
        """
        # ゲームの速度設定
        self.speed = speed

    def set_speed(self, speed: int) -> int:
        """ゲームの速度設定

        Args:
            speed (int): 速度
        """
        self.speed = speed
    
    def get_speed(self) -> int:
        """ゲームの速度取得

        Returns:
            int: ゲームの速度
        """
        return self.speed
