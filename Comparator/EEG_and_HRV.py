#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   EEG_and_HRV  
@Time        :   2022/2/15 3:39 下午
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr

from FeatureLoader import EEGLoader, HRVLoader
from src import *
channel_names.remove('VEO')
tag_to_desc.update({'baseline': 'baseline'})
user_id_list = list(start_time_bias.keys())


def calc_correlation():
    for user_id in user_id_list:
        eeg_feat = pd.DataFrame()
        hrv_feat = pd.DataFrame()
        for stimuli_id in tag_to_desc.keys():
            eeg_loader = EEGLoader(user_id, stimuli_id)
            hrv_loader = HRVLoader(user_id, stimuli_id)
            cur_eeg_feat = eeg_loader.get_power(bands=bands_name, channels=channel_names, method="mean")
            cur_hrv_feat = hrv_loader.get_all_features()
            eeg_feat = pd.concat([eeg_feat, cur_eeg_feat])
            hrv_feat = pd.concat([hrv_feat, cur_hrv_feat])
        correlation_df = pd.DataFrame(index=eeg_feat.columns, columns=hrv_feat.columns)
        for eeg_feat_name in list(eeg_feat.columns):
            for hrv_feat_name in list(hrv_feat.columns):
                _pearson_val = pearsonr(
                    eeg_feat[eeg_feat_name], hrv_feat[hrv_feat_name]
                )[0]
                if _pearson_val >= 0.2:
                    correlation_df.at[eeg_feat_name, hrv_feat_name] = _pearson_val
        correlation_df.to_csv(f"{RESULTS_PATH}/EEG_HRV_correlation/{user_id}.csv")


def plot_specific_stimulus(user_id, stimuli_id, eeg_feat, hrv_feat):
    eeg_loader = EEGLoader(user_id, stimuli_id)
    hrv_loader = HRVLoader(user_id, stimuli_id)
    cur_eeg_feat = eeg_loader.get_power(bands=[eeg_feat], channels=channel_names, method="mean")
    cur_hrv_feat = hrv_loader.get_specific_feature(hrv_feat)
    cur_eeg_feat.plot()
    plt.show()
    cur_hrv_feat.plot()
    plt.show()

plot_specific_stimulus('p10', 'A1', 'Gamma', 'HRV_SDNN')

