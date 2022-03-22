#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   find_dominant_channel  
@Time        :   2022/2/28 3:23 下午
@Author      :   Xuesong Chen
@Description :   
"""
from multiprocessing.pool import Pool

import numpy as np
from pandas import MultiIndex

from Reader import FIFReader
from src import *
from src.sleep.utils import get_user_ratings
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
    signals_arr = event_raw.get_data(picks=channel_names).squeeze() * 10e6
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

    # for user_id in tqdm(user_id_list):
    batch_size = 5
    for user_id_idx in range(0, len(user_id_list), batch_size):
        tmp_user_id_list = user_id_list[user_id_idx: user_id_idx + batch_size]
        # print(tmp_user_id_list, len(tag_to_desc) * len(tmp_user_id_list))
        # continue
        tmp_dic = defaultdict(lambda: defaultdict(lambda: None))
        pool = Pool(len(tag_to_desc) * len(tmp_user_id_list))
        for user_id in tmp_user_id_list:
            reader = FIFReader(
                f'{FIF_PATH}/{user_id}.fif',
            )
            for stimuli_id in tag_to_desc.keys():
                # _ = sub_process_causality(reader, stimuli_id)
                # print()
                # tmp_dic[user_id][stimuli_id] = pool.apply_async(sub_process, args=(reader, stimuli_id), error_callback=print_error)
                tmp_dic[user_id][stimuli_id] = pool.apply_async(sub_process_causality, args=(reader, stimuli_id),
                                                       error_callback=print_error)

        pool.close()
        pool.join()

        for user_id in tmp_user_id_list:
            for stimuli_id in tag_to_desc.keys():
                res.loc[user_id, stimuli_id] = tmp_dic[user_id][stimuli_id].get().values

        res.to_csv('find_dominant_channel_by_causality.csv')


def calc_diff_channels_correlation_time():

    extra_file_name = '_by_causality'
    # extra_file_name = ''
    # df = pd.read_csv('不同通道的时域相关性.csv', index_col=[0])
    df = pd.read_csv(f'find_dominant_channel{extra_file_name}.csv', index_col=[0])
    # df = pd.read_csv('find_dominant_channel_by_causality.csv', index_col=[0])
    corr_df = pd.DataFrame(index=user_id_list, columns=list(tag_to_desc.keys()))
    n_top = 10
    for (user_id, stimulus_id), group in df.groupby(['user', 'stimulus'], sort=False):
        max_channels = list(group[channel_names].abs().mean().sort_values(ascending=False).index[:n_top])
        max_v = list(group[channel_names].abs().mean().sort_values(ascending=False).data[:n_top])
        rating = get_user_ratings(user_id, stimulus_id=stimulus_id)
        # corr_df.at[user, stimulus] = f"{max_channels[0]}:" + "{:.2f}".format(max_v[0])
        _n_o = 0
        _n_f = 0
        for _chan in max_channels:
            if 'O' in _chan:
                _n_o += 1
            if 'F' in _chan:
                _n_f += 1
        if stimulus_id != 'baseline':
            sleepiness = str(rating['困倦'])
        else:
            sleepiness = str(rating[0]['实验前困倦程度'])
        corr_df.at[user_id, stimulus_id] = f"{';'.join([sleepiness] + max_channels)}"
        # corr_df.at[user_id, stimulus_id] = f"{sleepiness}; O:{_n_o}; F:{_n_f}"
    corr_df.sort_index(axis=1, ascending=True, inplace=True)

    corr_df.to_csv(f"top{n_top}_dominant_channel_name{extra_file_name}.csv")
    return 0

    def get_n_o_f(string):
        str_list = string.split(';')
        str_o = str_list[-2]
        str_f = str_list[-1]
        return {
            'sleepiness': int(str_list[0]),
            'n_o': int(str_o.split(':')[-1]),
            'n_f': int(str_f.split(':')[-1])
        }

    for user_id in user_id_list:

        row = corr_df.loc[user_id]
        baseline = row['baseline']
        _baseline_res = get_n_o_f(baseline)
        _baseline_n_o = _baseline_res['n_o']
        _baseline_n_f = _baseline_res['n_f']
        _baseline_sleepiness = _baseline_res['sleepiness']

        for stimulus_id in list(tag_to_desc.keys()):
            _res = get_n_o_f(row[stimulus_id])
            n_o = _res['n_o']
            n_f = _res['n_f']
            _sleepiness = _res['sleepiness']
            extra_info = ''
            predicted_sleepiness_score = 0

            if n_o < _baseline_n_o:
                predicted_sleepiness_score -= 1
            elif n_o == _baseline_n_o:
                predicted_sleepiness_score += 0
            else:
                predicted_sleepiness_score += 1

            if n_f < _baseline_n_f:
                predicted_sleepiness_score += 1
            elif n_f == _baseline_n_f:
                predicted_sleepiness_score += 0
            else:
                predicted_sleepiness_score -= 1

            if _sleepiness != _baseline_sleepiness:
                if predicted_sleepiness_score > 0:
                    if _sleepiness > _baseline_sleepiness:
                        extra_info = "Y"
                    else:
                        extra_info = "N"
                # if predicted_sleepiness_score == 0:
                #     if _sleepiness == _baseline_sleepiness:
                #         extra_info = "Y"
                #     else:
                #         extra_info = "N"
                if predicted_sleepiness_score < 0:
                    if _sleepiness < _baseline_sleepiness:
                        extra_info = "Y"
                    else:
                        extra_info = "N"

            corr_df.loc[user_id, stimulus_id] += f';{extra_info}'


    for sti in list(tag_to_desc.keys()) + ['baseline']:
        n_o = corr_df[sti].str.contains('O').sum()
        n_f = corr_df[sti].str.contains('F').sum()
        n_o_f = corr_df[sti].str.contains('O|F').sum()
        corr_df.at['n_o', sti] = n_o
        corr_df.at['n_f', sti] = n_f
        corr_df.at['n_o_f', sti] = n_o_f
    # corr_df.to_csv(f"top{n_top}_dominant_channels_by_causality.csv")
    corr_df.to_csv(f"top{n_top}_dominant_channels.csv")
    # corr_df.to_csv("top1_dominant_channels.csv")
    # res = pd.DataFrame()
    # for region, channels_in_one_region in brain_region.items():
    #     tmp = corr_df[channels_in_one_region].mean(axis=1)
    #     tmp = pd.DataFrame(tmp)
    #     tmp.columns = [region]
    #     res = pd.concat([res, tmp], axis=1)
    # res.T.to_csv('test.csv')

def calc_overlap():
    max_correlation_df = pd.read_csv("top10_dominant_channel_name.csv", index_col=[0])
    causality_df = pd.read_csv("top10_dominant_channel_name_by_causality.csv", index_col=[0])

    intersection_list = []

    for user_id in user_id_list:
        for sti_id in list(tag_to_desc.keys()) + ['baseline']:
            cor_list = max_correlation_df.loc[user_id, sti_id].split(';')[1:]
            causality_list = causality_df.loc[user_id, sti_id].split(';')[1:]
            intersection_length = len(set(cor_list).intersection(causality_list))
            intersection_list.append(intersection_length)

    print(np.mean(intersection_list))


def random_selection():
    a = list(range(1, 63, 1))
    b = list(range(1, 63, 1))
    import random
    res = []
    while True:
        a_samp = random.sample(a, 10)
        b_samp = random.sample(b, 10)
        res.append(len(set(a_samp).intersection(b_samp)))
        print(np.mean(res))


time_domain_correlation()
# calc_diff_channels_correlation_time()
calc_overlap()
# random_selection()
