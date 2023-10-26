# スネークゲーム

### 本リポジトリはCUI上で動作するスネークゲームのソースコード一式を保管するリポジトリです。
#### ※本リポジトリのURLは[こちら](https://github.com/NatsukiShimizu/snake_game)を参照

## ■ 動作環境
#### 以下の環境で動作することを確認済み
* OS : Windows11 (WSL : 22.04-LTS)
* Pythonバージョン : 3.11

## ■ 各種手順
### 1. 本リポジトリのクローン方法
### 以下のコマンドで本リポジトリをクローンする
#### **※事前にSSHキーの設定が必要**
```
git clone git@github.com:NatsukiShimizu/snake_game.git ./snake_game
```

### 2. スネークゲームの起動方法
### 以下のコマンドでスネークゲームを起動する
#### **※事前に1の手順を実施すること**
```
cd snake_game
python3 main_func_only.py
```

## ※ **本ゲームを作成した理由** ※
* **動機**
<br>pythonの学習をするにあたり、進捗が見て分かるゲームであれば学習速度が早いのではないかと判断したため。

* **Cursesを用いた理由**
<br>CUIアプリケーションを作成する上で学習する用に今回はCursesを利用。
