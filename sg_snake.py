#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sg_input_key_manager import KeyData

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
        # 蛇が進む方向
        self.cusor_direction = KeyData.RIGHT
        # 体が動かせるか動かせないかを判断するフラグ
        # NOTE:最初にTrueにすると本来欲しいキー入力以外でも体が動こうとする処理に入ってしまうためFalseで定義する
        self.is_move = False

    def get_x(self) -> int:
        """蛇のx座標を取得
        """
        return self.snake_pos[0]
    
    def __set_x(self, x: int) -> None:
        """蛇のx座標を設定
        """
        self.snake_pos[0] = x
    
    def get_y(self) -> int:
        """蛇のy座標を取得
        """
        return self.snake_pos[1]
    
    def __set_y(self, y: int) -> None:
        """蛇のy座標を設定
        """
        self.snake_pos[1] = y

    def get_pos(self) -> list:
        """蛇の位置を取得
        """
        return self.snake_pos

    def get_head_char(self) -> str:
        """蛇の頭を取得
        """
        return self.snake_head_char
        
    def move_up(self) -> None:
        """蛇を上に移動
        """
        # snake_pos[1]は蛇の位置のy座標を示す
        # snake_posのy座標が1以下の場合は1で設定し、体が動かないようにFalseに設定
        if self.get_y() <= 1:
            self.__set_y(1)
            self.__set_enable_move(False)
        
        # snake_posのy座標が1以上の場合は-1して上に移動、体がついていくようにTrueに設定
        # NOTE: y座標の場合、下に行くほど数がでかくなる
        else:
            self.__set_y(self.get_y() - 1)
            self.__set_enable_move(True)

        self.set_direction(KeyData.UP)

    def move_down(self) -> None:
        """蛇を下に移動
        """
        # snake_pos[1]は蛇の位置のy座標を示す
        # snake_posのy座標が1以下の場合は1で設定し、体が動かないようにFalseに設定
        if 8 <= self.get_y():
            self.__set_y(8)
            self.__set_enable_move(False)
        
        # snake_posのy座標が1以上の場合は-1して上に移動、体がついていくようにTrueに設定
        # NOTE: y座標の場合、下に行くほど数がでかくなる
        else:
            self.__set_y(self.get_y() + 1)
            self.__set_enable_move(True)

        self.set_direction(KeyData.UP)

    def move_right(self) -> None:
        """蛇を右に移動
        """
        # snake_pos[0]は蛇の位置のx座標を示す
        # snake_posのx座標が46以上の場合は46で設定し、体が動かないようにFalseに設定
        if 46 <= self.get_x():
            self.__set_x(46)
            self.__set_enable_move(False)
        
        # snake_posのx座標が46以下の場合は＋1して右に移動し、体がついていくようにTrueに設定
        # NOTE: x座標の場合、右に行くほど数がでかくなる
        else:
            self.__set_x(self.get_x() + 1)
            self.__set_enable_move(True)
        
        self.set_direction(KeyData.RIGHT)

    def move_left(self) -> None:
        """蛇を左に移動
        """
        # snake_pos[0]は蛇の位置のx座標を示す
        # snake_posのx座標が2以下の場合は2で設定し、体が動かないようにFalseに設定
        if self.get_x() <= 2:
            self.__set_x(2)
            self.__set_enable_move(False)
        
        # snake_pos[0]は蛇の位置のx座標を示す
        # snake_posのx座標が46以上の場合は46で設定し、体が動かないようにFalseに設定
        else:
            self.__set_x(self.get_x() - 1)
            self.__set_enable_move(True)

        self.set_direction(KeyData.LEFT)

    def set_direction(self, direct:KeyData) -> None:
        """蛇の自動で進む方向を設定
        """
        self.cusor_direction = direct

    def get_direction(self) -> KeyData:
        """蛇の自動で進む方向を取得
        """
        return self.cusor_direction
    
    def __set_enable_move(self, enable:bool) -> None:
        """蛇の移動可不可状態を設定
        """
        self.is_move = enable

    def get_is_move(self) -> bool:
        """蛇の移動可不可状態を取得
        """
        return self.is_move
