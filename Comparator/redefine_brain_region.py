#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   redefine_brain_region  
@Time        :   2022/3/4 3:54 下午
@Author      :   Xuesong Chen
@Description :   RQ1: 听不同声音时，根据现有的脑区划分标准，同脑区内的点位是否信号一致性保持在较高水平？
"""
from multiprocessing import Pool

import matplotlib.pyplot as plt
from pandas import MultiIndex

from DataAnalysis.Visualization.utils import plot_topomap
from Reader import FIFReader
from Scripts.concat_img import image_concat
from Scripts.system_cmd import del_file
from src import *
from src.sleep.utils import get_user_ratings, get_user_ratings_str
from src.utils import calc_phrase_bias_from_df


def sub_process(raw_df):
    tmp_cor, tmp_bias = calc_phrase_bias_from_df(raw_df, n_bias_samples=int(bp_samp_freq * 0.5), step=1)
    return tmp_cor, tmp_bias  # df

def calc_time_bias_among_brain_region():

    batch_size = 3
    tag_to_desc.update({'baseline': 'baseline'})

    # tag_to_desc = {'baseline': 'baseline'}

    # user_id_list.romove('p01')

    channel_names.remove('VEO')
    my_index = MultiIndex.from_product([user_id_list, list(tag_to_desc.keys()), channel_names],
                                       names=['user', 'stimulus', 'channel'])
    res_cor = pd.DataFrame(
        index=my_index,
        columns=channel_names,
    )
    res_bias = pd.DataFrame(
        index=my_index,
        columns=channel_names,
    )

    for user_id_idx in range(0, len(user_id_list), batch_size):
        tmp_user_id_list = user_id_list[user_id_idx: user_id_idx + batch_size]
        tmp_dic = defaultdict(lambda: defaultdict(lambda: None))
        pool = Pool(len(tag_to_desc) * len(tmp_user_id_list))
        for user_id in tmp_user_id_list:
            reader = FIFReader(
                f'{FIF_PATH}/{user_id}.fif',
            )
            for stimulus_id in list(tag_to_desc.keys()):
                event_raw = reader.get_event_raw(stimulus_id)
                raw_df = event_raw.to_data_frame()
                raw_df.drop('time', axis=1, inplace=True)
                raw_df.drop('VEO', axis=1, inplace=True)
                raw_df = raw_df[channel_names]
                tmp_dic[user_id][stimulus_id] = pool.apply_async(sub_process, args=(raw_df,))
        pool.close()
        pool.join()
        for user_id in tmp_user_id_list:
            for stimuli_id in tag_to_desc.keys():
                res = tmp_dic[user_id][stimuli_id].get()
                _cor_df = res[0]
                _bias_df = res[1]
                res_cor.loc[user_id, stimuli_id] = _cor_df.values
                res_bias.loc[user_id, stimuli_id] = _bias_df.values

        res_cor.to_csv("csv/intra_user_correlation.csv")
        res_bias.to_csv("csv/intra_user_time_bias.csv")


def plot_time_bias():
    # stimulus_id = 'baseline'
    # stimulus_id = 'B1'
    # for stimulus_id in ['baseline', 'A1', 'B1']:
    user_id = "p10"
    n_top = 15
    reader = FIFReader(
        # f'{FIF_PATH}/{user_id}.fif',
        "../data/EEGAndMusic/p10.fif"
    )
    tmp_file_path = './tmp/'

    for stimulus_id in ['baseline', 'A1', 'B1', 'A2']:
        corr_df = pd.read_csv(f"p10_correlation_{stimulus_id}.csv", index_col=[0])
        time_bias_df = pd.read_csv(f"p10_time_bias_{stimulus_id}.csv", index_col=[0])

        ratings_str = get_user_ratings_str(user_id=user_id, stimulus_id=stimulus_id)

        for chan in list(corr_df.columns):
            most_related_chans = corr_df[chan].abs().sort_values(ascending=False).index[:n_top]
            corr_df[chan][set(corr_df[chan].index)-set(most_related_chans)] = 0
            time_bias_df[chan][set(time_bias_df[chan].index)-set(most_related_chans)] = 0
            cor_fig = plot_topomap(pd.DataFrame(corr_df[chan]), reader.raw.info, chan, vmin=-1, vmax=1, show=False,
                                   title=f'Correlation of {chan} {ratings_str}')
            bias_fig = plot_topomap(pd.DataFrame(time_bias_df[chan]), reader.raw.info, chan, vmin=-0.5, vmax=0.5,
                                    show=False, title=f'Time bias of {chan}')

            cor_fig.savefig(f'{tmp_file_path}/tmp_cor_fig.png', dpi=300)
            bias_fig.savefig(f'{tmp_file_path}/tmp_bias_fig.png', dpi=300)
            image_concat(f'{tmp_file_path}', f'./res/top{n_top}/', f'{chan}_{stimulus_id}.png')
            del_file(tmp_file_path)
            plt.clf()
            plt.close(cor_fig)
            plt.close(bias_fig)


calc_time_bias_among_brain_region()
# plot_time_bias()
