#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   test_reader  
@Time        :   2021/11/26 4:22 下午
@Author      :   Xuesong Chen
@Description :   
"""
import os.path

import matplotlib

from Reader import EDFReader

# matplotlib.use('MacOSX')
matplotlib.use('TkAgg')
import numpy as np
from src.sleep.constants import *
from src.constants import *
from Reader.FIFReader import FIFReader
import mne

# plt.ion()
# user_id = 'p10'
user_id = 'p01'
# reader = EDFReader(
#     f'./data/EEGAndMusic/{user_id}-sound-1202_EEG_cleaned.edf',
#     f'/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/{user_id}-sound-1202.csv'
# )
reader = FIFReader(
    f'{FIF_PATH}/{user_id}.fif',
)
tmp_path = f'{EDF_PATH}/../edf/'
reader = EDFReader(
    f'{tmp_path}/{user_id}.edf',
    f'{LOG_PATH}/{user_id}.csv',
    offset=60 * 5,  # 5 mins
)

raw = reader.raw
print(raw.ch_names)
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
        figs = epoch.plot_psd_topomap(
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

# events, event_id = mne.events_from_annotations(
#     raw,
#     # event_id=annotation_desc_2_event_id,
#     # chunk_duration=30.
# )
# epochs = mne.Epochs(raw=raw,
#                     events=events,
#                     event_id=event_id,
#                     # tmin=0., tmax=tmax,
#                     # baseline=None
#                     )
# evoked = epochs.average()
# times = np.arange(0.05, 0.151, 0.02)
# figs = evoked.plot_topomap(times, ch_type='eeg', time_unit='s', show=False)
# # figs.show()
# figs.savefig('tmp.png')
# print()
# raw.plot_sensors(ch_type='eeg')
# raw_avg_ref = reader.raw.copy().set_eeg_reference(ref_channels='average')
# raw_avg_ref.plot(block=True)
# fig.canvas.key_press_event('a')
# anno = reader.raw.annotations
# for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
#     tmp = reader.raw.copy()
#     trail_raw = tmp.crop(tmin=onset, tmax=onset + duration, include_tmax=False)
#     trail_raw.plot()
#     break
# print()
