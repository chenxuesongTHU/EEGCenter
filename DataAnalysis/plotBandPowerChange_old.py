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

import matplotlib

from Reader import EDFReader

# matplotlib.use('MacOSX')
matplotlib.use('TkAgg')
import numpy as np
from src.sleep.constants import *
import mne

def get_baseline(user_id):
    df = pd.read_csv(
        f'../data/EEGAndMusic/baseline/{user_id}.csv',
        index_col=0
    )
    return df

# plt.ion()
# user_id = 'p10'
user_id = 'p03'
reader = EDFReader(
    f'../data/EEGAndMusic/{user_id}-sound-1202_EEG_cleaned.edf',
    f'/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/{user_id}-sound-1202.csv'
)

raw = reader.raw

baseline = get_baseline(user_id)

print(raw.ch_names)

raw_data = raw.get_data()
# raw_data
raw.set_channel_types({'VEO': 'eog'})
ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(ten_twenty_montage)
anno = raw.annotations
events, event_id = mne.events_from_annotations(
    raw,
    # chunk_duration=60*5
)

total_secs = 300
win_duration = 5
n_wins = int(300 / win_duration)

epochs = mne.Epochs(
    raw=raw,
    events=events,
    event_id=event_id,
    tmin=0., tmax=total_secs,
    baseline=(0, 0)
)

for epoch_idx in range(epochs.events.shape[0]):
    epoch = epochs[epoch_idx]
    event = list(epoch.event_id.keys())[0]
    desc = anno.description[epoch_idx]
    assert event == desc
    onset = anno.onset[epoch_idx]
    duration = anno.onset[epoch_idx]
    for win_idx in range(n_wins):
        tmin = win_idx * win_duration
        tmax = (win_idx+1) * win_duration
        figs = epoch.plot_topomap(
            # ch_type='grad',
            tmin=tmin,
            tmax=tmax,
            normalize=True,
            show=False,
            dB=True,
            vlim=(0, 0.3),
            # outlines='skirt',
        )
        figs.suptitle(f'{user_id}: {user_id_to_name[user_id]} \t {tag_to_desc[event]} \t time={tmin}')
        width, height = figs.get_size_inches()
        figs.set_size_inches(width, height + 0.8)
        target_path = f'./output/music_and_eeg/{user_id}_{user_id_to_name[user_id]}/'
        os.makedirs(target_path, exist_ok=True)
        figs.savefig(f'{target_path}/{event}_{tag_to_desc[event]}_{tmin}_{tmax}.png')
