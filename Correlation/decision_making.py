#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   decision_making  
@Time        :   2022/3/16 4:50 下午
@Author      :   Xuesong Chen
@Description :   
"""
from copy import copy

import matplotlib.pyplot as plt

from DataAnalysis.Visualization.utils import plot_topomap
from Reader.EDFReader import EDFReader
from src.constants import *
from src.sleep.constants import *
from src.utils import calc_pearsonr_from_df, calc_phrase_bias_from_df, max_pearsonr_and_phrase_bias
from src import *
import matplotlib
matplotlib.use('TkAgg')


# todo 可视化看看不同数值范围的实际含义是啥样子的

for user_id in user_id_list[3:7]:
    file = f"{DATA_PATH}/datasets/decision making/edf/{user_id}.edf"
    reader = EDFReader(file)
    bp_order_channels = copy(reader.raw.ch_names)
    print()
    bp_order_channels.remove('VEO')
    bp_order_channels.remove('Status')
    selected_raw = reader.raw.copy().crop(tmin=10, tmax=40+60*3)
    signals_arr = selected_raw.get_data(picks=channel_names).squeeze()
    signals_df = pd.DataFrame(signals_arr.T, columns=channel_names)
    max_pearsonr_and_phrase_bias(
        signals_df["Oz"], signals_df["Fpz"], int(bp_samp_freq * 0.5), 1
    )
    corr_df, time_bias_df = calc_phrase_bias_from_df(signals_df, n_bias_samples=int(bp_samp_freq * 0.1), step=1)
    corr_df = corr_df[bp_order_channels]
    corr_df = corr_df.reindex(bp_order_channels)
    time_bias_df = time_bias_df[bp_order_channels]
    time_bias_df = time_bias_df.reindex(bp_order_channels)
    for chan in channel_names_contains_z:
        for n_top in [100, 15]:
            cur_corr_df = copy(corr_df)
            cur_time_bias_df = copy(time_bias_df)
            most_related_chans = cur_corr_df[chan].abs().sort_values(ascending=False).index[:n_top]
            cur_corr_df[chan][set(cur_corr_df[chan].index) - set(most_related_chans)] = 0
            mean_v = round(cur_corr_df[chan].abs().sum() / n_top, 2)
            mean_time_bias_v = round(cur_time_bias_df[chan].abs().sum() / n_top, 2)
            cor_fig = plot_topomap(pd.DataFrame(cur_corr_df[chan]), reader.raw.info, chan, vmin=-1, vmax=1, show=False,
                                           title=f'ref: {chan} cor mean:{mean_v}')
            cor_fig.savefig(
                f'{DATA_PATH}/datasets/decision making/images/correlation/top{n_top}/{user_id}_{chan}.png', dpi=300)
            time_bias_fig = plot_topomap(pd.DataFrame(cur_time_bias_df[chan]), reader.raw.info, chan, vmin=-0.2, vmax=0.2, show=False,
                                           title=f'ref: {chan} time_bias mean:{mean_time_bias_v}')
            time_bias_fig.savefig(
                f'{DATA_PATH}/datasets/decision making/images/time_bias/top{n_top}/{user_id}_{chan}.png', dpi=300)
            plt.close(cor_fig)
            plt.close(time_bias_fig)

    print()
