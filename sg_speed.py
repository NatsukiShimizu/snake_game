#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Speed:
    """ゲーム速度クラス
    """
    def __init__(self, speed: int = 0.3) -> None:
        """コンストラクタ
        """
        # ゲームの速度設定
        self.speed = speed
        self._max = 1

    def set_speed(self, speed: int) -> int:
        """ゲームの速度設定

        Args:
            speed (int): 速度
        """
        if speed <= self._max:
            self.speed = speed
        else:
            self.speed = self._max
    
    def get_speed(self) -> int:
        """ゲームの速度取得

        Returns:
            int: ゲームの速度
        """
        return self.speed
