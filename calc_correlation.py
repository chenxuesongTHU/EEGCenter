#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   calc_correlation  
@Time        :   2021/12/15 10:40 上午
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib
import matplotlib.pyplot as plt
import mne
import numpy as np
from scipy.stats import pearsonr

from Reader import AcousticReader
from Reader import EDFReader

matplotlib.use('TkAgg')
from scipy import stats

stimulus = 'B1'
sound_reader = AcousticReader(f'./data/acoustics/{stimulus}.wav')

eeg_reader = EDFReader(
    './data/EEGAndMusic/p02-sound-1201_EEG_cleaned.edf',
    '/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/p02-sound-1201.csv'
)

event_raw = eeg_reader.get_event_raw(stimulus)
single_eeg = event_raw.get_data(picks='FT9').squeeze()
single_eeg_2 = event_raw.get_data(picks='T7').squeeze()
single_eeg_3 = event_raw.get_data(picks='TP7').squeeze()

event_raw = event_raw.pick(picks=['FT9', 'T7', 'TP7']).copy()

info = mne.create_info(['acoustic'], 100, ['eeg'])
acoustic_raw = mne.io.RawArray(np.reshape(sound_reader.acoustic, [1, -1]), info)
acoustic_raw = acoustic_raw.filter(l_freq=0.1, h_freq=40)
duration = acoustic_raw.last_samp / acoustic_raw.info['sfreq']
event_raw.crop(0, duration)
event_raw.add_channels([acoustic_raw])

total_info = mne.create_info(
    event_raw.ch_names,
    event_raw.info['sfreq'],
    ['eeg'] * 4,
)
arr = []
for ch_name in event_raw.ch_names:
    arr.append(
        stats.zscore(event_raw[ch_name][0], axis=1)
    )
arr = np.array(arr).squeeze()

total_raw = mne.io.RawArray(arr, total_info)
total_raw.plot(
    order=[1, 0, 3, 2],
    show_scalebars=True,
    scalings=dict(eeg=1)
)
tmp = stats.zscore(event_raw['FT9'][0], axis=1)

# event_raw.plot()

# acoustic_raw.plot()
n_diff_length = single_eeg.shape[0] - sound_reader.acoustic.shape[0]
start_bias = int(n_diff_length / 2)
sound_reader.acoustic = acoustic_raw.get_data(picks='acoustic').squeeze()
for start_bias in range(n_diff_length):
    print(
        start_bias, ': ',
        pearsonr(single_eeg[start_bias:start_bias + sound_reader.acoustic.shape[0]], sound_reader.acoustic)
    )

# plt.plot(single_eeg[:200])
# plt.plot(sound_reader.acoustic[:200])
# plt.show()

# print()

# 开启一个窗口，num设置子图数量，这里如果在add_subplot里写了子图数量，num设置多少就没影响了
# figsize设置窗口大小，dpi设置分辨率
fig = plt.figure(num=2, figsize=(20, 8), dpi=80)
# 使用add_subplot在窗口加子图，其本质就是添加坐标系
# 三个参数分别为：行数，列数，本子图是所有子图中的第几个，最后一个参数设置错了子图可能发生重叠
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
# 绘制曲线
ax1.plot(single_eeg[:800], color='g')
# 同理，在同一个坐标系ax1上绘图，可以在ax1坐标系上画两条曲线，实现跟上一段代码一样的效果
# ax1.plot(sound_reader.acoustic[:200], color='b')
# 在第二个子图上画图
ax2.plot(sound_reader.acoustic[:800], color='r')
plt.show()
