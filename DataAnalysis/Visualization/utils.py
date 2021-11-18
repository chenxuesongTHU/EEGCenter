#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils
@Time        :   2021/11/4 7:59 下午
@Author      :   Xuesong Chen
@Description :
"""
import matplotlib.pyplot as plt
import numpy as np
from DataAnalysis.SleepAid.constants import *

def plot_stage_span(ax, anno, start_sample_id):
    '''
    在脑电变化图像上进行不同stage的背景色标注
    添加图像的ax信息，无需返回
    Parameters
    ----------
    ax: matplotlib.axis
    anno: mne.Annotation
    start_sample_id: 开始的采样点id
    Returns
    -------
    '''
    for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
        event_id = annotation_desc_2_event_id[desc]
        start_pos = (onset-start_sample_id/sfreq)/60            # 单位为minute
        end_pos = (onset-start_sample_id/sfreq+duration)/60     # 单位为minute
        ax.axvspan(start_pos, end_pos, facecolor=color_dic[event_id], alpha=0.5)



def plot_feat_change(feats, feature_name, output_path=None, label=None):
    '''
    将不同用户在同一阶段的脑电特征进行整合绘图
    Parameters
    ----------
    feats
        DataFrame: every column contains a user's brain feat
    Returns
    -------
    '''
    # old method
    # feats_at_time_slots = feats.mean(axis=1)
    # feats_std_at_time_slots = feats.std(axis=1)
    # 删除最大值和最小值后求平均和方差

    if feats.shape[1] >= 4:
        max_idxs = feats.idxmax(axis=1)
        for item in max_idxs.items():
            feats.loc[item] = None

        min_idxs = feats.idxmin(axis=1)
        for item in min_idxs.items():
            feats.loc[item] = None

    feats_at_time_slots = feats.mean(axis=1)
    feats_std_at_time_slots = feats.std(axis=1)

    plt.fill_between(
        np.array(feats.index.values,dtype='float64'),
        feats_at_time_slots.values + feats_std_at_time_slots.values,
        feats_at_time_slots.values - feats_std_at_time_slots.values,
        alpha=0.2)
    feats_at_time_slots.plot(alpha=0.9, label=feats.index.name)
    plt.legend()
    plt.xlabel('time (min)')
    plt.title(feature_name)
    if output_path:
        plt.savefig(f'{output_path}.png')
    elif output_path=='show':
        plt.show()
    else:
        pass
