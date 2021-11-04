#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils  
@Time        :   2021/11/4 7:59 下午
@Author      :   Xuesong Chen
@Description :   
"""

from DataAnalysis.SleepAid.constants import *


def plot_stage_span(ax, anno, start_sample_id, period=30):
    '''
    在脑电变化图像上进行不同stage的背景色标注
    Parameters
    ----------
    ax: matplotlib.axis
    anno: mne.Annotation
    start_sample_id: 开始的采样点id
    period: 特征提取最小单元的时间长度，单位为s

    Returns
    -------
    添加图像的ax信息，无需返回
    '''
    for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
        event_id = annotation_desc_2_event_id[desc]
        start_pos = (onset-start_sample_id/sfreq) / period
        end_pos = (onset-start_sample_id/sfreq+duration) / period
        ax.axvspan(start_pos, end_pos, facecolor=color_dic[event_id], alpha=0.5)

