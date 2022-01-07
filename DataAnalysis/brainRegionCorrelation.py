#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   brainRegionCorrelation  
@Time        :   2021/12/23 12:25 上午
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr

from Feature import TimeFrequency
from Feature.utils import remove_outliers
from Reader import EDFReader

# matplotlib.use('MacOSX')
matplotlib.use('TkAgg')
import numpy as np
from src.sleep.constants import *
from src.constants import *

user_id = 'p10'
# stimulus = 'B1'
def signal_move_on_time_axis():
    for user_id in user_id_list:
        reader = EDFReader(
            f'{EDF_PATH}/{user_id}.edf',
            f'{LOG_PATH}/{user_id}.csv',
            offset=60 * 5,  # 5 mins
        )

        raw = reader.raw

        plot_target = ['rest'] + list(desc_to_tag.values())
        tag_to_desc['rest'] = 'rest'
        n_axes = len(plot_target)

        figs, axes = plt.subplots(n_axes, 1)

        for ax, stimulus in zip(axes, plot_target):
            if stimulus == 'rest':
                tmp_raw = raw.copy().crop(tmin=0, tmax=60*5)
            else:
                tmp_raw = reader.get_event_raw(stimulus)
            oz_signal = tmp_raw.get_data(picks=['Oz']).squeeze()
            Fpz_signal = tmp_raw.get_data(picks=['Fpz']).squeeze()
            sfreq = tmp_raw.info['sfreq']
            obs_samps = int(3 * 60 * sfreq) # 样本比较时长 3 min
            time_bias = int(2 * sfreq)      # 前后 1 s
            x = []
            y = []
            for i in range(-time_bias, time_bias):
                _ = np.corrcoef([oz_signal[time_bias:time_bias+obs_samps], Fpz_signal[time_bias+i:time_bias+i+obs_samps]])[0][1]
                x.append(i)
                y.append(_)

            ax.plot(x, y, label=tag_to_desc[stimulus])
            ax.set_ylim(-0.8, 0.8)
            ax.legend(loc='upper right')

        # figs.legend()
        # plt.show()
        plt.savefig(f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/Oz_Fpz_correlation.pdf', format='pdf')

        # eeg_signals = raw.get_data().squeeze()
        # df = pd.DataFrame(np.corrcoef(eeg_signals), index=raw.info.ch_names, columns=raw.info.ch_names)
        # df.to_csv('rest_all_channel_relation.csv')
        # print()

def cmp_brain_signals_with_specific_channel(channel_name):

    for user_id in user_id_list:
        reader = EDFReader(
            f'{EDF_PATH}/{user_id}.edf',
            f'{LOG_PATH}/{user_id}.csv',
            offset=60 * 5,  # 5 mins
        )

        raw = reader.raw
        raw = raw.drop_channels(['VEO', 'Status'])

        plot_target = ['rest'] + list(desc_to_tag.values())
        tag_to_desc['rest'] = 'rest'
        n_axes = len(plot_target)

        # figs, axes = plt.subplots(1, n_axes)
        res = pd.DataFrame()
        rest_mean_name = None
        for stimulus in plot_target:
            if stimulus == 'rest':
                tmp_raw = raw.copy().crop(tmin=0, tmax=60*5, include_tmax=False)
            else:
                tmp_raw = reader.get_event_raw(stimulus)
            oz_signal = tmp_raw.get_data(picks=[channel_name]).squeeze()
            other_channels = tmp_raw.info['ch_names'].copy()
            other_channels.remove(channel_name)
            other_signals = tmp_raw.get_data(picks=other_channels).squeeze()

            all_channels = [channel_name] + other_channels
            all_signals = np.vstack((oz_signal.reshape(1, -1), other_signals))
            df = pd.DataFrame(np.corrcoef(all_signals), index=all_channels, columns=all_channels)
            df = df.loc[:, [channel_name]]
            df = df.abs()
            tick = tag_to_desc[stimulus]
            tick += '-%.2f' % df[channel_name].mean()
            if stimulus == 'rest':
                rest_mean_name = tick
            if stimulus != 'rest':
                p, sig = pearsonr(res[rest_mean_name], df[channel_name])
                tick += '(%.2f)'%(p)
            df.columns = [tick]
            res = pd.concat([res, df], axis=1)

        # res.sort_values(by=[rest_mean_name], inplace=True)
        res.sort_index(0, inplace=True)
        plt.figure(figsize=(5, 16))
        ax = sns.heatmap(res, vmin=0, vmax=1, annot=True, cmap='rocket_r', annot_kws={'fontsize': 8}, fmt='.2f')
        n_y_ticks, n_x_ticks = res.shape
        ax.set_ylim([-0.5, n_y_ticks + 0.5])
        plt.savefig(
            # f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/interval_{channel_name}_and_others_correlation.pdf',
            f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/interval_{channel_name}_and_others_correlation_sort_by_channel_name.pdf',
            format='pdf')
        plt.close()


# signal_move_on_time_axis()
cmp_brain_signals_with_specific_channel('Oz')