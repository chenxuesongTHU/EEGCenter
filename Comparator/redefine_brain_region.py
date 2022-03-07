#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   redefine_brain_region  
@Time        :   2022/3/4 3:54 下午
@Author      :   Xuesong Chen
@Description :   RQ1: 听不同声音时，根据现有的脑区划分标准，同脑区内的点位是否信号一致性保持在较高水平？
"""

from Reader import FIFReader
from src import *
from src.utils import calc_pearsonr_from_df


def calc_intra_correlation_among_brain_region():
    # #user *stimulus * #brain region
    res = pd.DataFrame()

    for user_id in user_id_list:
        reader = FIFReader(
            # f'{FIF_PATH}/{user_id}.fif',
            "../data/EEGAndMusic/p10.fif"
        )
        tag_to_desc.update({'baseline': 'baseline'})
        for stimulus_id in list(tag_to_desc.keys()):
            event_raw = reader.get_event_raw(stimulus_id)
            raw_df = event_raw.to_data_frame()
            raw_df.drop('time', axis=1, inplace=True)
            raw_df.drop('VEO', axis=1, inplace=True)
            _res = calc_pearsonr_from_df(raw_df, n_bias_samples=int(bp_samp_freq * 0.5), step=1)
            print()


calc_intra_correlation_among_brain_region()
