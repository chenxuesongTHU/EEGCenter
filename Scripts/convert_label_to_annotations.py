#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   gen_annotations
@Time        :   2021/11/9 4:41 下午
@Author      :   Xuesong Chen
@Description :
"""
import json

from DataAnalysis.SleepAid.constants import *
from src import *


def convert_label_to_annotations(file_name, dataset, datapath=None):
    '''
    将单样本的标注结果转为mne.Annotations
    Parameters
    ----------
    file_name

    Returns
    -------

    '''
    if dataset in ['dodo', 'dodh']:
        file_path = '../data/annotation_result.json'
        anno_dic = json.load(open(file_path))
        label_list = anno_dic[file_name]
    if dataset == 'ChineseMedicine':
        file = pd.read_csv(datapath, sep=',', encoding='utf-16le')
        label_list = list(file['睡眠'])
        label_list = list(map(lambda x: Chinese_medicine_2_event_id[x], label_list))
    n_chunk = len(label_list)
    onset = range(0, chunk_duration * n_chunk, chunk_duration)
    duration = [chunk_duration] * n_chunk
    if dataset in ['dodo', 'dodh']:
        description = list(map(lambda x: event_id_2_annotation_desc[x + 1], label_list))
    if dataset == 'ChineseMedicine':
        description = list(map(lambda x: event_id_2_annotation_desc[x], label_list))
    anno = mne.Annotations(onset=onset,
                           duration=duration,
                           description=description)

    return anno


if __name__ == '__main__':
    file_name = '03341d0d-5927-5838-8a5f-1b8ef39d8f57'
    datapath = '/Users/cxs/EEG睡眠/papers/数据集/1例失眠患者治疗前后脑电数据/1.txt'
    convert_label_to_annotations(file_name, 'ChineseMedicine', datapath)
