#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   plotBandPowerChange  
@Time        :   2021/12/17 11:01 上午
@Author      :   Xuesong Chen
@Description :   
"""
import sys

import pandas as pd
from yasa.spectral import bandpower
from yasa.others import sliding_window
from yasa.spectral import bandpower_from_psd_ndarray
import os.path
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

from Feature import TimeFrequency
from Feature.utils import remove_outliers
from Reader import EDFReader

# matplotlib.use('MacOSX')
matplotlib.use('TkAgg')
import numpy as np
from src.sleep.constants import *
from src.constants import *
import mne
from mne.viz.topomap import _plot_topomap_multi_cbar
from collections import defaultdict
from src.sleep.utils import get_user_ratings

def get_baseline(user_id):
    df = pd.read_csv(
        f'../data/EEGAndMusic/baseline/{user_id}.csv',
        index_col=0
    )
    return df


def plot_topomap_from_df(df, info, user_id, event, win_size):

    # colorbar_range由全过程的raw图像的变化范围决定，
    # 为了保证不同band间由可比性，每个值的正负范围需相等。
    colorbar_range = {
        'Delta': 10,
        'Theta': 4,
        'Alpha': 2,
        'Sigma': 2,
        'Beta': 2,
        'Gamma': 6
    }

    tmin = df.index.name
    n_axes = len(bands_name)
    figs, axes = plt.subplots(1, n_axes, figsize=(2 * n_axes, 1.5))
    colorbar_info = defaultdict(lambda: [])
    for ax, (key, freq_range) in zip(axes, bands_freqs.items()):
        mne.viz.plot_topomap(df[key], info, axes=ax,
                             vmin=-colorbar_range[key], vmax=colorbar_range[key],
                             show=False)
        # _plot_topomap_multi_cbar(df[key], info, ax=ax, title=None, colorbar=True)
        ax.set_title(f'{key}({freq_range[0]}-{freq_range[1]} Hz)')

    tmax = tmin + win_size
    figs.suptitle(f'{user_id}: {user_id_to_name[user_id]} \t {tag_to_desc[event]} \t time={tmin}')
    width, height = figs.get_size_inches()
    figs.set_size_inches(width, height + 0.8)
    target_path = f'../output/music_and_eeg/norm/{user_id}_{user_id_to_name[user_id]}/img/'
    os.makedirs(target_path, exist_ok=True)
    figs.savefig(f'{target_path}/{event}_{tag_to_desc[event]}_{tmin}_{tmax}.png')


def plot_dynamic_topomap(win_size):
    # todo: 参数传递
    for time, feat_df in zip(tf.times, norm_feats):
        feat_df.index.name = time-win_size/2
        plot_topomap_from_df(feat_df, info, user_id, stimulus, win_size)


def plot_span(anno, ax, user_id):
    idx = 0
    for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
        task_start_pos = onset              # 单位为s
        task_end_pos = onset + duration     # 单位为s
        relax_start_pos = task_end_pos
        relax_end_pos = relax_start_pos + 60 * 3
        ax.axvspan(task_start_pos, task_end_pos, facecolor='#458CC4', alpha=0.2)
        ax.axvspan(relax_start_pos, relax_end_pos, facecolor='#A6A6A6', alpha=0.2)
        res = get_user_ratings(user_id)
        _l = res[idx+1]
        sound_name = tag_to_desc[_l['标号']]
        s = f"\t{sound_name} \n 困倦:{_l['困倦']} 熟悉:{_l['熟悉']} 喜爱:{_l['喜爱']}"
        x = task_start_pos
        y = ax.viewLim.ymax- 0.2 * (ax.viewLim.ymax- ax.viewLim.ymin)
        ax.text(x, y, s)
        idx += 1



user_id = 'p03'
stimulus = 'A1'

reader = EDFReader(
    f'../data/EEGAndMusic/{user_id}-sound-1201_EEG_cleaned.edf',
    f'/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/{user_id}-sound-1201.csv',
    offset=60*5, # 5 mins
)

reader.raw.set_channel_types({'VEO': 'eog'})
ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
reader.raw.set_montage(ten_twenty_montage)

event_raw = reader.get_event_raw(stimulus)

info = event_raw.info
tf = TimeFrequency(reader.raw,  win_sec=4, relative=False)   # todo
# tf = TimeFrequency(event_raw,  win_sec=5, relative=False, mode='psd')   # todo
# tf = TimeFrequency(reader.raw, 5, relative=False)
feats = tf.get_band_power()
baseline = get_baseline(user_id)

norm_feats = []
for feat in feats:
    _res = (feat - baseline) / baseline
    _res.drop(index=['VEO', 'Status'], inplace=True)
    _res = _res.loc[occipital_region]               # 仅使用枕区
    norm_feats.append(
        _res
    )
#
# for time, feat_df in zip(tf.times, norm_feats):
#     feat_df.index.name = time
#     plot_topomap_from_df(feat_df, info, user_id, stimulus)
# print()
#
# plot_dynamic_topomap(win_size=5)
# sys.exit(0)

plot_targets = defaultdict(lambda: [])
plot_targets_df = pd.DataFrame(columns=bands_name)
cut_off_percent = 0 # cut off total = cut_off_percent * 2

for time_slot_feat in norm_feats:
    n_channels = len(time_slot_feat)
    cut_off_channels = int(cut_off_percent * n_channels)
    for band in bands_name:
        if cut_off_percent == 0:
            _list = np.sort(time_slot_feat[band])
        else:
            _list = np.sort(time_slot_feat[band])[cut_off_channels: -cut_off_channels]
        _avg = np.average(_list)
        plot_targets[band].append(_avg)

# 将 3 sigma外的数值替换为均值
for band in bands_name:
    sigma = np.std(plot_targets[band])
    mu = np.mean(plot_targets[band])
    for _idx, _v in enumerate(plot_targets[band]):
        if _v < (mu - 3*sigma) or _v > (mu + 3*sigma):
            plot_targets[band][_idx] = mu

# time * bands
data = pd.DataFrame(columns=plot_targets.keys(), data=np.array(list(plot_targets.values())).T)
data.index = tf.times

rolling_length = 15
rolling_start_idx = rolling_length-1
data = data.rolling(rolling_length).mean()
for idx in range(rolling_start_idx):
    data.iloc[idx, :] = data.iloc[rolling_start_idx, :]

# z score
# from scipy import stats
# _data = stats.zscore(data, axis=0)
# data = pd.DataFrame(_data, index=data.index, columns=data.columns)

interest_band_list = [
    bands_name,
    ["Delta", "Theta", "Gamma"],
    ["Alpha", 'Sigma', 'Beta'],
]
for band in bands_name:
    interest_band_list.append([band])
# interest_band = ["Alpha", 'Sigma', 'Beta']
for interest_band in interest_band_list:
    fig, axes = plt.subplots(figsize=(25, 8))
    sns.lineplot(data=data[interest_band])
    # axes.set_xticks(tf.times)
    plot_span(reader.raw.annotations, axes, user_id)
    root_path = f'../output/music_and_eeg/norm/{user_id}_{user_id_to_name[user_id]}/'
    os.makedirs(root_path, exist_ok=True)
    file_name = '_'.join(interest_band)
    plt.savefig(f"{root_path}/{file_name}.pdf", format='pdf')

