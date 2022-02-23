#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   plot_feat_change  
@Time        :   2022/1/24 3:01 下午
@Author      :   Xuesong Chen
@Description :   
"""
import os

import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np
import pandas as pd
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values
from sklearn.preprocessing import minmax_scale

from DataAnalysis.hrv.utils import get_1d_peak_by_annotation, get_1d_data_by_annotation
from Reader.Annotation import csvAnnotation
from Reader.hrv import read_ppg_and_peak
from src.constants import *
from src.sleep.constants import *
from src.sleep.utils import get_user_ratings, get_sound_order
from neurokit2.hrv.hrv_utils import _hrv_get_rri

user_id_list = list(start_time_bias.keys())
user_id_list = hrv_user_id_list[-2:] + ['p15', 'p17']
user_id_list = ['p17']
plt.rcParams['figure.figsize'] = [14, 11]  # Bigger images


def remove_outliers_and_ectopic_beats(peaks, samp_freq, rm_ectopic_beats=True):

    # convert peaks to rr intervals in ms
    rr_intervals_list, _ = _hrv_get_rri(peaks, samp_freq, interpolate=False)

    # 按照异常值的固定值删除数据
    rr_intervals_without_outliers = remove_outliers(rr_intervals=rr_intervals_list,
                                                    low_rri=300, high_rri=2000)
    # This replace outliers nan values with linear interpolation
    interpolated_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
                                                       interpolation_method="linear")

    # 按照分布删除数据
    outliers_mask = nk.find_outliers(interpolated_intervals, exclude=0.05)
    nan_count = np.sum(outliers_mask)
    if nan_count == 0:
        print("{} outlier(s) have been deleted.".format(nan_count))
    else:
        print("{} outlier(s) have been deleted.".format(nan_count))
    _interpolated_intervals = np.where(outliers_mask, np.nan, interpolated_intervals)
    _interpolated_intervals = interpolate_nan_values(rr_intervals=_interpolated_intervals)
    interpolated_intervals = np.where(np.isnan(_interpolated_intervals), np.nanmean(_interpolated_intervals), _interpolated_intervals)
    # 按照ectopic_beats的标准删除数据
    if rm_ectopic_beats:
        # This remove ectopic beats from signal
        nn_intervals_list = remove_ectopic_beats(rr_intervals=interpolated_intervals, method="malik")
        # This replace ectopic beats nan values with linear interpolation
        interpolated_intervals = interpolate_nan_values(rr_intervals=nn_intervals_list)

    # convert rr intervals in ms to peaks
    res_peaks = nk.intervals_to_peaks(
        np.array(interpolated_intervals) * samp_freq / 1000
    ) + peaks[0]
    # np.sum(res_peaks == peaks) / len(res_peaks)
    return res_peaks


def plot_hrv_feat_base_all_stimuli():
    # 从整个实验过程中找peak，然后提取特征并可视化
    for user_id in user_id_list[-1:]:
        print(f"**********当前用户：{user_id}***********")
        ppg_file_path = f'{PPG_PATH}/minmax/{user_id}.ppg'
        csv_file_path = f'{PPG_PATH}/{user_id}.csv'
        baseline, data = read_ppg_and_peak(ppg_file_path)
        anno = csvAnnotation(csv_file_path)
        baseline_hrv_feats = nk.hrv(baseline['peak'], sampling_rate=hrv_samp_freq, show=True)
        user_info = f"{user_id}_{user_id_to_name[user_id]}"
        plt.suptitle(f'{user_info} baseline')
        plt.savefig(f"{RESULTS_PATH}/hrv/{user_id}_{user_id_to_name[user_id]}_baseline.pdf", format="pdf")

        for sound_id, sound_name in tag_to_desc.items():
            _data = get_1d_peak_by_annotation(data['peak'], anno, sound_id)
            if _data == []:
                print(user_id, sound_id, '无peak信息')
                continue
            cur_feat = nk.hrv(_data, sampling_rate=hrv_samp_freq, show=True)
            sound_info = f"{sound_id}_{sound_name}"

            _rating_dic = get_user_ratings(user_id, sound_id)
            rating_info = f"困倦:{_rating_dic['困倦']} 熟悉:{_rating_dic['熟悉']} 喜爱:{_rating_dic['喜爱']}"

            plt.suptitle(f'{user_info} {sound_info} {rating_info}')
            plt.savefig(f"{RESULTS_PATH}/hrv/{user_info} {sound_info}.pdf", format="pdf")
            plt.close()


def plot_hrv_feat_base_single_stimuli():
    '''
    同一个用户，同一个刺激下，在同一张图中画三种类型的特征。

    ATTENTION:
        如果采用rm_outliers的话，会对interval存在的异常值进行插值重建，导致整体的时间长度会变化。

    Returns
    -------

    '''
    target_dir = 'remove_outliers'
    os.makedirs(f'{RESULTS_PATH}/hrv/{target_dir}/', exist_ok=True)
    os.makedirs(f'{RESULTS_PATH}/hrv/{target_dir}/tables/', exist_ok=True)
    rm_ectopic_beats = False
    for user_id in user_id_list:
        print(f"**********当前用户：{user_id}***********")
        ppg_file_path = f'{PPG_PATH}/minmax/{user_id}.ppg'
        csv_file_path = f'{PPG_PATH}/{user_id}.csv'
        baseline, data = read_ppg_and_peak(ppg_file_path)
        anno = csvAnnotation(csv_file_path)
        baseline = minmax_scale(X=baseline['data'], feature_range=(-1, 1))
        ppg_signals, ppg_info = nk.ppg_process(baseline, sampling_rate=hrv_samp_freq)

        ppg_peaks = remove_outliers_and_ectopic_beats(ppg_info["PPG_Peaks"], hrv_samp_freq, rm_ectopic_beats=rm_ectopic_beats)

        baseline_hrv_feats = nk.hrv(ppg_peaks, sampling_rate=hrv_samp_freq, show=True)
        baseline_hrv_feats.index = ['baseline']
        user_feats = baseline_hrv_feats
        user_info = f"{user_id}_{user_id_to_name[user_id]}"
        plt.suptitle(f'{user_info} baseline')
        plt.savefig(f"{RESULTS_PATH}/hrv/{target_dir}/{user_id}_{user_id_to_name[user_id]}_baseline.pdf",
                    format="pdf")
        sound_order = get_sound_order(user_id)
        for sound_id in sound_order:
            sound_name = tag_to_desc[sound_id]
            _data = get_1d_data_by_annotation(data['data'], anno, sound_id)
            if _data == []:
                print(user_id, sound_id, '无peak信息')
                continue
            _data = minmax_scale(X=_data, feature_range=(-1, 1))
            ppg_signals, ppg_info = nk.ppg_process(_data, sampling_rate=hrv_samp_freq)
            ppg_peaks = remove_outliers_and_ectopic_beats(ppg_info["PPG_Peaks"], hrv_samp_freq, rm_ectopic_beats=rm_ectopic_beats)
            cur_feat = nk.hrv(ppg_peaks, sampling_rate=hrv_samp_freq, show=True)
            sound_info = f"{sound_id}_{sound_name}"
            _rating_dic = get_user_ratings(user_id, sound_id)
            rating_info = f"困倦:{_rating_dic['困倦']} 熟悉:{_rating_dic['熟悉']} 喜爱:{_rating_dic['喜爱']}"
            cur_feat.index = [sound_info]
            user_feats = pd.concat([user_feats, cur_feat])

            plt.suptitle(f'{user_info} {sound_info} {rating_info}')
            plt.savefig(f"{RESULTS_PATH}/hrv/{target_dir}/{user_info} {sound_info}.pdf", format="pdf")
            plt.close()
        user_feats.to_csv(f'{RESULTS_PATH}/hrv/{target_dir}/tables/{user_info}.csv')


def plot_hrv_feat_across_stimuli():
    '''
    同一个用户，不同刺激下，同一张图中画一个类型的特征。

    Returns
    -------

    '''
    target_dir = 'across_stimuli'
    os.makedirs(f'{RESULTS_PATH}/hrv/{target_dir}/', exist_ok=True)
    rm_ectopic_beats = False
    # ['time', 'frequency', 'nonlinear']
    for feat_type in ['nonlinear']:
        for user_id in user_id_list:
            print(f"**********当前用户：{user_id}***********")
            ppg_file_path = f'{PPG_PATH}/minmax/{user_id}.ppg'
            csv_file_path = f'{PPG_PATH}/{user_id}.csv'
            baseline, data = read_ppg_and_peak(ppg_file_path)
            anno = csvAnnotation(csv_file_path)
            # plot settings
            subplot_kw = {}
            nrows = 2
            ncols = 5
            subplot_kw = {}
            if feat_type == "nonlinear":
                subplot_kw = {'aspect': 'equal'}
            figure, axes = plt.subplots(
                figsize=(15, 6),
                nrows=nrows, ncols=ncols, sharex=True, sharey=True,
                constrained_layout=True, subplot_kw=subplot_kw
            )

            baseline = minmax_scale(X=baseline['data'], feature_range=(-1, 1))
            ppg_signals, ppg_info = nk.ppg_process(baseline, sampling_rate=hrv_samp_freq)

            ppg_peaks = remove_outliers_and_ectopic_beats(ppg_info["PPG_Peaks"], hrv_samp_freq, rm_ectopic_beats=rm_ectopic_beats)

            ax = axes[0, 0]
            if feat_type == "time":
                baseline_hrv_feats = nk.hrv_time(ppg_peaks, sampling_rate=hrv_samp_freq, show=True, ax=ax)
            elif feat_type == "frequency":
                baseline_hrv_feats = nk.hrv_frequency(ppg_peaks, sampling_rate=hrv_samp_freq, show=True, ax=ax)
            elif feat_type == "nonlinear":
                baseline_hrv_feats = nk.hrv_nonlinear(ppg_peaks, sampling_rate=hrv_samp_freq, show=True, ax=ax)

            user_info = f"{user_id}_{user_id_to_name[user_id]}"
            ax.set_aspect('equal')
            ax.set_title(f'baseline')
            # plt.savefig(f"{RESULTS_PATH}/hrv/{target_dir}/{user_id}_{user_id_to_name[user_id]}_baseline.pdf",
            #             format="pdf")

            for sound_id, sound_name in tag_to_desc.items():
                if sound_id == 'B2':
                    print()
                (type_id, seq_id) = list(sound_id)
                row_idx = 0
                if type_id == 'B':
                    row_idx = 1
                col_idx = int(seq_id)
                ax = axes[row_idx, col_idx]

                _data = get_1d_data_by_annotation(data['data'], anno, sound_id)
                if _data == []:
                    print(user_id, sound_id, '无peak信息')
                    continue
                _data = minmax_scale(X=_data, feature_range=(-1, 1))
                ppg_signals, ppg_info = nk.ppg_process(_data, sampling_rate=hrv_samp_freq)
                ppg_peaks = remove_outliers_and_ectopic_beats(ppg_info["PPG_Peaks"], hrv_samp_freq, rm_ectopic_beats=rm_ectopic_beats)

                if feat_type == "time":
                    cur_feat = nk.hrv_time(ppg_peaks, sampling_rate=hrv_samp_freq, show=True, ax=ax)
                elif feat_type == "frequency":
                    cur_feat = nk.hrv_frequency(ppg_peaks, sampling_rate=hrv_samp_freq, show=True, ax=ax)
                elif feat_type == "nonlinear":
                    cur_feat = nk.hrv_nonlinear(ppg_peaks, sampling_rate=hrv_samp_freq, show=True, ax=ax)

                sound_info = f"{sound_id}_{sound_name}"
                _rating_dic = get_user_ratings(user_id, sound_id)
                rating_info = f"困倦:{_rating_dic['困倦']} 熟 悉:{_rating_dic['熟悉']} 喜爱:{_rating_dic['喜爱']}"
                ax.set_aspect('equal')
                ax.set_title(f'{sound_info} \n {rating_info}')
            plt.suptitle(user_info)
            ax.set_aspect('equal')
            plt.savefig(f"{RESULTS_PATH}/hrv/{target_dir}/{user_info} {feat_type}.pdf", format="pdf")
            plt.close()


def store_hrv_feat():
    '''
    存储stimulus级别的hrv特征
    Returns
    -------

    '''
    from yasa.others import sliding_window

    target_dir = 'tables/time_domain_feats'
    os.makedirs(f'{RESULTS_PATH}/hrv/{target_dir}/', exist_ok=True)
    rm_ectopic_beats = False
    win_size = 30 # 单位为s
    step_size = 5
    for user_id in user_id_list:
        print(f"**********当前用户：{user_id}***********")
        ppg_file_path = f'{PPG_PATH}/minmax/{user_id}.ppg'
        csv_file_path = f'{PPG_PATH}/{user_id}.csv'
        baseline, data = read_ppg_and_peak(ppg_file_path)
        anno = csvAnnotation(csv_file_path)
        user_info = f"{user_id}_{user_id_to_name[user_id]}"

        times, epochs = sliding_window(np.array(baseline['data']), sf=hrv_samp_freq, window=win_size, step=step_size)
        all_feat = pd.DataFrame()
        for _time, _epoch in zip(times, epochs):
            _epoch = minmax_scale(X=_epoch, feature_range=(-1, 1))
            ppg_signals, ppg_info = nk.ppg_process(_epoch, sampling_rate=hrv_samp_freq)
            # nk.ppg_plot(ppg_signals, sampling_rate=hrv_samp_freq)
            ppg_peaks = remove_outliers_and_ectopic_beats(ppg_info["PPG_Peaks"], hrv_samp_freq, rm_ectopic_beats=rm_ectopic_beats)

            _feat = None
            _feat = nk.hrv(ppg_peaks, sampling_rate=hrv_samp_freq, show=False)
            _time = int(_time)
            _feat.index = [f"{_time}-{_time+win_size}"]
            all_feat = pd.concat([all_feat, _feat])
        all_feat.to_csv(f'{RESULTS_PATH}/hrv/{target_dir}/{user_info}_baseline.csv')

        for sound_id, sound_name in tag_to_desc.items():
            _data = get_1d_data_by_annotation(np.array(data['data']), anno, sound_id)
            if _data == []:
                print(user_id, sound_id, '无peak信息')
                continue

            times, epochs = sliding_window(_data, sf=hrv_samp_freq, window=win_size, step=step_size)
            all_feat = pd.DataFrame()
            for _time, _epoch in zip(times, epochs):
                _epoch = minmax_scale(X=_epoch, feature_range=(-1, 1))
                ppg_signals, ppg_info = nk.ppg_process(_epoch, sampling_rate=hrv_samp_freq)
                # nk.ppg_plot(ppg_signals, sampling_rate=hrv_samp_freq)
                ppg_peaks = remove_outliers_and_ectopic_beats(ppg_info["PPG_Peaks"], hrv_samp_freq,
                                                              rm_ectopic_beats=rm_ectopic_beats)

                _feat = None
                _feat = nk.hrv(ppg_peaks, sampling_rate=hrv_samp_freq, show=False)
                _time = int(_time)
                _feat.index = [f"{_time}_{_time + win_size}"]
                all_feat = pd.concat([all_feat, _feat])
            all_feat.to_csv(f'{RESULTS_PATH}/hrv/{target_dir}/{user_info}_{sound_id}_{sound_name}.csv')

def store_whole_hrv_feat():
    '''
    存储stimulus级别的hrv特征
    Returns
    -------

    '''
    from yasa.others import sliding_window

    target_dir = 'tables/time_domain_feats'
    os.makedirs(f'{RESULTS_PATH}/hrv/{target_dir}/', exist_ok=True)
    rm_ectopic_beats = False
    win_size = 30  # 单位为s
    step_size = 5
    for user_id in user_id_list:
    # for user_id in ['p10']:
        print(f"**********当前用户：{user_id}***********")
        ppg_file_path = f'{PPG_PATH}/minmax/{user_id}.ppg'
        baseline, data = read_ppg_and_peak(ppg_file_path)
        user_info = f"{user_id}_{user_id_to_name[user_id]}"

        times, epochs = sliding_window(np.array(data['data']), sf=hrv_samp_freq, window=win_size, step=step_size)
        all_feat = pd.DataFrame()
        first_epoch_feat = None
        for _time, _epoch in zip(times, epochs):
            _epoch = minmax_scale(X=_epoch, feature_range=(-1, 1))
            ppg_signals, ppg_info = nk.ppg_process(_epoch, sampling_rate=hrv_samp_freq)
            # nk.ppg_plot(ppg_signals, sampling_rate=hrv_samp_freq)
            ppg_peaks = remove_outliers_and_ectopic_beats(ppg_info["PPG_Peaks"], hrv_samp_freq,
                                                          rm_ectopic_beats=rm_ectopic_beats)

            _feat = None
            try:
                _feat = nk.hrv(ppg_peaks, sampling_rate=hrv_samp_freq, show=False)
            except:
                _feat = first_epoch_feat
                with open('log.txt', 'a') as f:
                    f.write(f'{user_id}_{_time}\n')
            if type(first_epoch_feat) == type(None):
                first_epoch_feat = _feat
            _time = int(_time)
            _feat.index = [f"{_time}_{_time + win_size}"]
            all_feat = pd.concat([all_feat, _feat])
        all_feat.to_csv(f'{RESULTS_PATH}/hrv/{target_dir}/{user_info}_all_sounds.csv')


if __name__ == '__main__':
    # plot_hrv_feat_base_single_stimuli()
    # plot_hrv_feat_across_stimuli()
    store_hrv_feat()
    # store_whole_hrv_feat()
