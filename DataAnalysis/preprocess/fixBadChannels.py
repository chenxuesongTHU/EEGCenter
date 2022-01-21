#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   fixBadChannels  
@Time        :   2022/1/5 4:05 下午
@Author      :   Xuesong Chen
@Description :   
"""
from collections import defaultdict

import pandas as pd
from Scripts.save_edf import write_mne_raw_to_edf
from Reader import EDFReader
from src.constants import *
from src.sleep.constants import *
from src.sleep.utils import get_sound_order


def read_bad_channels(file_path, user_id):
    df = pd.read_csv(file_path, encoding='GB2312')
    df = df[df['被试编号'] == user_id]
    channel_dic = {}

    for row in df.iterrows():
        stimuli = row[1]['对应声音']
        bad_channels = row[1]['电极名称']
        bad_channels = bad_channels.split()
        channel_dic[stimuli] = bad_channels

    return channel_dic

if __name__ == '__main__':
    file_path = '../../data/EEGAndMusic/bad_channels.csv'
    user_id = user_id_list[0]
    for user_id in user_id_list:
    # for user_id in ['p01', 'p02', 'p03', 'p06']:
        # user_id = 'p02'
        bad_channels = read_bad_channels(file_path, user_id)
        sound_order = get_sound_order(user_id)

        src_reader = EDFReader(
            f'{DATA_PATH}/datasets/edfV3/{user_id}.edf',
            f'{LOG_PATH}/{user_id}.csv',
            offset=60 * 5,  # 5 mins
        )

        raw = src_reader.raw
        anno = raw.annotations
        stimuli_end_time = list(anno.onset + anno.duration)
        baseline_duration = 300                                  # secs
        stimuli_end_time.insert(0, baseline_duration)            # baseline结束时间
        stimuli_end_time[-1] = raw.times[-1]                     # 最后结束时间
        res_raw = raw.copy().crop(tmin=0, tmax=stimuli_end_time[0], include_tmax=False)
        for idx, stimulus in enumerate(sound_order):
            start_time = stimuli_end_time[idx]
            end_time = stimuli_end_time[idx+1]
            tmp_raw = raw.copy().crop(tmin=start_time, tmax=end_time, include_tmax=False)
            if stimulus in bad_channels.keys():
                cur_bad_chs = bad_channels[stimulus]
                tmp_raw.info['bads'].extend(cur_bad_chs)
                tmp_raw = tmp_raw.load_data().interpolate_bads()
            res_raw.append(tmp_raw)

        res_raw.info = raw.info
        res_raw.set_annotations(raw.annotations)
        # write_mne_raw_to_edf(res_raw, f'{DATA_PATH}/datasets/edfV3/new/{user_id}.edf', overwrite=True)
        res_raw.save(f'{DATA_PATH}/datasets/fifV3/{user_id}.fif', overwrite=True)


