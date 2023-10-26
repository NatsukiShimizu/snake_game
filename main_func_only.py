#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import random
import copy
import time
from curses import wrapper


def main(stdscr):
    """エントリーポイント用の関数
        NOTE:この関数を引数として[wrapper]関数に渡す必要がある

    Args:
        stdscr (_type_): 標準画面出力インスタンス
                         NOTE:ターミナルに何かを表示するためにこの引数が必要
                              stdscrの引数を使って色々と画面に表示するものを作る
    """
    # -----------------------------------------
    ### 変数定義 ###
    # 入力された文字列用バッファ
    text =''
    # 区切り文字
    horizontal_frame = '-'
    vertical_frame = '|'
    # 区切り文字数
    horizontal_num = 0
    vertical_num = 0
    # 区切り文字数(画面サイズ)制限値
    horizontal_num_limit = 0
    vertical_num_limit = 0
    # 画面メニュー状態用(1:TOP画面/2:スタート画面/3:設定画面)
    # NOTE: TOP画面状態で初期化
    window_state = 1
    # TOP画面ボタン選択状態(1:スタートボタン点滅/2:設定ボタン点滅)
    top_menu_state = 1
    # 蛇の位置(x, y)
    snake_pos = [22, 4]
    # 蛇の餌位置(x, y)
    food_pos = [0, 0]
    # ゲームの速度設定用
    speed = 1

    # -----------------------------------------
    ### 初期化処理 ###
    # カーソルを不可視に設定
    curses.curs_set(0)
    # 画面サイズ取得(表示されているターミナルの表示サイズ)
    horizontal_num_limit, vertical_num_limit = stdscr.getmaxyx()
    # 標準出力画面の情報をクリアする
    stdscr.clear()
    # -----------------------------------------
    ### メイン処理 ###
    try:
        # アプリ機能を持続させるためのループ
        while True:

            # -----------------------------------------
            ### TOP画面表示処理
            # NOTE: 以下のような画面をターミナルに出力する処理を記述する
            """
                ===============================================
                <<<<            スネークゲーム             >>>> 
                ===============================================

                            <-- ゲームスタート -->
                            <--      設定      -->
            """
            # TOP画面表示用ループ処理
            while True:
                stdscr.addstr('\t===============================================\n')
                stdscr.addstr('\t<<<<            スネークゲーム             >>>>\n')
                stdscr.addstr('\t===============================================\n')
                stdscr.addstr('\n')

                if top_menu_state != 1:
                    # 設定ボタンを点滅
                    stdscr.addstr(4, 20, '<-- ゲームスタート -->\n')
                    stdscr.addstr(5, 20, '<--      設定      -->', curses.A_STANDOUT)
                else:
                    # スタートボタンを点滅
                    stdscr.addstr(4, 20, '<-- ゲームスタート -->\n', curses.A_STANDOUT)
                    stdscr.addstr(5, 20, '<--      設定      -->\n')
                
                # 画面更新
                stdscr.refresh()

                # キー入力待ち
                key = stdscr.getch()

                # エンター入力で
                if key == 10:
                    # TOP画面を終了
                    break
                elif key == 259:
                    top_menu_state = 1
                elif key == 258:
                    top_menu_state = 2
                else:
                    pass

                # 画面クリア
                stdscr.clear()

            # 画面クリア(トップ画面を一度削除する)
            stdscr.clear()

            # -----------------------------------------
            ### ゲーム画面切り替え処理
            # NOTE: TOP画面からゲーム画面か設定画面に遷移する
            if top_menu_state == 1:
                window_state = 2
            
            elif top_menu_state == 2:
                window_state = 3

            # ゲーム画面表示
            if window_state == 2:
                # -----------------------------------------
                ### ゲーム画面表示処理
                # NOTE: 以下のような画面をターミナルに出力する処理を記述する
                #       蛇は(#<),餌は(+)で表す
                """
                    <<<<            スネークゲーム             >>>>
                    -----------------------------------------------
                    |                                             |
                    |                                             |
                    |                                             |
                    |                   oo@       +               |
                    |                                             |
                    |                                             |
                    |                                             |
                    |                                             |
                    -----------------------------------------------
                                
                            <--      上移動 ↑ キー     -->
                            <--      下移動 ↓ キー     -->
                            <--      左移動 ← キー     -->
                            <--      右移動 → キー     -->
                            <--        ESCで終了       -->
                """
                
                ### ゲーム画面用データ定義 ###
                game_wnd_header = [
                    '\n',
                    '\n',
                    '\t<<<<            スネークゲーム             >>>>\n'
                ]
                game_wnd_footer = [
                    '\n',
                    '\t\t<--      上移動 ↑ キー     -->\n',
                    '\t\t<--      下移動 ↓ キー     -->\n',
                    '\t\t<--      左移動 ← キー     -->\n',
                    '\t\t<--      右移動 → キー     -->\n',
                    '\t\t<--     ESC,Enterで終了    -->\n',
                    '\n'
                ]
                game_over_wnd = [
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
                # 蛇の体用変数定義(デフォルトでは蛇の体は頭を含めて3つの部品から構成)
                food_body_pos_list = [
                    [21, 4],
                    [20, 4]
                ]
                
                # ゲーム画面のボディー部分の作成
                snake_head_char = '@'
                snake_body_char = 'o'
                snake_food_char = '+'

                # ゲーム画面が表示されて初めて餌の座標を生成する用のフラグ
                is_feed = False
                # ゲームオーバー判定フラグ
                is_game_over = False
                # カーソルの方向
                cusor_direction_num = 261

                # ゲーム画面表示ループ処理
                stdscr.nodelay(True)
                while True:
                    game_wnd_body = [
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
                    
                    # ゲーム画面のヘッダー部分の作成
                    for text in game_wnd_header:
                        stdscr.addstr(text)

                    # ゲーム画面が表示されて初回のみここの処理に入る
                    # NOTE: ２回目以降はここの処理に入らなくなる
                    while is_feed is False:
                        random_num_x = random.randint(2, 46)
                        random_num_y = random.randint(1, 8)
                        food_pos = [random_num_x, random_num_y]

                        # 餌の位置と蛇の位置が一緒の場合はこれ以降の処理を行わずwhile文のブロックの先頭に戻る
                        if food_pos == snake_pos:
                            continue

                        # 蛇が餌を食べるまで餌の位置を固定して表示させる
                        else:
                            is_feed = True
                            break

                    # 蛇の体が追加できるようにy座標の数字が小さい順位並べ替える
                    newfood_body_pos_list = sorted(food_body_pos_list, key=lambda x:(x[1], x[0]))
                    body_pos_num = len(newfood_body_pos_list)
                    body_pos_idx_cnt = 0
                    food_body_pos_list[0]
                    # 体を増やす判定
                    is_add_body = False
                    

                    for y, text in enumerate(game_wnd_body):
                        new_text = ''

                        if is_game_over is True:
                            break

                        # 205行目で1つずつ配列を取り出し、1つの配列の中の1文字を取り出す
                        for x, char in enumerate(text):
                            if is_game_over is True:
                                # 何週かループして追加されたテキストを念のためリセットする[new_text = '']
                                new_text = ''
                                break

                            for body_pos in food_body_pos_list:
                                if snake_pos[0] == body_pos[0] and \
                                   snake_pos[1] == body_pos[1]:
                                    is_game_over = True
                                    break
                            
                            # 食べ物が食べられたかor配置されていないかの判定
                            if snake_pos[0] == food_pos[0] and \
                               snake_pos[1] == food_pos[1]:
                                while True:
                                    random_num_x = random.randint(2, 46)
                                    random_num_y = random.randint(1, 8)
                                    food_pos = [random_num_x, random_num_y]
                                    # 餌の位置と蛇の頭の位置が一緒の場合はこれ以降の処理を行わずwhile文のブロックの先頭に戻る
                                    if food_pos == snake_pos:
                                        continue
                                    # 餌の位置と蛇の体の位置が一緒の場合も同様
                                    elif food_pos in newfood_body_pos_list:
                                        continue
                                    else:
                                        # 餌を表示する
                                        # 体も1つ追加
                                        is_add_body = True
                                        speed *= 1.1
                                        break

                            # 蛇の頭配置判定
                            if x == snake_pos[0] and \
                               y == snake_pos[1]:
                                # new_textに追加することにより空白を文字に置き換える
                                new_text += snake_head_char
                                continue

                            ## 蛇の体配置判定
                            # 配列にアクセスする時の要素数を超えないようにする判定
                            # NOTE:test_list = [1, 2] -> test_list[2]のような範囲外のアクセスを防ぐ
                            if body_pos_idx_cnt < body_pos_num:
                                if x == newfood_body_pos_list[body_pos_idx_cnt][0] and \
                                   y == newfood_body_pos_list[body_pos_idx_cnt][1]:
                                    new_text += snake_body_char
                                    body_pos_idx_cnt += 1
                                    continue

                            # 蛇の餌配置判定
                            if x == food_pos[0] and \
                               y == food_pos[1]:
                                new_text += snake_food_char
                                continue

                            # それ以外の文字列配置
                            new_text += char

                        stdscr.addstr(new_text)

                    if is_game_over is True:
                        # ゲームオーバー画面の作成
                        for text in game_over_wnd:
                            stdscr.addstr(text)
                    
                    # ゲーム画面のフッター部分の作成
                    for text in game_wnd_footer:
                        stdscr.addstr(text)

                    # キー入力待ち
                    key = stdscr.getch()
                    if key == -1:
                        key = cusor_direction_num

                    # キー入力で移動
                    # 体が動かせるか動かせないかを判断するフラグ
                    # NOTE:最初にTrueにすると本来欲しいキー入力以外でも体が動こうとする処理に入ってしまうためFalseで定義する
                    is_move = False
                    priv_snake_pos = copy.deepcopy(snake_pos)
                    priv_food_body_pos_list = copy.deepcopy(food_body_pos_list)
                    # if key == 'KEY_UP':
                    if key == 259:
                        # snake_pos[1]は蛇の位置のy座標を示す
                        # snake_posのy座標が1以下の場合は1で設定し、体が動かないようにFalseに設定
                        if snake_pos[1] <= 1:
                            snake_pos[1] = 1
                            is_move = False
                        # snake_posのy座標が1以上の場合は-1して上に移動、体がついていくようにTrueに設定
                        # NOTE: y座標の場合、下に行くほど数がでかくなる
                        else:
                            snake_pos[1] = snake_pos[1] - 1
                            is_move = True
                        cusor_direction_num = 259

                    # elif key == 'KEY_DOWN':
                    elif key == 258:
                        # snake_pos[1]は蛇の位置のy座標を示す
                        # snake_posのy座標が8以上の場合は8で設定し、体が動かないようにFalseに設定
                        if 8 <= snake_pos[1]:
                            snake_pos[1] = 8
                            is_move = False
                        # snake_posのy座標が8以下の場合は＋1して下に移動、体がついていくようにTrueに設定
                        # NOTE: y座標の場合、下に行くほど数がでかくなる
                        else:
                            snake_pos[1] = snake_pos[1] + 1
                            is_move = True
                        cusor_direction_num = 258

                    # elif key == 'KEY_LEFT':
                    elif key == 260:
                        # snake_pos[0]は蛇の位置のx座標を示す
                        # snake_posのx座標が2以下の場合は2で設定し、体が動かないようにFalseに設定
                        if snake_pos[0] <= 2:
                            snake_pos[0] = 2
                            is_move = False
                        # snake_posのx座標が2以上の場合はｰ1して左に移動し、体がついていくようにTrueに設定
                        # NOTE: x座標の場合、右に行くほど数がでかくなる
                        else:
                            snake_pos[0] = snake_pos[0] - 1
                            is_move = True
                        cusor_direction_num = 260

                    # elif key == 'KEY_RIGHT':
                    elif key == 261:
                        # snake_pos[0]は蛇の位置のx座標を示す
                        # snake_posのx座標が46以上の場合は46で設定し、体が動かないようにFalseに設定
                        if 46 <= snake_pos[0]:
                            snake_pos[0] = 46
                            is_move = False
                        # snake_posのx座標が46以下の場合は＋1して右に移動し、体がついていくようにTrueに設定
                        # NOTE: x座標の場合、右に行くほど数がでかくなる
                        else:
                            snake_pos[0] = snake_pos[0] + 1
                            is_move = True
                        cusor_direction_num = 261

                    # elif key == '\n':
                    elif key == 10 or key == 27:
                        # NOTE: [ESC], [Enter]キーで終了
                        stdscr.nodelay(False)
                        break

                    # 上記で指定したキー以外が入力されるとここの処理に入る
                    else:
                        # NOTE: デバック用
                        stdscr.addstr(f'{key}')
                    
                    # 体が動かせるか動かせないかを判断するフラグ
                    # NOTE: フラグがTrueの場合こちらの処理に入る
                    if is_move is True:
                        for i, pos in enumerate(food_body_pos_list):
                            # food_body_pos_list[21, 4]の場合に入る処理
                            if i == 0:
                            # 頭がいた場所の座標を代入し、頭のいた場所に体を移動させる処理
                                food_body_pos_list[i][0] = priv_snake_pos[0]
                                food_body_pos_list[i][1] = priv_snake_pos[1]
                            # food_body_pos_list[20, 4]の場合に入る処理
                            # 頭の次の体の座標を代入し、1つ前の体の位置に移動させる処理
                            else:
                                food_body_pos_list[i][0] = priv_food_body_pos_list[i-1][0]
                                food_body_pos_list[i][1] = priv_food_body_pos_list[i-1][1]

                    # 体を増やす判定処理
                    priv_body_pos_num = len(priv_food_body_pos_list)
                    if is_add_body is True:
                        food_body_pos_list.append(priv_food_body_pos_list[priv_body_pos_num-1])

                    # 蛇の速度設定
                    time.sleep(0.5 / speed)
                    # 画面クリア
                    stdscr.clear()
                    # 画面更新
                    stdscr.refresh()
                break

            # 設定画面表示
            elif window_state == 3:
                while True:
                    stdscr.addstr(f'設定画面\n')
                
                    # 画面更新
                    stdscr.refresh()

                    # キー入力待ち
                    key = stdscr.getkey()

                    # エンター入力で
                    if key == '\n':
                        break
                    elif key == 'KEY_UP':
                        pass
                    elif key == 'KEY_DOWN':
                        pass
                    elif key == '^[':
                        stdscr.addstr('ESC')
                    else:
                        stdscr.addstr(f'{key}')
                    # 画面更新
                    stdscr.refresh()

                    # キー入力待ち
                    key = stdscr.getkey()
                    
                    # 画面クリア
                    stdscr.clear()
                break

    except curses.error:
        print('異常終了')
        # curses.beep()

    except KeyboardInterrupt:
        print('正常に終了しました')

    print('テスト')
    return



if __name__ == "__main__":
    # 以下のwrapper関数は必ず呼び出す必要がある
    try:
        wrapper(main)
    except curses.error:
        print('異常終了')
    print('終了')
    