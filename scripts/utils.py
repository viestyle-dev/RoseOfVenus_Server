import os
import glob
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog


def select_model():
    """ GUIでモデル選択(TKInterが将来使えなくなるかも)"""
    cd = os.getcwd()
    root = tk.Tk()
    path = filedialog.askdirectory(initialdir=cd)
    root.withdraw()
    return path


def load_data(path):
    return pd.read_csv(path, header=None, dtype=np.float64)


def load_model(model_dir):
    model_paths = glob.glob(os.path.join(model_dir, '*.csv'))
    model = {}
    for model_path in model_paths:
        _, filepath = os.path.split(model_path)
        filename, _ = os.path.splitext(filepath)
        model[filename] = np.loadtxt(model_path, delimiter=',')

    return model
