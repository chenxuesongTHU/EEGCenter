#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   redefine_brain_region  
@Time        :   2022/3/4 3:54 下午
@Author      :   Xuesong Chen
@Description :   RQ1: 听不同声音时，根据现有的脑区划分标准，同脑区内的点位是否信号一致性保持在较高水平？
"""
import os
from copy import copy
from multiprocessing import Pool

import matplotlib.pyplot as plt
from PIL import Image
from pandas import MultiIndex

from DataAnalysis.Visualization.utils import plot_topomap
from Reader import FIFReader, BrainVisionReader
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
    # tag_to_desc.update({'baseline': 'baseline'})

    # tag_to_desc = {'baseline': 'baseline'}

    user_id_list = ['p01']

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

            # reader = FIFReader(
            #     f'{FIF_PATH}/{user_id}.fif',
            # )

            reader = BrainVisionReader(f'{RAW_EEG_PATH}/{user_id}.vhdr', f'{LOG_PATH}/{user_id}.csv')

            for stimulus_id in list(tag_to_desc.keys()):

                event_raw = reader.get_event_raw(stimulus_id)

                # test start
                event_raw = event_raw.load_data().filter(0.5, 40)
                event_raw = event_raw.copy().set_eeg_reference(ref_channels='average', projection=False)
                # event_raw = event_raw.copy().set_eeg_reference(ref_channels=['TP9', 'TP10'])
                # end

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

        res_cor.to_csv("csv/tmp/intra_user_correlation.csv")
        res_bias.to_csv("csv/tmp/intra_user_time_bias.csv")

def plot_time_bias():
    # stimulus_id = 'baseline'
    # stimulus_id = 'B1'
    # for stimulus_id in ['baseline', 'A1', 'B1']:
    user_id = "p10"
    n_top = 100
    reader = FIFReader(
        # f'{FIF_PATH}/{user_id}.fif',
        "../data/EEGAndMusic/p10.fif"
    )
    tmp_file_path = './tmp/'

    for stimulus_id in ['baseline', 'A1', 'B1', 'A2']:
        corr_file = f"p10_correlation_{stimulus_id}.csv"
        time_bias_file = f"p10_time_bias_{stimulus_id}.csv"
        corr_file = f"../tests/avg_cov.csv"
        # corr_file = f"../tests/ear_cov.csv"
        # time_bias_file = f"p10_time_bias_{stimulus_id}.csv"
        corr_df = pd.read_csv(corr_file, index_col=[0])
        time_bias_df = pd.read_csv(time_bias_file, index_col=[0])
        corr_df.drop(['time', 'TP9', 'TP10'], axis=0, inplace=True)
        corr_df.drop(['time', 'TP9', 'TP10'], axis=1, inplace=True)

        ratings_str = get_user_ratings_str(user_id=user_id, stimulus_id=stimulus_id)

        for chan in list(corr_df.columns):
            chan = 'Oz'
            most_related_chans = corr_df[chan].abs().sort_values(ascending=False).index[:n_top]
            corr_df[chan][set(corr_df[chan].index)-set(most_related_chans)] = 0
            time_bias_df[chan][set(time_bias_df[chan].index)-set(most_related_chans)] = 0
            cor_fig = plot_topomap(pd.DataFrame(corr_df[chan]), reader.raw.info, chan, vmin=-1, vmax=1, show=True,
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

def plot_correlation_region():

    tag_to_desc.update({'baseline': 'baseline'})

    n_top = 100
    reader = FIFReader(
        # f'{FIF_PATH}/{user_id}.fif',
        "../data/EEGAndMusic/p10.fif"
    )

    corr_df = pd.read_csv("csv/intra_user_correlation.csv", index_col=[0])
    time_bias_df = pd.read_csv("csv/intra_user_time_bias.csv", index_col=[0, 1])

    bp_order_channels = copy(reader.raw.ch_names)
    bp_order_channels.remove('VEO')
    max_time_bias_list = []
    for (user_id, stimulus_id), group in corr_df.groupby(['user', 'stimulus'], sort=False):

        ratings_str = get_user_ratings_str(user_id=user_id, stimulus_id=stimulus_id)
        group.drop('stimulus', axis=1, inplace=True)
        group.set_index(['channel'], inplace=True)
        group = group[bp_order_channels]
        group = group.reindex(bp_order_channels)

        time_bias_group = time_bias_df.loc[user_id, stimulus_id]
        time_bias_group.set_index(['channel'], inplace=True)
        time_bias_group = time_bias_group[bp_order_channels]
        time_bias_group = time_bias_group.reindex(bp_order_channels)

        for chan in list(group.columns):
            most_related_chans = group[chan].abs().sort_values(ascending=False).index[:n_top]
            group[chan][set(group[chan].index)-set(most_related_chans)] = 0
            time_bias_group[chan][set(group[chan].index)-set(most_related_chans)] = 0
            mean_v = round(group[chan].abs().sum()/n_top, 2)
            mean_time_bias_v = round(time_bias_group[chan].abs().sum()/n_top, 4)
            max_time_bias_list.append(max(time_bias_group[chan].abs()))
            print(max(max_time_bias_list))
            cor_fig = plot_topomap(pd.DataFrame(group[chan]), reader.raw.info, chan, vmin=-1, vmax=1, show=False,
                                   title=f'{user_id} {tag_to_desc[stimulus_id]} ref: {chan} cor mean:{mean_v} {ratings_str}')
            bias_fig = plot_topomap(pd.DataFrame(time_bias_group[chan]),
                                    reader.raw.info, chan,
                                    vmin=-0.2, vmax=0.2,
                                    show=False,
                                    title=f'{user_id} {tag_to_desc[stimulus_id]} ref: {chan} time bias mean:{mean_time_bias_v} {ratings_str}')
            cor_fig.savefig(f'{RESULTS_PATH}/EEG/redefine_brain_region/top{n_top}/correlation/{user_id}_{stimulus_id}_{chan}.png', dpi=300)
            bias_fig.savefig(f'{RESULTS_PATH}/EEG/redefine_brain_region/top{n_top}/time_bias/{user_id}_{stimulus_id}_{chan}.png', dpi=300)
            plt.clf()
            plt.close(cor_fig)
            plt.close(bias_fig)

def concat_image(files, target_path, axis=0, same_size=True):
    '''

    Parameters
    ----------
    files
    axis
    -------
    '''
    n_img = len(files)
    if same_size:
        (width, height) = Image.open(files[0]).size
    else:
        widths = []
        heights = []
        for file in files:
            size = Image.open(file).size
            widths.append(size[0])
            heights.append(size[1])
        width = max(widths)
        height = max(heights)

    if axis==0:
        new_img = Image.new('RGB', (width, height*n_img))
        up = 0
        bottom = height
        for image in files:
            # print(image)
            # 将现有图片复制到新的上面 参数分别为图片文件和复制的位置(左上角, 右下角)
            _img = Image.open(image)
            (_width, _height) = _img.size
            if _width < width:
                left = int(width / 2 - _width / 2)
                right = left + _width
            else:
                left = 0
                right = width
            new_img.paste(Image.open(image), (left, up, right, bottom))
            # left += width
            # right += width
            up += height
            bottom += height
            quantity_value = 100
            new_img.save(target_path, quantity=quantity_value)

    if axis==1:
        new_img = Image.new('RGB', (width*n_img, height))
        left = 0
        right = width
        for image in files:
            # print(image)
            # 将现有图片复制到新的上面 参数分别为图片文件和复制的位置(左上角, 右下角)
            _img = Image.open(image)
            (_width, _height) = _img.size
            if _height < height:
                up = int(height / 2 - _height / 2)
                bottom = up + _height
            else:
                up = 0
                bottom = height
            new_img.paste(Image.open(image), (left, up, right, bottom))
            left += width
            right += width
            # up += height
            # bottom += height
        quantity_value = 100
        new_img.save(target_path, quantity=quantity_value)


def concat_stimulus_on_z_position():
    n_top=15
    src_path = f'{RESULTS_PATH}/EEG/redefine_brain_region/top{n_top}/correlation/'
    target_path = f'{RESULTS_PATH}/EEG/redefine_brain_region/top{n_top}/concat/'
    tmp = f'{RESULTS_PATH}/EEG/redefine_brain_region/top{n_top}/tmp/'
    os.makedirs(target_path, exist_ok=True)
    os.makedirs(tmp, exist_ok=True)
    for user_id in user_id_list:
        for channel in channel_names_contains_z:
            A_sti_list = []
            B_sti_list = []
            for stimulus_id in range(1, 5):
                A_sti_list.append(f'{src_path}/{user_id}_A{stimulus_id}_{channel}.png')
                B_sti_list.append(f'{src_path}/{user_id}_B{stimulus_id}_{channel}.png')
            concat_image(A_sti_list, f'{tmp}/A_tmp.png', axis=1)
            concat_image(B_sti_list, f'{tmp}/B_tmp.png', axis=1)
            img_list = [f'{src_path}/{user_id}_baseline_{channel}.png', f'{tmp}/A_tmp.png', f'{tmp}/B_tmp.png']
            concat_image(img_list, f'{target_path}/{user_id}_{channel}.png', axis=0, same_size=False)


# calc_time_bias_among_brain_region()
# plot_correlation_region()
plot_time_bias()
# concat_stimulus_on_z_position()