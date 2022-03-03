#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   find_sound_related_channel  
@Time        :   2022/2/23 5:27 下午
@Author      :   Xuesong Chen
@Description :   
"""
import pandas as pd
from pandas import MultiIndex
from tqdm import tqdm

from FeatureLoader import EEGLoader
from Reader import FIFReader
from src import *
from src.utils import calc_pearsonr_from_df


def time_domain_correlation():
    # tag_to_desc.update({'baseline': 'baseline'})
    tag_to_desc = {'A1': '粉噪声'}
    channel_user_id_index = MultiIndex.from_product([channel_names, list(tag_to_desc.keys()), user_id_list],
                                                    names=['channel', 'stimulus', 'user'])
    res = pd.DataFrame(
        index=channel_user_id_index,
        columns=user_id_list,
    )

    reader_dic = {}
    for user_id in user_id_list:
        reader_dic[user_id] = FIFReader(
            f'{FIF_PATH}/{user_id}.fif',
        )

    for chan_name in tqdm(channel_names):
        for stimuli_id in tag_to_desc.keys():
            voltage_df = pd.DataFrame()
            for user_id in user_id_list:
                reader = reader_dic[user_id]
                event_raw = reader.get_event_raw(stimuli_id)
                tmp = event_raw.to_data_frame(picks=[chan_name])
                tmp.rename(columns={chan_name: user_id}, inplace=True)
                voltage_df = pd.concat([voltage_df, tmp[user_id]], axis=1)
            res.loc[chan_name, stimuli_id] = \
                calc_pearsonr_from_df(voltage_df, n_bias_samples=bp_samp_freq * 2, step=50).values

    res.to_csv('听粉噪声的时域相关性.csv')
    pass


def concat_stimuli_power(user_id, bands, channels):
    tag_to_desc.update({'baseline': 'baseline'})
    res = pd.DataFrame()
    for stimuli_id in tag_to_desc.keys():
        eeg_loader = EEGLoader(user_id, stimuli_id)
        cur_eeg_feat = eeg_loader.get_power(bands=bands, channels=[channels], method="mean")
        res = pd.concat([res, cur_eeg_feat], axis=0)
    res.reset_index(drop=True, inplace=True)
    return res


def freq_domain_correlation():
    multi_index = MultiIndex.from_product([channel_names, bands_name, user_id_list],
                                          names=['channel', 'band', 'user'])
    res = pd.DataFrame(
        index=multi_index,
        columns=user_id_list,
    )

    for chan_name in tqdm(channel_names):
        for band in bands_name:
            power_df = pd.DataFrame()
            for user_id in user_id_list:
                cur_eeg_feat = concat_stimuli_power(user_id, band, chan_name)
                cur_eeg_feat.rename(columns={band: user_id}, inplace=True)
                power_df = pd.concat([power_df, cur_eeg_feat[user_id]], axis=1)
            res.loc[chan_name, band] = calc_pearsonr_from_df(power_df, n_bias_samples=3).values

    res.to_csv('不同通道频域相关性.csv')


def calc_diff_channels_correlation_freq():
    df = pd.read_csv('不同通道频域相关性.csv', index_col=[0])
    corr_df = pd.DataFrame(index=bands_name, columns=channel_names)
    for (channel, band), group in df.groupby(['channel', 'band'], sort=False):
        corr_df.at[band, channel] = group.mean().mean()

    res = pd.DataFrame()
    for region, channels_in_one_region in brain_region.items():
        tmp = corr_df[channels_in_one_region].mean(axis=1)
        tmp = pd.DataFrame(tmp)
        tmp.columns = [region]
        res = pd.concat([res, tmp])
    res.T.to_csv('test.csv')


def calc_diff_channels_correlation_time():
    # df = pd.read_csv('不同通道的时域相关性.csv', index_col=[0])
    df = pd.read_csv('听粉噪声的时域相关性.csv', index_col=[0])
    corr_df = pd.DataFrame(index=list(tag_to_desc.keys()), columns=channel_names)
    for (channel, stimulus), group in df.groupby(['channel', 'stimulus'], sort=False):
        corr_df.at[stimulus, channel] = group.mean().mean()

    res = pd.DataFrame()
    for region, channels_in_one_region in brain_region.items():
        tmp = corr_df[channels_in_one_region].mean(axis=1)
        tmp = pd.DataFrame(tmp)
        tmp.columns = [region]
        res = pd.concat([res, tmp], axis=1)
    res.T.to_csv('test.csv')


if __name__ == '__main__':
    # time_domain_correlation()
    # freq_domain_correlation()
    # concat_stimuli_power('p01', 'Alpha', 'O1')
    # calc_diff_channels_correlation_freq()
    calc_diff_channels_correlation_time()
