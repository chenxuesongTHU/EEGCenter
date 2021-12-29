#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   analyzeEventInfo  
@Time        :   2021/12/23 11:38 上午
@Author      :   Xuesong Chen
@Description :   
"""
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
from sklearn.preprocessing import minmax_scale

"""
@File        :   plotBandPowerChange  
@Time        :   2021/12/17 11:01 上午
@Author      :   Xuesong Chen
@Description :   
"""

import pandas as pd
import os.path
import matplotlib.pyplot as plt
import matplotlib

from Feature import TimeFrequency
from Feature.utils import remove_outliers
from Reader import EDFReader

# matplotlib.use('MacOSX')
matplotlib.use('TkAgg')
import numpy as np
from src.sleep.constants import *
from src.constants import *
import mne
from collections import defaultdict
from src.sleep.utils import get_user_ratings


def get_baseline(user_id):
    df = pd.read_csv(
        f'{RESULTS_PATH}/baseline/{user_id}.csv',
        index_col=0
    )
    return df

def get_colorbar_limits(user_id):
    target_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/stimulus_level/norm_among_stimulus'
    df = pd.read_csv(
        f'{target_path}/axesLimitsInDiffBands.csv',
        index_col=0,
    )
    low_cols, high_cols = [], []
    for _feat in list(df.columns):
        if _feat.startswith('low'):
            low_cols.append(_feat)
        if _feat.startswith('high'):
            high_cols.append(_feat)
    df['low'] = df[low_cols].min(axis=1)
    df['high'] = df[high_cols].max(axis=1)
    return df[['low', 'high']].T.to_dict()


def plot_static_topomap_from_df(df, info, params, show=True, cmp_in_diff_stimulus=False):

    if cmp_in_diff_stimulus:
        colorbar_range = get_colorbar_limits(params['user_id'])

    n_axes = len(bands_name)
    figs, axes = plt.subplots(1, n_axes, figsize=(2 * n_axes, 1.5))
    colorbar_info = defaultdict(lambda: [])
    for ax, (key, freq_range) in zip(axes, bands_freqs.items()):

        vmin = None
        vmax = None

        if cmp_in_diff_stimulus:
            vmin=colorbar_range[key]['low']
            vmax=colorbar_range[key]['high']

        mne.viz.plot_topomap(df[key], info, axes=ax,
                             vmin=vmin, vmax=vmax,
                             show=False)
        # _plot_topomap_multi_cbar(df[key], info, ax=ax, title=None, colorbar=True)
        ax.set_title(f'{key}({freq_range[0]}-{freq_range[1]} Hz)')

    res = get_user_ratings(user_id, stimulus_id=params['stimulus'])
    sound_name = tag_to_desc[params['stimulus']]
    user_name = user_id_to_name[params['user_id']]
    title = f"\t {user_name}\t{sound_name} 困倦:{res['困倦']} 熟悉:{res['熟悉']} 喜爱:{res['喜爱']}"

    figs.suptitle(title)
    width, height = figs.get_size_inches()
    figs.set_size_inches(width, height + 0.8)
    if show:
        figs.show()
    else:
        return figs


def plot_topomap_from_df(df, info, user_id, event, win_size):
    # colorbar_range由全过程的raw图像的变化范围决定，
    # 为了保证不同band间由可比性，每个值的正负范围需相等。
    colorbar_range = {
        'Delta': 1,
        'Theta': 1,
        'Alpha': 1,
        'Sigma': 1,
        'Beta': 1,
        'Gamma': 1
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


def plot_dynamic_topomap(reader, baseline):
    win_size = 5

    for stimulus in desc_to_tag.values():
        event_raw = reader.get_event_raw(stimulus)

        info = event_raw.info
        # tf = TimeFrequency(reader.raw,  win_sec=5, relative=False, mode='psd')   # todo
        tf = TimeFrequency(event_raw, win_sec=5, relative=False)  # todo
        # tf = TimeFrequency(reader.raw, 5, relative=False)
        feats = tf.get_band_power()
        norm_feats = []
        for feat in feats:
            _res = (feat - baseline) / baseline
            _res.drop(index=['VEO', 'Status'], inplace=True)
            # _res = _res.loc[occipital_region]
            norm_feats.append(
                _res.values
            )
        channel_name = list(feats[0].index)
        features = list(feats[0].columns)
        channel_name.remove('VEO')
        channel_name.remove('Status')
        feats_arr = np.array(norm_feats)
        feats_arr = remove_outliers(feats_arr, axis=0, max_deviations=2)
        # 为了方便跨被试的比较，将所有特征在时间轴做了minmax_scale
        org_shape = feats_arr.shape
        n_times = feats_arr.shape[0]
        feats_arr = feats_arr.reshape((n_times, -1))
        feats_arr = minmax_scale(X=feats_arr, feature_range=(-1, 1))
        _data = feats_arr.reshape(org_shape)
        print("max:", np.max(_data), "min:", np.min(_data))
        norm_feats = []
        for single_win in _data:
            _df = pd.DataFrame(single_win, index=channel_name, columns=features)
            norm_feats.append(_df)

        for time, feat_df in zip(tf.times, norm_feats):
            feat_df.index.name = time - win_size / 2
            plot_topomap_from_df(feat_df, info, user_id, stimulus, win_size)


def output_avg_band_power_per_channel(reader, baseline, cmp_in_diff_stimulus=False):
    target_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/stimulus_level/norm_among_stimulus'
    total_axes_lims_info_df = pd.DataFrame()

    for stimulus in desc_to_tag.values():
        event_raw = reader.get_event_raw(stimulus)
        info = event_raw.info
        # tf = TimeFrequency(reader.raw,  win_sec=5, relative=False, mode='psd')   # todo
        tf = TimeFrequency(event_raw, win_sec=4, relative=False)  # todo
        # tf = TimeFrequency(reader.raw, 5, relative=False)
        feats = tf.get_band_power()

        # dim_info, feats = tf.get_band_power_array()
        _res = None

        norm_feats = []
        for feat in feats:
            _res = (feat - baseline) / baseline
            _res.drop(index=['VEO', 'Status'], columns=['FreqRes', 'Relative'], inplace=True)
            # _res = _res.loc[occipital_region]
            norm_feats.append(
                _res.values
            )
        channel_name = list(_res.index)
        feature_name = list(_res.columns)

        norm_feats = np.array(norm_feats)  # [#times, #channels, #bands]
        norm_feats = remove_outliers(norm_feats, axis=0, max_deviations=1)
        stimulus_feats = np.mean(norm_feats, axis=0)
        stimulus_feats_df = pd.DataFrame(
            stimulus_feats, columns=feature_name, index=channel_name
        )
        params_dic = {
            'user_id': user_id,
            'stimulus': stimulus,
        }
        figs = plot_static_topomap_from_df(
            stimulus_feats_df, info, params_dic,
            show=False, cmp_in_diff_stimulus=cmp_in_diff_stimulus
        )
        axes_lims_info = {}
        for band_idx, band in enumerate(bands_name):
            low, high = figs.axes[band_idx].CB.lims  # 获取每个band对应子图的数值范围
            axes_lims_info[band] = {f'low_{stimulus}': low, f'high_{stimulus}': high}
        axes_lims_info_df = pd.DataFrame.from_dict(axes_lims_info, 'index')
        total_axes_lims_info_df = pd.concat([total_axes_lims_info_df, axes_lims_info_df], axis=1)
        os.makedirs(target_path, exist_ok=True)
        file_name = f'{params_dic["stimulus"]}_{tag_to_desc[params_dic["stimulus"]]}'
        if not cmp_in_diff_stimulus:
            file_name = 'org_'+file_name
        figs.savefig(f'{target_path}/{file_name}.png')
    if not cmp_in_diff_stimulus:
        total_axes_lims_info_df.to_csv(f'{target_path}/axesLimitsInDiffBands.csv')


def output_avg_band_power(reader, baseline):
    total_res = []
    for stimulus in desc_to_tag.values():
        event_raw = reader.get_event_raw(stimulus)
        info = event_raw.info
        # tf = TimeFrequency(reader.raw,  win_sec=5, relative=False, mode='psd')   # todo
        tf = TimeFrequency(event_raw, win_sec=5, relative=False)  # todo
        # tf = TimeFrequency(reader.raw, 5, relative=False)
        feats = tf.get_band_power()
        channel_name = list(feats[0].index)
        features = list(feats[0].columns)

        # dim_info, feats = tf.get_band_power_array()

        norm_feats = []
        for feat in feats:
            _res = (feat - baseline) / baseline
            _res.drop(index=['VEO', 'Status'], inplace=True)
            _res = _res.loc[occipital_region]
            norm_feats.append(
                _res.values
            )

        norm_feats = np.array(norm_feats)  # [#times, #channels, #bands]
        norm_feats = norm_feats.reshape((-1, len(features)))
        res = np.mean(norm_feats, axis=0)
        # res = res.reshape((1, -1))
        total_res.append(res)
    total_res = np.vstack(total_res)
    df = pd.DataFrame(total_res, columns=bands_name, index=desc_to_tag.values())
    root_path = f'../output/music_and_eeg/tmp/'
    os.makedirs(root_path, exist_ok=True)
    df.to_csv(f'{root_path}/{user_id}_{user_id_to_name[user_id]}.csv')
    # plot_topomap_from_df(df, info, user_id, stimulus, win_size)


def plot_span(anno, ax, user_id):
    idx = 0
    for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
        task_start_pos = onset  # 单位为s
        task_end_pos = onset + duration  # 单位为s
        relax_start_pos = task_end_pos
        relax_end_pos = relax_start_pos + 60 * 3
        ax.axvspan(task_start_pos, task_end_pos, facecolor='#458CC4', alpha=0.2)
        ax.axvspan(relax_start_pos, relax_end_pos, facecolor='#A6A6A6', alpha=0.2)
        res = get_user_ratings(user_id)
        _l = res[idx + 1]
        sound_name = tag_to_desc[_l['标号']]
        s = f"\t{sound_name} \n 困:{_l['困倦']} 熟:{_l['熟悉']} 喜:{_l['喜爱']}"
        x = task_start_pos
        y = ax.viewLim.ymax - 0.2 * (ax.viewLim.ymax - ax.viewLim.ymin)
        ax.text(x, y, s)
        idx += 1


for user_id in user_id_list:
    # user_id = 'p03'
    # get_colorbar_limits(user_id)
    print(f"**********当前user id{user_id}**************")
    reader = EDFReader(
        f'{EDF_PATH}/{user_id}.edf',
        f'{LOG_PATH}/{user_id}.csv',
        offset=60 * 5,  # 5 mins
    )

    reader.raw.set_channel_types({'VEO': 'eog'})
    ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
    reader.raw.set_montage(ten_twenty_montage)
    baseline = get_baseline(user_id)
    # plot_dynamic_topomap(reader, baseline)
    # output_avg_band_power(reader, baseline)
    # for cmp_in_diff_stimulus in [False, True]:
    cmp_in_diff_stimulus = True
    output_avg_band_power_per_channel(reader, baseline, cmp_in_diff_stimulus)
