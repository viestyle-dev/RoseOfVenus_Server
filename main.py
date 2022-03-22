import os
import configparser
import datetime
import pandas as pd
from pythonosc import udp_client, dispatcher, osc_server
from scripts.prediction import prediction
from scripts.utils import load_model, select_model


class EEGStreamHandler:
    def __init__(self, max_count=2400):
        self.max_count = max_count
        self.left_values = []
        self.right_values = []
        self.count = 0
        self.dir_name = 'data'
        self.model = load_model(model_path)

    def handle(self, left_value, right_value):
        self.left_values.append(left_value)
        self.right_values.append(right_value)
        self.count += 1
        if self.count == self.max_count:
            # 脳波をデコーディング
            vec = prediction(self.model, self.get_values())
            # OSCで結果を送信
            send_message(vec)
            print(vec)
            # self.save()
            self.clear()

    def get_values(self):
        return pd.DataFrame(list(zip(self.left_values, self.right_values)))

    def save(self):
        file_name = 'Rawdata_' + datetime.datetime.today().strftime('%Y%m%d_%H%M%S_%f') + '.csv'
        path = os.path.join(self.dir_name, file_name)
        df = pd.DataFrame(list(zip(self.left_values, self.right_values)))
        header = ['Left Raw', 'Right Raw']
        df.to_csv(path, header=header, index=False)
        print('write to csv')

    def clear(self):
        self.left_values = []
        self.right_values = []
        self.count = 0


parser = configparser.ConfigParser()
parser.read('config.ini')
osc_client_host = parser['common']['oscClientHost']
osc_client_port = int(parser['common']['oscClientPort'])
osc_client_address = parser['common']['oscClientAddress']
osc_server_host = parser['common']['oscServerHost']
osc_server_port = int(parser['common']['oscServerPort'])
osc_server_address = parser['common']['oscServerAddress']

model_path = select_model()

eeg_stream_handler = EEGStreamHandler()


# ----- Receiver -----
def handler(addr, args, left, right):
    """ Serverで送られてきた脳波をハンドリング"""
    eeg_stream_handler.handle(left, right)


def start_server():
    """ Start server"""
    dp = dispatcher.Dispatcher()
    dp.map(osc_server_address, handler, 'left', 'right')
    server = osc_server.ThreadingOSCUDPServer((osc_server_host, osc_server_port), dp)
    server.serve_forever()


# ----- Sender -----
def send_message(values):
    """ OSCでDecodingした値を送信"""
    client = udp_client.SimpleUDPClient(osc_client_host, osc_client_port)
    client.send_message(osc_client_address, values)


if __name__ == '__main__':
    start_server()

