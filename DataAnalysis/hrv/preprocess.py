#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   plot_feats  
@Time        :   2022/1/17 7:02 下午
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt
import numpy as np
from hrvanalysis import plot_timeseries
from sklearn.preprocessing import minmax_scale

from src.constants import *
from src.sleep.constants import *
from Reader.hrv import read_ecg_file
import mne
import neurokit2 as nk

user_ids = list(start_time_bias.keys())

def visual_peaks():
    for user_id in user_ids[-3:-2]:
        path = ECG_PATH + f'{user_id}.pulse'
        baseline, data = read_ecg_file(path)
        for _res in [baseline, data]:

            ppg_signals, ppg_info = nk.ppg_process(_res, sampling_rate=hrv_samp_freq)
            # peak
            peak = ppg_info['PPG_Peaks'][3]
            plt.plot(_res[peak - 100: peak + 100])
            plt.show()

def plot_ppg():
    for user_id in user_ids[2:]:
        path = ECG_PATH + f'{user_id}.pulse'
        # path = '../../data/Pulse/p01.pulse'
        baseline, data = read_ecg_file(path)
        for _res in [baseline, data]:

            _res = _res[-60*hrv_samp_freq:]
            _res = minmax_scale(X=_res[-hrv_samp_freq*30:], feature_range=(-1, 1))
            ppg_signals, ppg_info = nk.ppg_process(_res, sampling_rate=hrv_samp_freq)

            nk.ppg_plot(ppg_signals, sampling_rate=hrv_samp_freq)
            plt.show()


def store_peaks():
    for user_id in user_ids:
        path = ECG_PATH + f'{user_id}.pulse'
        baseline, data = read_ecg_file(path)
        output_file = open(f"{PPG_PATH}/minmax/{user_id}.ppg", 'w')
        for _res in [baseline, data]:
            _minmax_res = minmax_scale(X=_res, feature_range=(-1, 1))
            ppg_signals, ppg_info = nk.ppg_process(_minmax_res, sampling_rate=hrv_samp_freq)
            _res_s = [str(_) for _ in _res]
            output_file.write(','.join(_res_s))
            output_file.write('\n')
            _peak_s = [str(_) for _ in ppg_info['PPG_Peaks']]
            output_file.write(','.join(_peak_s))
            output_file.write('\n')
        output_file.close()

        # baseline = np.array(baseline)
        # data = np.array(data)
        # baseline = baseline[-60*hrv_samp_freq:]
        # baseline = minmax_scale(X=baseline, feature_range=(-1, 1))
        # # Process it
        # ppg_signals, ppg_info = nk.ppg_process(baseline, sampling_rate=hrv_samp_freq)
        # # Visualize the processing
        # nk.ppg_plot(ppg_signals, sampling_rate=hrv_samp_freq)
        #
        # plt.plot(baseline[:hrv_samp_freq])
        # data = minmax_scale(X=data, feature_range=(-1, 1))
        # info = mne.create_info(['ecg'], hrv_samp_freq, ['ecg'])
        # ecg_raw = mne.io.RawArray(baseline.reshape([1, -1]), info)
        # ecg_raw.plot()
        # plot_timeseries(baseline)
        # plot_timeseries(data)
        # print()

if __name__ == '__main__':
    store_peaks()
    # visual_peaks()
    # plot_ppg()