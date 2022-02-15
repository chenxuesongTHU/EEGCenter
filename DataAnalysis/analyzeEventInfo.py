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
import pickle

from scipy.stats import stats
from sklearn.preprocessing import minmax_scale

from DataAnalysis.Visualization.utils import plot_topomap
from Scripts.tmp.generate_special_time_info import get_special_time_spans
from src.utils import is_equal_variance

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
from Reader import FIFReader

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
    # figs, axes = plt.subplots(1, n_axes, figsize=(2 * n_axes, 1.5)) # 横向
    figs, axes = plt.subplots(n_axes, 1, figsize=(3, 2 * n_axes))  # 纵向
    colorbar_info = defaultdict(lambda: [])
    for ax, (key, freq_range) in zip(axes, bands_freqs.items()):

        vmin = None
        vmax = None

        if cmp_in_diff_stimulus:
            vmin = colorbar_range[key]['low']
            vmax = colorbar_range[key]['high']

        mne.viz.plot_topomap(df[key], info, axes=ax,
                             vmin=vmin, vmax=vmax,
                             show=False)
        # _plot_topomap_multi_cbar(df[key], info, ax=ax, title=None, colorbar=True)
        ax.set_title(f'{key}({freq_range[0]}-{freq_range[1]} Hz)')

    res = get_user_ratings(user_id, stimulus_id=params['stimulus'])
    sound_name = tag_to_desc[params['stimulus']]
    user_name = user_id_to_name[params['user_id']]
    title = f"\t {user_name}\t{sound_name} \n 困倦:{res['困倦']} 熟悉:{res['熟悉']} 喜爱:{res['喜爱']}"

    figs.suptitle(title, y=0.08)
    # width, height = figs.get_size_inches()

    # row oriented
    # figs.set_size_inches(width+0.8, height)

    # column oriented
    # figs.set_size_inches(width, height+1)
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
    target_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/stimulus_level/topomap/'
    os.makedirs(target_path, exist_ok=True)
    figs.savefig(f'{target_path}/{event}_{tag_to_desc[event]}_{tmin}_{tmax}.png')
    plt.close()


def plot_dynamic_topomap(reader, baseline, user_id):
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
            # _res.drop(index=['VEO', 'Status'], inplace=True) # if edf
            _res.drop(index=['VEO'], inplace=True)
            # _res = _res.loc[occipital_region]
            norm_feats.append(
                _res.values
            )
        channel_name = list(feats[0].index)
        features = list(feats[0].columns)
        channel_name.remove('VEO')
        # channel_name.remove('Status')
        feats_arr = np.array(norm_feats)
        feats_arr = remove_outliers(feats_arr, axis=0, max_deviations=2)
        # 为了方便跨被试的比较，将所有特征在时间轴做了minmax_scale
        org_shape = feats_arr.shape
        n_times = feats_arr.shape[0]
        feats_arr = feats_arr.reshape((n_times, -1))
        feats_arr = minmax_scale(X=feats_arr, feature_range=(-1, 1))
        _data = feats_arr.reshape(org_shape)
        # print("max:", np.max(_data), "min:", np.min(_data))
        norm_feats = []
        for single_win in _data:
            _df = pd.DataFrame(single_win, index=channel_name, columns=features)
            norm_feats.append(_df)

        dump_dic = {}
        for time, feat_df in zip(tf.times, norm_feats):
            start_time = int(time - win_size / 2)
            feat_df.index.name = start_time
            # plot_topomap_from_df(feat_df, info, user_id, stimulus, win_size)
            dump_dic[start_time] = feat_df    # start time -> feat df
            # 用于保存结果
        pickle.dump(dump_dic, open(f'{RESULTS_PATH}/dumps/topomap/{user_id}_{stimulus}_{tag_to_desc[stimulus]}.pkl', 'wb'))


def output_avg_band_power_per_channel(user_id, reader, baseline, cmp_in_diff_stimulus=False):
    target_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/stimulus_level/norm_among_stimulus'
    total_axes_lims_info_df = pd.DataFrame()

    for stimulus in desc_to_tag.values():
        event_raw = reader.get_event_raw(stimulus)
        info = event_raw.info
        # tf = TimeFrequency(reader.raw,  win_sec=5, relative=False, mode='psd')   # todo
        tf = TimeFrequency(event_raw, win_sec=5, relative=False)  # todo
        # tf = TimeFrequency(reader.raw, 5, relative=False)
        feats = tf.get_band_power()

        # dim_info, feats = tf.get_band_power_array()
        _res = None

        norm_feats = []
        for feat in feats:
            _res = (feat - baseline) / baseline
            _res.drop(index=['VEO'], columns=['FreqRes', 'Relative'], inplace=True)
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
            file_name = 'org_' + file_name

        # row oriented
        # figs.savefig(f'{target_path}/{file_name}.png')

        # column oriented
        store_path = f'{target_path}/column_oriented/'
        os.makedirs(store_path, exist_ok=True)
        figs.savefig(f'{store_path}/{file_name}.png')

    if not cmp_in_diff_stimulus:
        total_axes_lims_info_df.to_csv(f'{target_path}/axesLimitsInDiffBands.csv')


def output_avg_band_power(reader, baseline):
    # 不区分位置导出用户听同一声音时不同波段的枕区能量
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
            _res.drop(index=['VEO'], inplace=True)
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


def time_overlying_main():
    # 弃用，没有做baseline和min max，实现见time_overlying_main_v2()
    special_times = get_special_time_spans()
    win_size = 5
    user_y_lims = defaultdict(lambda: None)
    user_y_lims = {
        'p17': 29.73743738907362, 'p16': 26.48677555031468, 'p13': 73.71093759112559, 'p02': 342.5012314346288,
        'p09': 431.59542349504204, 'p11': 216.35120453721947, 'p04': 13.237494593784943, 'p07': 65.57241921634511}

    for user_id, user_info in special_times.items():
        user_level_y_lim_list = []
        for sound_id, sound_info in user_info.items():
            reader = FIFReader(
                f'{FIF_PATH}/{user_id}.fif',
            )
            event_raw = reader.get_event_raw(sound_id)

            diff_time_feat = []
            res_feats = None
            for _band, _times in sound_info.items():
                for start_time in _times:
                    end_time = start_time + win_size
                    _tmp_raw = event_raw.copy().crop(tmin=start_time, tmax=end_time, include_tmax=True)
                    tf = TimeFrequency(_tmp_raw, win_sec=win_size, relative=False)  # todo
                    # tf = TimeFrequency(reader.raw, 5, relative=False)
                    feats = tf.get_band_power()[0]
                    if type(res_feats) == type(None):
                        res_feats = feats
                    else:
                        res_feats += feats
                res_feats.drop(index=['VEO'], columns=['FreqRes', 'Relative', 'TotalAbsPow'], inplace=True)
                res_feats /= len(_times)
                col_name = _band.split('_')[0]
                feats_arr = minmax_scale(X=res_feats, feature_range=(-1, 1))
                res_feats = pd.DataFrame(feats_arr, columns=res_feats.columns, index=res_feats.index)
                col_name = col_name.capitalize()
                title = f"{user_id}_{user_id_to_name[user_id]} {tag_to_desc[sound_id]} {_band}"
                figs = plot_topomap(res_feats, event_raw.info, col_name,
                                    show=False, title=title,
                                    vmax=1, vmin=-1,
                                    )
                low, high = figs.axes[0].CB.lims
                user_level_y_lim_list.append(high)
                figs.savefig(f"{RESULTS_PATH}/time_overlying/img_scale/{title}.png", format='png')
        user_y_lims[user_id] = max(user_level_y_lim_list)
    print(dict(user_y_lims))

def time_overlying_main_v2():

    action = "cmp_peak_valley"      # {plot | cmp_peak_valley}
    special_times = get_special_time_spans()

    reader = FIFReader(
        f'{FIF_PATH}/p10.fif',
    )
    info = reader.raw.info
    peak_and_valley = defaultdict(lambda: defaultdict(lambda: []))  # channel -> {peak | valley} -> list
    for user_id, user_info in special_times.items():
        for sound_id, sound_info in user_info.items():

            with open(f'{RESULTS_PATH}/dumps/topomap/{user_id}_{sound_id}_{tag_to_desc[sound_id]}.pkl', 'rb') as _file:
                feats_src = pickle.load(_file)
            res_feats = None
            for _band, _times in sound_info.items():
                if sound_id == 'A2':
                    print("debug")
                # _times = [100]
                for start_time in _times:
                    feats = feats_src[start_time]
                    if type(res_feats) == type(None):
                        res_feats = feats
                    else:
                        res_feats += feats
                # res_feats.drop(index=['VEO'], columns=['FreqRes', 'Relative', 'TotalAbsPow'], inplace=True)
                res_feats /= len(_times)
                col_name = _band.split('_')[0]
                col_name = col_name.capitalize()
                if action == "plot":
                    title = f"{user_id}_{user_id_to_name[user_id]} {tag_to_desc[sound_id]} {_band}"
                    figs = plot_topomap(res_feats, info, col_name,
                                        show=False, title=title,
                                        vmax=1, vmin=-1,
                                        )
                    figs.savefig(f"{RESULTS_PATH}/time_overlying/img_scale/{title}.png", format='png')
                    # figs.savefig(f"{RESULTS_PATH}/time_overlying/img_scale/tmp.png", format='png')
                if action == "cmp_peak_valley":
                    for _chan in res_feats.index:
                        peak_and_valley[_chan][_band].append(res_feats.loc[_chan, col_name])

    for _chan, _pairs in peak_and_valley.items():
        peak = 'alpha_peak'
        valley = 'alpha_valley'
        _peak_list = _pairs[peak]
        _valley_list = _pairs[valley]
        equal_var = is_equal_variance(_peak_list, _valley_list)
        print(_chan ,stats.ttest_ind(_peak_list, _valley_list, equal_var=equal_var))

def time_overlying_main_all_users():

    action = "plot"      # {plot | cmp_peak_valley}

    reader = FIFReader(
        f'{FIF_PATH}/p10.fif',
    )
    info = reader.raw.info

    for stage in ['困倦', '入睡', '放松', '清醒']:
        special_times = get_special_time_spans(stage=stage)
        for target_band in ['alpha_peak', 'alpha_valley', 'theta_peak']:

            peak_and_valley = defaultdict(lambda: defaultdict(lambda: []))  # channel -> {peak | valley} -> list
            res_feats = None
            count = 0
            for user_id, user_info in special_times.items():
                for sound_id, sound_info in user_info.items():

                    with open(f'{RESULTS_PATH}/dumps/topomap/{user_id}_{sound_id}_{tag_to_desc[sound_id]}.pkl', 'rb') as _file:
                        feats_src = pickle.load(_file)
                    for _band, _times in sound_info.items():
                        if sound_id == 'A2':
                            print("debug")
                        # _times = [100]
                        if _band != target_band:
                            continue
                        for start_time in _times:
                            feats = feats_src[start_time]
                            if type(res_feats) == type(None):
                                res_feats = feats
                            else:
                                res_feats += feats
                            count += 1
                        # res_feats.drop(index=['VEO'], columns=['FreqRes', 'Relative', 'TotalAbsPow'], inplace=True)
                if type(res_feats) == type(None):
                    continue
                res_feats /= count
                col_name = target_band.split('_')[0]
                col_name = col_name.capitalize()
                if action == "plot":
                    title = f"{stage} {target_band}"
                    figs = plot_topomap(res_feats, info, col_name,
                                        show=False, title=title,
                                        vmax=1, vmin=-1,
                                        )
                    figs.savefig(f"{RESULTS_PATH}/time_overlying/all_users/{title}.png", format='png')


def main():
    for user_id in user_id_list:
    # for user_id in ['p17']:
        # user_id = 'p03'
        # get_colorbar_limits(user_id)
        print(f"**********当前user id{user_id}**************")
        # reader = EDFReader(
        #     f'{EDF_PATH}/{user_id}.edf',
        #     f'{LOG_PATH}/{user_id}.csv',
        #     offset=60 * 5,  # 5 mins
        # )
        reader = FIFReader(
            f'{FIF_PATH}/{user_id}.fif',
        )

        baseline = get_baseline(user_id)
        plot_dynamic_topomap(reader, baseline, user_id)

        # output_avg_band_power(reader, baseline)

        # for cmp_in_diff_stimulus in [False, True]:
        #     output_avg_band_power_per_channel(user_id, reader, baseline, cmp_in_diff_stimulus)


if __name__ == '__main__':
    # time_overlying_main()
    # time_overlying_main_v2()
    time_overlying_main_all_users()
    # main()
