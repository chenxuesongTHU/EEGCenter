#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   test_reader  
@Time        :   2021/11/26 4:22 下午
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt

from Reader import BrainVisionReader
from src import *

if __name__ == '__main__':
    file_path = "/Users/cxs/project/EEGDevice/sleep data/1125-sleep data/eeg data/t01-1125.vhdr"
    reader = BrainVisionReader(file_path)

    reader.raw.pick('Fpz').plot_psd(
        # start=60,
        # duration=60,
        # picks=['FPz'],
        # scalings=dict(
        #     eeg=1e-4, resp=1e3, eog=1e-4, emg=1e-7,
        #               misc=1e-1)
    )
    plt.show()
    print()
