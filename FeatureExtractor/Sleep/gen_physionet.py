#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   gen_physionet  
@Time        :   2021/11/24 4:23 下午
@Author      :   Xuesong Chen
@Description :   
"""

import os.path
import sys

import numpy as np

sys.path.append('.')
sys.path.append('..')

import matplotlib.patches as mpatches
from mne.datasets.sleep_physionet.age import fetch_data

from DataAnalysis.SleepAid.utils import *
from DataAnalysis.SleepAid.datasets import *
from DataAnalysis.Visualization.utils import *
from src import *
from Reader.EDFReader import EDFReader
from Scripts import convert_label_to_annotations


def get_raw_and_annotation(dataset, user_id, days=1):
    raw = None
    annotation = None

    if dataset == 'physionet':
        [alice_files] = fetch_data(subjects=[user_id], recording=days)
        raw = mne.io.read_raw_edf(alice_files[0])
        annotation = mne.read_annotations(alice_files[1])

    if dataset == 'dodh':
        config = Config()
        annotation = convert_label_to_annotations(dodh_filename_list[user_id], dataset)
        file = os.path.join(config.get('dataset', 'dodh'), f'{dodh_filename_list[user_id]}.edf')
        reader = EDFReader(file)
        raw = reader.raw

    if dataset == 'dodo':
        config = Config()
        annotation = convert_label_to_annotations(dodo_filename_list[user_id], dataset)
        file = os.path.join(config.get('dataset', 'dodo'), f'{dodo_filename_list[user_id]}.edf')
        reader = EDFReader(file)
        raw = reader.raw

    if dataset == 'ChineseMedicine':
        config = Config()
        file_path = os.path.join(config.get('dataset', dataset), f'{user_id}.txt')
        annotation = convert_label_to_annotations(user_id, dataset, file_path)
        file = os.path.join(config.get('dataset', dataset), f'{user_id}.edf')
        reader = EDFReader(file)
        raw = reader.raw

    if raw.info['sfreq'] != 100:
        raw.resample(sfreq)
    assert sfreq == raw.info['sfreq'], 'The sample freq is not 100Hz'

    return raw, annotation


def get_feature_by_user_id(dataset, user_id, feature_name, days=None, obs_mins=20, output='show'):
    if days is None:
        days = [1]

    # [physionet, dodh, dodh]
    raw, annotation = get_raw_and_annotation(dataset, user_id, days)

    first_special_stage_index = get_stage_onset(annotation, stage_name="Sleep stage 1")

    annotation.crop(annotation[first_special_stage_index]['onset'] - obs_mins * 60,
                    annotation[first_special_stage_index]['onset'] + obs_mins * 60)
    raw.set_annotations(annotation, emit_warning=False)
    events_train, _ = mne.events_from_annotations(
        raw, event_id=annotation_desc_2_event_id, chunk_duration=chunk_duration)

    start_sample_id = events_train[0][0]
    diff_stage_idxs = defaultdict(lambda: None)
    for event_id in set(annotation_desc_2_event_id.values()):
        diff_stage_idxs[event_id] = np.squeeze(np.where(events_train[:, -1] == event_id))

    raw.crop(events_train[0][0] / sfreq,
             (events_train[-1][0] + chunk_duration * sfreq - 1) / sfreq)  # 左闭右闭

    eeg_name = None
    eog_name = None
    if dataset == 'ChineseMedicine':
        print('channels:', raw.ch_names)
        for name in ['F4-M1', 'F4-A1']:
            if name in raw.ch_names:
                eeg_name = name
                break
        for name in ['E1-M2', 'LOC-A2']:
            if name in raw.ch_names:
                eog_name = name
                break
    if dataset == 'physionet':
        print('channels:', raw.ch_names)
        eeg_name = "EEG Pz-Oz"
        eog_name="EOG horizontal"
        # for name in ['F4-M1', 'F4-A1']:
        #     if name in raw.ch_names:
        #         eeg_name = name
        #         break
        # for name in ['E1-M2', 'LOC-A2']:
        #     if name in raw.ch_names:
        #         eog_name = name
        #         break
    sls = yasa.SleepStaging(raw,
                            # eeg_name="C3_M2",
                            # eeg_name="F4_O2",
                            eeg_name=eeg_name,
                            eog_name=eog_name,
                            # eog_name="EOG horizontal",
                            # emg_name="EMG1-EMG2",
                            # metadata=dict(age=29, male=True)
                            )

    feat = sls.get_features()

    # 将index修改为分钟
    feat.index *= chunk_duration / 60
    return feat


def physionet():
    dataset = 'physionet'
    res = pd.DataFrame()
    # n_users = len(eval(f'{dataset}_filename_list'))
    n_users = 83
    feat_idx = 0
    for use_idx in range(0, n_users):
        # for day_idx in [1]:
        if use_idx in [36, 52, 39, 68, 69, 78, 79]:
            continue
        for day_idx in [1]:
            plot = False
            tmp = get_feature_by_user_id(
                dataset, use_idx, yasa_ordered_feat_list[feat_idx],
                days=[day_idx], output=plot, obs_mins=10)
            if plot == True:
                continue
            if tmp.shape[0] != 10 * 2:
                continue
            # 删除时间列
            # tmp = tmp.to_numpy()[:, :-2]
            # tmp = np.insert(tmp, 0, np.arange(40), axis=1)
            # res.append(tmp)
            res = pd.concat([res, tmp], axis=0)

    return res

res = physionet()
res.to_csv('./data/20min_win_siz=60s.csv')
