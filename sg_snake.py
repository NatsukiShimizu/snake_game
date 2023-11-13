#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from sg_input_key_manager import KeyData

class Snake:
    """蛇クラス
    """
    def __init__(self) -> None:
        """コンストラクタ
        """
        # ゲーム画面のボディー部分の作成
        self.head_char = '@'
        self.body_char = 'o'
        # 蛇の位置(x, y)
        self.head_pos       = [22, 4]
        # 蛇の体用変数定義(デフォルトでは蛇の体は頭を含めて3つの部品から構成)
        self.body_pos_list = [
            [self.head_pos[0]-1, self.head_pos[1]],
            [self.head_pos[0]-2, self.head_pos[1]]
        ]
        self.sorted_body_pos_list = []
        # 蛇が進む方向
        self.cusor_direction = KeyData.RIGHT
        # 体が動かせるか動かせないかを判断するフラグ
        # NOTE:最初にTrueにすると本来欲しいキー入力以外でも体が動こうとする処理に入ってしまうためFalseで定義する
        self.is_move = False

    def get_head_x(self) -> int:
        """蛇の頭のx座標を取得

        Returns:
            int: 蛇の頭のx座標
        """
        return self.head_pos[0]
    
    def get_head_y(self) -> int:
        """蛇の頭のy座標を取得

        Returns:
            int: 蛇の頭のy座標
        """
        return self.head_pos[1]
    
    def get_body_x(self, index: int) -> int:
        """蛇の体のx座標を取得

        Returns:
            int: 蛇の体のx座標
        """
        return self.sorted_body_pos_list[index][0]
    
    def get_body_y(self, index: int) -> int:
        """蛇の体のy座標を取得

        Returns:
            int: 蛇の体のy座標
        """
        return self.sorted_body_pos_list[index][1]

    def get_head_pos(self) -> list:
        """蛇の頭の位置を取得

        Returns:
            list: 蛇の頭の位置
        """
        return self.head_pos

    def get_head_char(self) -> str:
        """蛇の頭を示す文字を取得

        Returns:
            str: 蛇の頭を示す文字
        """
        return self.head_char
    
    def get_body_char(self) -> str:
        """蛇の体を示す文字を取得

        Returns:
            str: 蛇の体を示す文字
        """
        return self.body_char
    
    def get_body_pos(self) -> list:
        """蛇の体の位置を取得

        Returns:
            list: 蛇の体の位置情報
        """
        return self.body_pos_list
    
    def sort_body_pos(self) -> None:
        """蛇の体を昇順でソートする
        """
        # 蛇の体が追加できるようにy座標の数字が小さい順位並べ替える
        self.sorted_body_pos_list = sorted(self.body_pos_list, key=lambda x:(x[1], x[0]))

    def get_length_body_pos(self) -> int:
        """蛇の体の配列の要素数を取得

        Returns:
            int: 要素数
        """
        return len(self.body_pos_list)

    def move_up(self) -> None:
        """蛇を上に移動
        """
        # snake_pos[1]は蛇の位置のy座標を示す
        # snake_posのy座標が1以下の場合は1で設定し、体が動かないようにFalseに設定
        if self.get_head_y() <= 1:
            self.__set_head_y(1)
            self.__set_enable_move(False)
        
        # snake_posのy座標が1以上の場合は-1して上に移動、体がついていくようにTrueに設定
        # NOTE: y座標の場合、下に行くほど数がでかくなる
        else:
            self.__update_body_pos()
            self.__set_head_y(self.get_head_y() - 1)
            self.__set_enable_move(True)

        self.set_direction(KeyData.UP)

    def move_down(self) -> None:
        # snake_pos[1]は蛇の位置のy座標を示す
        # snake_posのy座標が1以下の場合は1で設定し、体が動かないようにFalseに設定
        if 8 <= self.get_head_y():
            self.__set_head_y(8)
            self.__set_enable_move(False)
        
        # snake_posのy座標が1以上の場合は-1して上に移動、体がついていくようにTrueに設定
        # NOTE: y座標の場合、下に行くほど数がでかくなる
        else:
            self.__update_body_pos()
            self.__set_head_y(self.get_head_y() + 1)
            self.__set_enable_move(True)

        self.set_direction(KeyData.DOWN)

    def move_right(self) -> None:
        """蛇を右に移動
        """
        # snake_pos[0]は蛇の位置のx座標を示す
        # snake_posのx座標が46以上の場合は46で設定し、体が動かないようにFalseに設定
        if 46 <= self.get_head_x():
            self.__set_head_x(46)
            self.__set_enable_move(False)
        
        # snake_posのx座標が46以下の場合は＋1して右に移動し、体がついていくようにTrueに設定
        # NOTE: x座標の場合、右に行くほど数がでかくなる
        else:
            self.__update_body_pos()
            self.__set_head_x(self.get_head_x() + 1)
            self.__set_enable_move(True)
        
        self.set_direction(KeyData.RIGHT)

    def move_left(self) -> None:
        """蛇を左に移動
        """
        # snake_pos[0]は蛇の位置のx座標を示す
        # snake_posのx座標が2以下の場合は2で設定し、体が動かないようにFalseに設定
        if self.get_head_x() <= 2:
            self.__set_head_x(2)
            self.__set_enable_move(False)
        
        # snake_pos[0]は蛇の位置のx座標を示す
        # snake_posのx座標が46以上の場合は46で設定し、体が動かないようにFalseに設定
        else:
            self.__update_body_pos()
            self.__set_head_x(self.get_head_x() - 1)
            self.__set_enable_move(True)

        self.set_direction(KeyData.LEFT)

    def set_direction(self, direct:KeyData) -> None:
        """蛇の自動で進む方向を設定

        Args:
            direct (KeyData): 蛇の自動で進む方向
        """
        self.cusor_direction = direct

    def get_direction(self) -> KeyData:
        """蛇の自動で進む方向を取得

        Returns:
            KeyData: 蛇の自動で進む方向
        """
        return self.cusor_direction
    
    def get_is_move(self) -> bool:
        """蛇の移動可不可状態を取得

        Returns:
            bool: 蛇の移動可不可状態
        """
        return self.is_move

    def __set_enable_move(self, enable:bool) -> None:
        """蛇の移動可不可状態を設定

        Args:
            enable (bool): 蛇の移動可不可状態
        """
        self.is_move = enable
    
    def __set_head_x(self, x: int) -> None:
        """蛇の頭x座標を設定 (内部処理用)

        Args:
            x (int): 蛇の頭x座標
        """
        self.head_pos[0] = x

    def __set_head_y(self, y: int) -> None:
        """蛇の頭y座標を設定 (内部処理用)

        Args:
            y (int): 蛇の頭y座標
        """
        self.head_pos[1] = y

    def __set_body_x(self, index: int, x: int) -> None:
        """蛇の体x座標を設定 (内部処理用)

        Args:
            index (int): 蛇の体の位置を示す要素位置
            x (int): 蛇の体x座標
        """
        self.body_pos_list[index][0] = x

    def __set_body_y(self, index: int, y: int) -> None:
        """蛇の体y座標を設定 (内部処理用)

        Args:
            index (int): 蛇の体の位置を示す要素位置
            y (int): 蛇の体y座標
        """
        self.body_pos_list[index][1] = y

    def __update_body_pos(self) -> None:
        """蛇の体の位置情報更新
        """
        _priv_body_pos = copy.deepcopy(self.get_body_pos())
        for i, _ in enumerate(_priv_body_pos):
            if i == 0:
                self.__set_body_x(i, self.get_head_x())
                self.__set_body_y(i, self.get_head_y())
            else:
                self.__set_body_x(i, _priv_body_pos[i-1][0])
                self.__set_body_y(i, _priv_body_pos[i-1][1])
