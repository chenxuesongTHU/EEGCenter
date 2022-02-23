#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   AllSound  
@Time        :   2022/2/22 2:34 下午
@Author      :   Xuesong Chen
@Description :   
"""
import seaborn as sns
from scipy.stats import pearsonr

from DataAnalysis.Visualization.utils import plot_span
from FeatureLoader import EEGLoader, HRVLoader
from Reader.Annotation import csvAnnotation
from src import *


def nan_pearsonr(x, y):
    x = np.array(x)
    y = np.array(y)
    x[np.where(np.isinf(x))] = np.nan
    y[np.where(np.isinf(y))] = np.nan
    nan_idx_x = np.argwhere(np.isnan(x))
    nan_idx_y = np.argwhere(np.isnan(y))
    nan_idx = np.vstack([nan_idx_x, nan_idx_y]).squeeze()
    x = np.delete(x, nan_idx)
    y = np.delete(y, nan_idx)
    return pearsonr(x, y)


def plot_feat_change():
    signal_type = 'eeg'
    # signal_type = 'ppg'
    # interest_feat = ['HRV_pNN50', 'HRV_pNN20']
    interest_feat = bands_name

    for user_id in hrv_user_id_list:

        csv_file_path = f'{PPG_PATH}/{user_id}.csv'
        anno = csvAnnotation(csv_file_path).annotation
        stimuli = 'all'
        if signal_type == "eeg":
            loader = EEGLoader(user_id, stimuli)
            cur_feat = loader.get_power(bands=bands_name, channels=channel_names, method="mean")
        if signal_type == 'ppg':
            loader = HRVLoader(user_id, stimuli)
            cur_feat = loader.get_all_features()
        [first_samp_start_time, first_samp_end_time] = cur_feat.index[0].split('_')
        first_samp_start_time = int(first_samp_start_time)
        first_samp_end_time = int(first_samp_end_time)
        win_size = int(first_samp_end_time - first_samp_start_time)
        step = int(cur_feat.index[1].split('_')[0]) - int(cur_feat.index[0].split('_')[0])
        end_time = int(win_size / 2) + step * len(cur_feat.index)
        time_idx = list(np.arange(int(win_size / 2), end_time, step))
        cur_feat.index = time_idx
        fig, axes = plt.subplots(figsize=(25, 8))
        cur_feat = smooth_dataframe(cur_feat, rolling_length=7)
        sns.lineplot(data=cur_feat[interest_feat])
        # axes.set_xticks(tf.times)
        plot_span(anno, axes, user_id)
        plt.show()
        print()


def calc_correlation():
    stimuli = "all"
    for user_id in hrv_user_id_list:
        # for user_id in ['p03']:
        eeg_loader = EEGLoader(user_id, stimuli)
        eeg_feat = eeg_loader.get_power(bands=bands_name, channels=channel_names, method="mean")
        hrv_loader = HRVLoader(user_id, stimuli)
        hrv_feat = hrv_loader.get_all_features()
        correlation_df = pd.DataFrame(index=eeg_feat.columns, columns=hrv_feat.columns)
        total = 0
        sig_n = 0
        for eeg_feat_name in list(eeg_feat.columns):
            for hrv_feat_name in list(hrv_feat.columns):
                _pearson_val = nan_pearsonr(
                    eeg_feat[eeg_feat_name], hrv_feat[hrv_feat_name]
                )[0]
                total += 1
                if abs(_pearson_val) >= 0.2:
                    correlation_df.at[eeg_feat_name, hrv_feat_name] = _pearson_val
                    sig_n += 1
        print(user_id, sig_n/total)
        correlation_df.to_csv(f"{RESULTS_PATH}/EEG_HRV_correlation/{user_id}.csv")


def calc_single_type_signal_correlation():
    stimuli = 'all'
    for user_id in user_id_list:
        loader = EEGLoader(user_id, stimuli)
        cur_feat = loader.get_power(bands=bands_name, channels=channel_names, method="mean")
        correlation_df = pd.DataFrame(index=cur_feat.columns, columns=cur_feat.columns)
        for eeg_feat_name in list(cur_feat.columns):
            for hrv_feat_name in list(cur_feat.columns):
                _pearson_val = nan_pearsonr(
                    cur_feat[eeg_feat_name], cur_feat[hrv_feat_name]
                )[0]
                # if abs(_pearson_val) >= 0.2:
                correlation_df.at[eeg_feat_name, hrv_feat_name] = _pearson_val
        correlation_df.to_csv(f"{RESULTS_PATH}/EEG/tables/correlation/p>=0.2_{user_id}.csv")

    for user_id in hrv_user_id_list:
        loader = HRVLoader(user_id, stimuli)
        cur_feat = loader.get_all_features()
        correlation_df = pd.DataFrame(index=cur_feat.columns, columns=cur_feat.columns)
        for eeg_feat_name in list(cur_feat.columns):
            for hrv_feat_name in list(cur_feat.columns):
                _pearson_val = nan_pearsonr(
                    cur_feat[eeg_feat_name], cur_feat[hrv_feat_name]
                )[0]
                if abs(_pearson_val) >= 0.2:
                    correlation_df.at[eeg_feat_name, hrv_feat_name] = _pearson_val
        correlation_df.to_csv(f"{RESULTS_PATH}/hrv/tables/correlation/p>=0.2_{user_id}.csv")


if __name__ == '__main__':
    calc_correlation()
    # calc_single_type_signal_correlation()
