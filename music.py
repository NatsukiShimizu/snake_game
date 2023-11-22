#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
from pydub import AudioSegment
from pydub.playback import play

IS_TERMINATE = False
def play_music():
    # 音楽再生
    print('音楽再生スレッド処理開始')
    while True:
        try:
            sound = AudioSegment.from_mp3("./sample.mp3")
            play(sound)
        except Exception as e:
            print(f'{e}')
        print('音楽再生スレッド処理終了')

def main():
    """初期化処理
    """
    count = 0
    print('メインスレッド処理開始')
    while True:
        for i in range(100000):
            pass
        print(count)
        count += 1
        if IS_TERMINATE is True:
            print('メインスレッド処理終了')
            break
    

if __name__ == '__main__':
    _main_thread = threading.Thread(target=main)
    _play_music_thread = threading.Thread(target=play_music)

    try:
        print('スレッド処理開始')
        _main_thread.start()
        _play_music_thread.start()
    
    except KeyboardInterrupt:
        IS_TERMINATE = True
        _main_thread.join()
        _play_music_thread.join()
        print('スレッド処理終了')
