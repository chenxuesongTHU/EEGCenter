#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   find_dominant_channel  
@Time        :   2022/2/28 3:23 下午
@Author      :   Xuesong Chen
@Description :   
"""
from multiprocessing.pool import Pool

from pandas import MultiIndex
from statsmodels.tsa.stattools import grangercausalitytests
from tqdm import tqdm

from Reader import FIFReader
from src import *
from src.utils import calc_pearsonr_from_df, calc_max_GCI_from_df


def sub_process(reader, stimuli_id):
    event_raw = reader.get_event_raw(stimuli_id)
    signals_arr = event_raw.get_data(picks=channel_names).squeeze()
    signals_df = pd.DataFrame(signals_arr.T, columns=channel_names)
    tmp = calc_pearsonr_from_df(signals_df, n_bias_samples=int(bp_samp_freq * 0.2), step=10)

    # tmp = calc_pearsonr_from_df(signals_df, n_bias_samples=0)
    return tmp  # df


def sub_process_causality(reader, stimuli_id):
    '''
        通过因果推断来寻找主导脑区
    Parameters
    ----------
    reader
    stimuli_id

    Returns
    -------

    '''
    event_raw = reader.get_event_raw(stimuli_id)
    event_raw = event_raw.resample(100)
    signals_arr = event_raw.get_data(picks=channel_names).squeeze()*10e6
    signals_df = pd.DataFrame(signals_arr.T, columns=channel_names)
    tmp = calc_max_GCI_from_df(signals_df, maxlag=10)
    return tmp  # df


def time_domain_correlation():
    tag_to_desc.update({'baseline': 'baseline'})

    my_index = MultiIndex.from_product([user_id_list, list(tag_to_desc.keys()), channel_names],
                                       names=['user', 'stimulus', 'channel'])
    res = pd.DataFrame(
        index=my_index,
        columns=channel_names,
    )

    def print_error(err):
        print('err Info:', err)

    for user_id in tqdm(user_id_list):
        reader = FIFReader(
            f'{FIF_PATH}/{user_id}.fif',
        )
        pool = Pool(len(tag_to_desc))
        tmp_dic = {}

        for stimuli_id in tag_to_desc.keys():
            # _ = sub_process_causality(reader, stimuli_id)
            # print()
            # tmp_dic[stimuli_id] = pool.apply_async(sub_process, args=(reader, stimuli_id), error_callback=print_error)
            tmp_dic[stimuli_id] = pool.apply_async(sub_process_causality, args=(reader, stimuli_id), error_callback=print_error)

        pool.close()
        pool.join()

        for stimuli_id in tag_to_desc.keys():
            res.loc[user_id, stimuli_id] = tmp_dic[stimuli_id].get().values

    res.to_csv('find_dominant_channel_by_causality.csv')


def calc_diff_channels_correlation_time():
    # df = pd.read_csv('不同通道的时域相关性.csv', index_col=[0])
    df = pd.read_csv('find_dominant_channel.csv', index_col=[0])
    corr_df = pd.DataFrame(index=user_id_list, columns=list(tag_to_desc.keys()))
    for (user, stimulus), group in df.groupby(['user', 'stimulus'], sort=False):
        n_top = 3
        max_channels = list(group[channel_names].abs().mean().sort_values(ascending=False).index[:n_top])
        max_v = list(group[channel_names].abs().mean().sort_values(ascending=False).data[:n_top])
        # corr_df.at[user, stimulus] = f"{max_channels[0]}:" + "{:.2f}".format(max_v[0])
        corr_df.at[user, stimulus] = f"{';'.join(max_channels)}"
    corr_df.sort_index(axis=1, ascending=True, inplace=True)
    for sti in list(tag_to_desc.keys()) + ['baseline']:
        n_o = corr_df[sti].str.contains('O').sum()
        n_f = corr_df[sti].str.contains('F').sum()
        n_o_f = corr_df[sti].str.contains('O|F').sum()
        corr_df.at['n_o', sti] = n_o
        corr_df.at['n_f', sti] = n_f
        corr_df.at['n_o_f', sti] = n_o_f
    corr_df.to_csv("top3_dominant_channels.csv")
    # corr_df.to_csv("top1_dominant_channels.csv")
    # res = pd.DataFrame()
    # for region, channels_in_one_region in brain_region.items():
    #     tmp = corr_df[channels_in_one_region].mean(axis=1)
    #     tmp = pd.DataFrame(tmp)
    #     tmp.columns = [region]
    #     res = pd.concat([res, tmp], axis=1)
    # res.T.to_csv('test.csv')


time_domain_correlation()
# calc_diff_channels_correlation_time()

