# EEG Server

## 実行手順

### 1: 環境構築
Pythonの実行環境を用意します。Python3.8.6で動作テストしております。
関連するライブラリをインストールします。

```.sh
git clone git@github.com:viestyle-dev/EEGServer.git

cd EEGViewer

python3 -m venv .venv

source .venv/bin/activate

pip install -U pip

pip install -r requirements.txt
```

### 1: 設定を変更
設定は `config.ini` ファイルを修正して行います。
oscClientHostにiPadのIPアドレス、oscServerHostにPCのIPアドレスを入力します。

```.ini
[common]
# iPadのIPアドレスとポート
oscClientHost = 192.168.xxx.xxx
oscClientPort = 12400
oscClientAddress = /decoding
# PCのIPアドレスとポート
oscServerHost = 192.168.xxx.xxx
oscServerPort = 10000
oscServerAddress = /brain
```

### 2: 実行
以下のコマンドを実行してiPadから送られてくるデータを待ち受けます。

```.sh
python main.py
```
