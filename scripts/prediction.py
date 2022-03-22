import os
import glob
import numpy as np
import pandas as pd
from scripts.train import get_psd_from_time_series
from scripts.utils import load_model, load_data


def prediction(model, data):
    craw = len(data)
    alldata = np.empty((0, 3))
    # 左、右のみ利用
    selected_column = [0, 1]
    # 脳波データを読み込み、uVに変換
    temp_data = data.values[:, selected_column]
    temp_data = temp_data * 18.3 / 64
    # L R diff＝信号左右差を３列目に格納
    temp_data = np.hstack([temp_data, temp_data[:, [1]] - temp_data[:, [0]]])
    # 連結
    alldata = np.vstack([alldata, temp_data])
    # crawのアップデート
    craw = craw + len(temp_data)

    # 時系列データのPSDの取得
    time_window = 4  # sec
    sample_freq = 600
    # alldataから最新の４秒のデータを取得
    data2nft = alldata[-(sample_freq * time_window):]

    # PSDの計算
    spct_l = get_psd_from_time_series(data2nft, SAMPLE_FREQ_VIE=600, FreqStart=4, FreqEnd=40)

    # PSD正規化
    power_mean = np.mean(spct_l / np.sum(spct_l, axis=0), axis=1)
    # RSM計算
    c_rsm = np.corrcoef(model["MeanPower3"], power_mean)[-1][:-1]
    # 学習済み主成分空間への変換 (@は行列積の計算)
    c_vie_score = (c_rsm - model["VIEpcamu"]).T @ model["VIEcoeff"]
    # 1-7D：必要な次元のみ抜き出し
    c_vie_score = c_vie_score[0:7]
    c_vie_score_z = (c_vie_score - model["VIEscoreMu"]) / model["VIEscoreSigma"]
    # 調整
    c_vie_score_z = c_vie_score_z + abs(np.min(model["VIEscoreZ"], axis=0)) + 0.1
    c_vie_score_z = c_vie_score_z / model["maxVIEscoreZ2"]
    # max=1
    c_vie_score_z[c_vie_score_z > 1] = 1
    # min=0
    c_vie_score_z[c_vie_score_z < 0] = 0

    return c_vie_score_z.T


if __name__ == '__main__':
    data = load_data('../data/Rawdata_20220314_175740_626200.csv')
    model = load_model('../models/haruka20220317EmotionVisualizerFromRSM')
    result = prediction(model, data)
    print(result)
