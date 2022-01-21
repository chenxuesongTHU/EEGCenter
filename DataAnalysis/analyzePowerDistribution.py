#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   analyzePowerDistribution  
@Time        :   2021/12/17 4:33 下午
@Author      :   Xuesong Chen
@Description :   生成baseline
"""
import pandas as pd

from Reader import EDFReader, FIFReader
from Feature.timeFrequency import TimeFrequency
import matplotlib.pyplot as plt
import numpy as np
from Feature.utils import remove_outliers
from src.constants import *
from src.sleep.constants import *
import os
import mne


def plot_topomap(df, info, show=True, title=None):
    figs, ax = plt.subplots()  # 纵向
    ch_names = info['ch_names'].copy()
    ch_names.remove('VEO')
    if 'Status' in ch_names:
        ch_names.remove('Status')
    mne.viz.plot_topomap(df['All'], info, axes=ax,
                         names=ch_names,
                         show_names=True,
                         show=False)
    # _plot_topomap_multi_cbar(df[key], info, ax=ax, title=None, colorbar=True)
    ax.set_title(title)

    if show:
        figs.show()
    else:
        return figs


def generate_baseline():
    for user_id in user_id_list:
    # for user_id in ['p17']:
    #     reader = EDFReader(
    #         f'{EDF_PATH}/{user_id}.edf',
    #         f'{LOG_PATH}/{user_id}.csv'
    #     )
        reader = FIFReader(
            f'{FIF_PATH}/{user_id}.fif',
        )
        raw = reader.raw
        raw = raw.crop(0, 5 * 60)
        tf = TimeFrequency(raw, 4, step_sec=1)
        dim_info, feats = tf.get_band_power_array()
        # 避免极值影响，仅使用65%的数据求平均
        feats = remove_outliers(feats, axis=0, max_deviations=1)
        baseline = np.mean(feats, axis=0)
        # baseline = np.median(feats, axis=0)
        baseline = pd.DataFrame(
            baseline, index=dim_info['channel'], columns=dim_info['feature']
        )
        baseline.to_csv(f'{RESULTS_PATH}/baseline/{user_id}.csv')

        print()


def plot_all_channel_info(type='power'):
    for user_id in user_id_list:
        # for user_id in ['p02']:
        # reader = EDFReader(
        #     f'{EDF_PATH}/{user_id}.edf',
        #     f'{LOG_PATH}/{user_id}.csv'
        # )
        reader = FIFReader(
            f'{FIF_PATH}/{user_id}.fif',
        )
        raw = reader.raw
        raw = raw.crop(0, 5 * 60)
        tf = TimeFrequency(raw, 4, bands=[(4, 40, 'All')])
        dim_info, feats = tf.get_band_power_array()
        # 避免极值影响，仅使用65%的数据求平均
        feats = remove_outliers(feats, axis=0, max_deviations=1)
        if type == 'power':
            power_dic = np.mean(feats, axis=0)
        if type == 'change':
            power_dic = np.std(feats, axis=0)
        # baseline = np.median(feats, axis=0)
        power_dic = pd.DataFrame(
            power_dic, index=dim_info['channel'], columns=dim_info['feature']
        )
        # power_dic.drop(index=['VEO', 'Status'], inplace=True)
        power_dic.drop(index=['VEO'], inplace=True)

        figs = plot_topomap(power_dic, raw.info, show=False, title=f"{type} distribution")
        # target_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/power_distribution/'
        target_path = f'{RESULTS_PATH}/power/'
        os.makedirs(target_path, exist_ok=True)
        figs.savefig(f'{target_path}/{user_id}_{user_id_to_name[user_id]}_{type}.pdf', format='pdf')
        # figs.close()

if __name__ == '__main__':

    # generate_baseline()
    for type in ['power', 'change']:
        plot_all_channel_info(type)
