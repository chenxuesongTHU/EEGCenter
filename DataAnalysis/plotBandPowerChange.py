#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   plotBandPowerChange  
@Time        :   2021/12/17 11:01 上午
@Author      :   Xuesong Chen
@Description :   
"""
import sys

import pandas as pd
from scipy.stats import stats
from sklearn.preprocessing import minmax_scale
from yasa.spectral import bandpower
from yasa.others import sliding_window
from yasa.spectral import bandpower_from_psd_ndarray
import os.path
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

from Feature import TimeFrequency
from Feature.utils import remove_outliers
from Reader import EDFReader, FIFReader

# matplotlib.use('MacOSX')
matplotlib.use('TkAgg')
import numpy as np
from src.sleep.constants import *
from src.constants import *
import mne
from mne.viz.topomap import _plot_topomap_multi_cbar
from collections import defaultdict
from src.sleep.utils import get_user_ratings

def get_baseline(user_id):
    df = pd.read_csv(
        f'{RESULTS_PATH}/baseline/{user_id}.csv',
        index_col=0
    )
    return df


def plot_topomap_from_df(df, info, user_id, event, win_size):

    # colorbar_range由全过程的raw图像的变化范围决定，
    # 为了保证不同band间由可比性，每个值的正负范围需相等。
    colorbar_range = {
        'Delta': 10,
        'Theta': 4,
        'Alpha': 2,
        'Sigma': 2,
        'Beta': 2,
        'Gamma': 6
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


def plot_dynamic_topomap(win_size):
    # todo: 参数传递
    for time, feat_df in zip(tf.times, region_feats):
        feat_df.index.name = time-win_size/2
        plot_topomap_from_df(feat_df, info, user_id, stimulus, win_size)


def plot_span(anno, ax, user_id):
    idx = 0
    for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
        task_start_pos = onset              # 单位为s
        task_end_pos = onset + duration     # 单位为s
        relax_start_pos = task_end_pos
        relax_end_pos = relax_start_pos + 60 * 3
        ax.axvspan(task_start_pos, task_end_pos, facecolor='#458CC4', alpha=0.2)
        ax.axvspan(relax_start_pos, relax_end_pos, facecolor='#A6A6A6', alpha=0.2)
        res = get_user_ratings(user_id)
        _l = res[idx+1]
        sound_name = tag_to_desc[_l['标号']]
        s = f"\t{sound_name} \n 困倦:{_l['困倦']} 熟悉:{_l['熟悉']} 喜爱:{_l['喜爱']}"
        x = task_start_pos
        y = ax.viewLim.ymax- 0.2 * (ax.viewLim.ymax- ax.viewLim.ymin)
        ax.text(x, y, s)
        idx += 1


def plot_diff_band_power_change():
    '''
    整个实验过程中，不同波段的能量值随时间的变化情况
    '''

    for user_id in user_id_list:
    # for user_id in ['p17']:
        print(f"**********当前user id{user_id}**************")
        # reader = EDFReader(
        #     f'{EDF_PATH}/{user_id}.edf',
        #     f'{LOG_PATH}/{user_id}.csv',
        #     offset=60 * 5,  # 5 mins
        # )
        reader = FIFReader(
            f'{FIF_PATH}/{user_id}.fif',
        )

        win_size = 4

        tf = TimeFrequency(reader.raw,  win_sec=win_size, relative=False)   # todo
        # tf = TimeFrequency(event_raw,  win_sec=5, relative=False, mode='psd')   # todo
        # tf = TimeFrequency(reader.raw, 5, relative=False)
        feats = tf.get_band_power()
        baseline = get_baseline(user_id)

        region_feats = []                     # [times, #channles, #feats]
        _res = None
        for feat in feats:
            _res = (feat - baseline) / baseline
            _res.drop(index=['VEO'], columns=['FreqRes', 'Relative'], inplace=True)

            # 仅使用枕区
            _res = _res.loc[occipital_region]

            # 选取枕区所有channel的平均值作为枕区特征
            n_index = _res.shape[0]
            for column in list(_res.columns):
                _res.loc[n_index, column] = _res[column].mean()
            _res.rename({n_index: 'mean'}, axis='index', inplace=True)
            region_feats.append(
                np.array(_res.loc['mean'].values)
            )

        channel_name = list(_res.index)
        feature_name = list(_res.columns)

        region_feats = np.array(region_feats)          # [times, feats]
        region_feats = remove_outliers(region_feats, axis=0, max_deviations=2)
        # 为了方便跨被试的比较，将所有特征在时间轴做了minmax_scale
        # org_shape = region_feats.shape
        # n_times = region_feats.shape[0]
        # region_feats = region_feats.reshape((n_times, -1))
        # region_feats = minmax_scale(X=region_feats, feature_range=(-1, 1))

        data = pd.DataFrame(
            columns=feature_name,
            data=region_feats,
            index=tf.times,
        )

        rolling_length = 15
        data = data.rolling(rolling_length).mean()

        # padding操作：将滑动平均未涉及的值设置为第一个mean值。
        rolling_start_idx = rolling_length-1
        for idx in range(rolling_start_idx):
            data.iloc[idx, :] = data.iloc[rolling_start_idx, :]

        # z score
        # from scipy import stats
        # _data = stats.zscore(data, axis=0)
        # data = pd.DataFrame(_data, index=data.index, columns=data.columns)

        # interest_band_list = [
        #     bands_name,
        #     ["Delta", "Theta", "Gamma"],
        #     ["Alpha", 'Sigma', 'Beta'],
        # ]
        interest_band_list = [
            bands_name,
            ["Delta", "Theta", "Gamma"],
            ["Alpha", 'Sigma', 'Beta'],
        ]
        for band in bands_name:
            interest_band_list.append([band])
        # interest_band = ["Alpha", 'Sigma', 'Beta']
        for interest_band in interest_band_list:
            fig, axes = plt.subplots(figsize=(25, 8))
            sns.lineplot(data=data[interest_band])
            # axes.set_xticks(tf.times)
            plot_span(reader.raw.annotations, axes, user_id)
            root_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/all/'
            os.makedirs(root_path, exist_ok=True)
            file_name = '_'.join(interest_band)
            plt.savefig(f"{root_path}/{file_name}.pdf", format='pdf')


def plot_brain_power_change():
    '''
    整个实验过程中，全脑的能量变化
    Returns
    -------
    '''
    for user_id in user_id_list:
        reader = FIFReader(
            f'{FIF_PATH}/{user_id}.fif',
        )

        tf = TimeFrequency(reader.raw, 4)
        feats = tf.get_band_power()
        extra_info = 'mean_of_80%'
        for region in list(brain_region_info.keys())[:1]:

            res = []
            for feat in feats:
                feat = feat.loc[brain_region_info[region]]
                cut_ratio = 0.1
                start_index = int(len(feat) * cut_ratio)
                _pow_list = sorted(list(feat['TotalAbsPow']))[start_index: -start_index]
                res.append(
                    # feat['All'].mean()
                    np.mean(_pow_list)
                )

            # res = stats.zscore(res, axis=0)

            data = pd.DataFrame(
                columns=[region],
                data=res,
                index=tf.times,
            )

            rolling_length = 15
            data = data.rolling(rolling_length).mean()

            # padding操作：将滑动平均未涉及的值设置为第一个mean值。
            rolling_start_idx = rolling_length-1
            for idx in range(rolling_start_idx):
                data.iloc[idx, :] = data.iloc[rolling_start_idx, :]

            interest_band = region
            fig, axes = plt.subplots(figsize=(25, 8))
            sns.lineplot(data=data[interest_band])
            # axes.set_xticks(tf.times)
            plot_span(reader.raw.annotations, axes, user_id)
            root_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/all/'
            os.makedirs(root_path, exist_ok=True)
            file_name = interest_band
            plt.savefig(f"{root_path}/{extra_info}_{file_name}.pdf", format='pdf')

            print()
    pass

if __name__ == '__main__':
    # plot_diff_band_power_change()
    plot_brain_power_change()
