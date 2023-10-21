#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
import random
import copy
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

    # -----------------------------------------
    ### 初期化処理 ###
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
                    stdscr.addstr('\t\t    <-- ゲームスタート -->\n')
                    stdscr.addstr('\t\t    <--      設定      -->\n', curses.A_BLINK)
                else:
                    # スタートボタンを点滅
                    stdscr.addstr('\t\t    <-- ゲームスタート -->\n', curses.A_BLINK)
                    stdscr.addstr('\t\t    <--      設定      -->\n')

                # 画面更新
                stdscr.refresh()

                # キー入力待ち
                key = stdscr.getkey()

                # エンター入力で
                if key == '\n':
                    # TOP画面を終了
                    break
                elif key == 'KEY_UP':
                    top_menu_state = 1
                elif key == 'KEY_DOWN':
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
                    '\t\t<--        ESCで終了       -->\n',
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

                # ゲーム画面表示ループ処理
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

                    newfood_body_pos_list = sorted(food_body_pos_list, key=lambda x:(x[1], x[0]))

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
                                     # 餌の位置と蛇の位置が一緒の場合はこれ以降の処理を行わずwhile文のブロックの先頭に戻る
                                    if food_pos == snake_pos:
                                        continue
                                    else:
                                        break

                            # 蛇の頭配置判定
                            if x == snake_pos[0] and \
                               y == snake_pos[1]:
                                # new_textに追加することにより空白を文字に置き換える
                                new_text += snake_head_char
                                continue

                            ## 蛇の体配置判定
                            # 蛇の体１(頭のすぐ後ろ)
                            if x == food_body_pos_list[0][0] and \
                               y == food_body_pos_list[0][1]:
                                new_text += snake_body_char
                                continue

                            # 蛇の体２
                            if x == food_body_pos_list[1][0] and \
                               y == food_body_pos_list[1][1]:
                                new_text += snake_body_char
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
                    key = stdscr.getkey()

                    # キー入力で移動
                    # 体が動かせるか動かせないかを判断するフラグ
                    # NOTE:最初にTrueにすると本来欲しいキー入力以外でも体が動こうとする処理に入ってしまうためFalseで定義する
                    is_move = False
                    priv_snake_pos = copy.deepcopy(snake_pos)
                    priv_food_body_pos_list = copy.deepcopy(food_body_pos_list)
                    if key == 'KEY_UP':
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

                    elif key == 'KEY_DOWN':
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

                    elif key == 'KEY_LEFT':
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

                    elif key == 'KEY_RIGHT':
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

                    elif key == '\n':
                        # NOTE: 暫定てエンターキー入力で終了
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
                            # raise Exception(f'i:{i} food_body_pos_list:{food_body_pos_list[i]}')
                            stdscr.addstr(f'food_body_pos_list{food_body_pos_list[i]}\n')
                    
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

            # -----------------------------------------
            ### 入力処理 ###
            # ユーザーからの入力を受け付けるループ
            while True:
                key = stdscr.getkey()
                # keyの値が改行コードだったら
                if key == '\n':
                    break

                else:
                    text += key

            # 確認用
            # stdscr.addstr(0,0,str(text))
            

            # -----------------------------------------
            ### アプリ画面作成処理 ###
            # NOTE: text = '100 50' のようなデータが想定
            horizontal_num, vertical_num = map(int, text.split())
            # stdscr.addstr(0,0,str(horizontal_num))
            # stdscr.addstr(1,0,str(vertical_num))

            # # 先頭
            # for i in range(horizontal_num):
            #     stdscr.addstr(0,i,str(horizontal_frame))
            #     stdscr.refresh()

            # # 左横
            # for i in range(vertical_num-2):
            #     stdscr.addstr(i+1,0,str(vertical_frame))
            #     stdscr.refresh()
            
            # # 右横
            # for i in range(vertical_num-2):
            #     stdscr.addstr(i+1,horizontal_num-1,str(vertical_frame))
            #     stdscr.refresh()

            # # 最下部
            # for i in range(horizontal_num):
            #     stdscr.addstr(vertical_num-1,i,str(horizontal_frame))
            #     stdscr.refresh()

            ### 画面サイズを取得して画面範囲外エラー発生を防ぐ
            stdscr_y, stdscr_x = stdscr.getmaxyx()

            stdscr.addstr(f'{horizontal_frame*horizontal_num}\n')
            # stdscr.addstr(f'{vertical_frame}{" "*(horizontal_num-2)}{vertical_frame}\n')
            for i in range(3):
                stdscr.addstr(f'{vertical_frame}{" "*(horizontal_num-2)}{vertical_frame}\n')

            ### 画面サイズ表示
            stdscr.addstr(f'x:{stdscr_x} y {stdscr_y}\n')

            stdscr.refresh()

            

            # # 横文字作成
            # horizontal = horizontal_frame * horizontal_num
            # stdscr.addstr(0,0,str(horizontal))
            # stdscr.refresh()
            

            # # 縦文字作成
            # vertical =  vertical_frame * (vertical_num-2)
            # stdscr.addstr(1,0,str(vertical))
            # stdscr.refresh()
            # stdscr.addstr(1,horizontal_num-1,str(vertical))
            # stdscr.refresh()

            # stdscr.addstr(49,0,str(horizontal))
            # stdscr.refresh()

            stdscr.getkey()
            stdscr.clear()
            text = ''
            
            ### 処理終了位置 ###

            # 最後に標準出力画面に入力情報を反映させる
            # NOTE:最低限絶対に必要
            stdscr.refresh()

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
    