#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   plotBandPowerChange  
@Time        :   2021/12/17 11:01 上午
@Author      :   Xuesong Chen
@Description :   
"""
import pandas as pd
from yasa.spectral import bandpower
from yasa.others import sliding_window
from yasa.spectral import bandpower_from_psd_ndarray
import os.path
import matplotlib.pyplot as plt
import matplotlib

from Feature import TimeFrequency
from Reader import EDFReader

# matplotlib.use('MacOSX')
matplotlib.use('TkAgg')
import numpy as np
from src.sleep.constants import *
from src.constants import *
import mne
from mne.viz.topomap import _plot_topomap_multi_cbar

def get_baseline(user_id):
    df = pd.read_csv(
        f'../data/EEGAndMusic/baseline/{user_id}.csv',
        index_col=0
    )
    return df


def plot_topomap_from_df(df, info, user_id, event):

    colorbar_range = {
        'Delta': 17.30,
        'Theta': 1.45,
        'Alpha': 1.40,
        'Sigma': 1.10,
        'Beta': 3.35,
        'Gamma': 13.20
    }

    tmin = df.index.name
    n_axes = len(bands_name)
    figs, axes = plt.subplots(1, n_axes, figsize=(2 * n_axes, 1.5))
    for ax, (key, freq_range) in zip(axes, bands_freqs.items()):
        mne.viz.plot_topomap(df[key], info, axes=ax, vmin=-colorbar_range[key], vmax=colorbar_range[key],
                             show=False)
        # _plot_topomap_multi_cbar(df[key], info, ax=ax, title=None, colorbar=True)
        ax.set_title(f'{key}({freq_range[0]}-{freq_range[1]} Hz)')

    tmax = tmin + 5
    figs.suptitle(f'{user_id}: {user_id_to_name[user_id]} \t {tag_to_desc[event]} \t time={tmin}')
    width, height = figs.get_size_inches()
    figs.set_size_inches(width, height + 0.8)
    target_path = f'../output/music_and_eeg/norm/{user_id}_{user_id_to_name[user_id]}/'
    os.makedirs(target_path, exist_ok=True)
    figs.savefig(f'{target_path}/{event}_{tag_to_desc[event]}_{tmin}_{tmax}.png')


user_id = 'p02'
stimulus = 'A1'

reader = EDFReader(
    f'../data/EEGAndMusic/{user_id}-sound-1201_EEG_cleaned.edf',
    f'/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/{user_id}-sound-1201.csv'
)

reader.raw.set_channel_types({'VEO': 'eog'})
ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
reader.raw.set_montage(ten_twenty_montage)

event_raw = reader.get_event_raw(stimulus)

info = event_raw.info
tf = TimeFrequency(event_raw, 5)
feats = tf.get_band_power()
baseline = get_baseline(user_id)

norm_feats = []
for feat in feats:
    _res = (feat - baseline) / baseline
    _res.drop(index=['VEO', 'Status'], inplace=True)
    norm_feats.append(
        _res
    )

for time, feat_df in zip(tf.times, norm_feats):
    feat_df.index.name = time
    plot_topomap_from_df(feat_df, info, user_id, stimulus)
print()

