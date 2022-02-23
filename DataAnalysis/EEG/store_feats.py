#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   store_feats  
@Time        :   2022/2/14 6:36 下午
@Author      :   Xuesong Chen
@Description :   
"""
import os

from pandas import MultiIndex

from DataAnalysis.analyzeEventInfo import get_baseline
from Feature import TimeFrequency
from Feature.utils import remove_outliers
from Reader import FIFReader
from src.sleep.constants import *
from src.constants import *
import numpy as np
import pandas as pd
from sklearn.preprocessing import minmax_scale


def store_stimulus_level_eeg_features(reader, user_id):
    '''
    存储单个刺激级别的eeg特征
    Parameters
    ----------
    reader
    user_id

    Returns
    -------

    '''
    win_size = 30
    step_size = 5
    tag_to_desc.update({'baseline': 'baseline'})
    target_dir = 'EEG/tables'
    os.makedirs(f'{RESULTS_PATH}/{target_dir}/', exist_ok=True)
    user_info = f"{user_id}_{user_id_to_name[user_id]}"

    for sound_id, sound_name in tag_to_desc.items():
        event_raw = reader.get_event_raw(sound_id)
        tf = TimeFrequency(event_raw, win_sec=win_size, step_sec=step_size, relative=False)
        feats = tf.get_band_power(log_power=True)
        start_time = (tf.times - win_size/2).astype(int)
        end_time = (tf.times + win_size/2).astype(int)
        time_index = np.char.add(start_time.astype('str'), ['_'])
        time_index = np.char.add(time_index, end_time.astype('str'))
        time_channel_index = MultiIndex.from_product([time_index, feats[0].index],
                                                        names=['time', 'channel'])
        res = pd.DataFrame(
            index=time_channel_index,
            columns=feats[0].columns,
        )
        for time, feat_df in zip(tf.times, feats):
            start_time = int(time - win_size/2)
            end_time = int(time + win_size/2)
            res.loc[f"{start_time}_{end_time}"] = feat_df.values
        sound_info = f'{sound_id}_{sound_name}'
        res.to_csv(f'{RESULTS_PATH}/{target_dir}/{user_info}_{sound_info}.csv')


def store_whole_stage_level_eeg_features(reader, user_id):
    '''
    存储全实验阶段的eeg特征
    Parameters
    ----------
    reader
    user_id

    Returns
    -------

    '''
    win_size = 30
    step_size = 5
    tag_to_desc.update({'baseline': 'baseline'})
    target_dir = 'EEG/tables/log_power'
    os.makedirs(f'{RESULTS_PATH}/{target_dir}/', exist_ok=True)
    user_info = f"{user_id}_{user_id_to_name[user_id]}"
    raw = reader.raw.copy().crop(5 * 60, None)
    tf = TimeFrequency(raw, win_sec=win_size, step_sec=step_size, relative=False)
    feats = tf.get_band_power(log_power=True)
    start_time = (tf.times - win_size/2).astype(int)
    end_time = (tf.times + win_size/2).astype(int)
    time_index = np.char.add(start_time.astype('str'), ['_'])
    time_index = np.char.add(time_index, end_time.astype('str'))
    time_channel_index = MultiIndex.from_product([time_index, feats[0].index],
                                                    names=['time', 'channel'])
    res = pd.DataFrame(
        index=time_channel_index,
        columns=feats[0].columns,
    )
    for time, feat_df in zip(tf.times, feats):
        start_time = int(time - win_size/2)
        end_time = int(time + win_size/2)
        res.loc[f"{start_time}_{end_time}"] = feat_df.values
    sound_info = "all_sounds"
    res.to_csv(f'{RESULTS_PATH}/{target_dir}/{user_info}_{sound_info}.csv')

if __name__ == '__main__':
    for user_id in user_id_list:
        print(f"**********当前user id{user_id}**************")
        reader = FIFReader(
            f'{FIF_PATH}/{user_id}.fif',
        )
        # store_stimulus_level_eeg_features(reader, user_id)
        store_whole_stage_level_eeg_features(reader, user_id)
