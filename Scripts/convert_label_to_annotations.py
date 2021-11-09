#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   gen_annotations  
@Time        :   2021/11/9 4:41 下午
@Author      :   Xuesong Chen
@Description :   
"""
from src import *
import json
from DataAnalysis.SleepAid.constants import *

def convert_label_to_annotations(file_name):
    '''
    将单样本的标注结果转为mne.Annotations
    Parameters
    ----------
    file_name

    Returns
    -------

    '''
    file_path = '../DatasetInterface/dreem-learning-evaluation/annotation_result.json'
    anno_dic = json.load(open(file_path))
    label_list = anno_dic[file_name]
    n_chunk = len(label_list)
    onset = range(0, chunk_duration*n_chunk, chunk_duration)
    duration = [chunk_duration] * n_chunk
    description = list(map(lambda x: event_id_2_annotation_desc[x+1], label_list))
    anno = mne.Annotations(onset=onset,
                    duration=duration,
                    description=description)

    return anno

file_name = '03341d0d-5927-5838-8a5f-1b8ef39d8f57'
convert_label_to_annotations(file_name)