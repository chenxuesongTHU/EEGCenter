#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   brainSignalChange
@Time        :   2021/11/4 7:51 下午
@Author      :   Xuesong Chen
@Description :
"""
import os.path
import sys

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


mapping = {'EOG horizontal': 'eog',
           'Resp oro-nasal': 'resp',
           'EMG submental': 'emg',
           'Temp rectal': 'misc',
           'Event marker': 'misc'}


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
    # 修改index，若N1前时间不够observation的长度，则在后段对齐
    feat.index += 2 * obs_mins - chunk_duration / 60 - feat.index[-1]
    if not output:
        if feature_name in feat.columns:
            return feat[feature_name]
        else:
            return None

    plt.figure()
    ax = feat.plot(y=feature_name, kind='line')

    plot_stage_span(ax, annotation, start_sample_id)

    plt.xlabel('time (min)')
    # plt.vlines(pos_w1_w2, -1, 10000, color="red")  # 竖线
    patch_list = []
    for stage, id in face_color_legend.items():
        patch_list.append(
            mpatches.Patch(color=color_dic[id], label=stage, alpha=0.5)
        )

    # x_ticks = plt.xticks()[0]
    # x_ticks_label = x_ticks * chunk_duration / 60
    # x_ticks_label = [int(x) for x in x_ticks_label]
    # plt.xticks(x_ticks, x_ticks_label)
    # plt.ylim((1.005, 1.025))
    # plt.ylim((0, 12000))
    # plt.ylim((0, 8000))
    plt.legend(handles=patch_list)
    plt.title(feature_name)
    if output == 'show':
        plt.show()
    else:
        plt.savefig(f'{output}.png')


# run on deepest
def dodh_and_dodo():
    for dataset in ['dodh', 'dodo']:
        feats = pd.DataFrame()
        n_users = len(eval(f'{dataset}_filename_list'))
        # n_users = 10
        feat_idx = 0
        for use_idx in range(0, n_users):
            # for day_idx in [1]:
            for day_idx in [1]:
                plot = True
                tmp = get_feature_by_user_id(
                    dataset, use_idx, yasa_ordered_feat_list[feat_idx],
                    days=[day_idx], output=plot, obs_mins=10)
                if plot:
                    continue
                tmp.name = f'{use_idx}_{day_idx}'
                feats = pd.concat([feats, tmp], axis=1)

        plot_feat_change(feats, yasa_ordered_feat_list[feat_idx], dataset)


# run on mac

def physionet():
    dataset = 'physionet'
    feats = pd.DataFrame()
    # n_users = len(eval(f'{dataset}_filename_list'))
    n_users = 10
    feat_idx = 0
    for use_idx in range(0, n_users):
        # for day_idx in [1]:
        for day_idx in [1]:
            plot = False
            tmp = get_feature_by_user_id(
                dataset, use_idx, yasa_ordered_feat_list[feat_idx],
                days=[day_idx], output=plot, obs_mins=10)
            if plot == True:
                continue
            tmp.name = f'{use_idx}_{day_idx}'
            feats = pd.concat([feats, tmp], axis=1)

    plot_feat_change(feats, yasa_ordered_feat_list[feat_idx], dataset)


# physionet()
def ChineseMedicine():
    dataset = 'ChineseMedicine'
    use_idx = 1
    feat_idx = 0
    feats = pd.DataFrame()
    human_type = 'health'    # health insomnia
    aid_type = ''      # ta-VNS tn-VNS
    stage_type = ''    # before after
    healthy_user_list = ChineseMedicine_user_info['health']
    # healthy_user_list = ChineseMedicine_user_info[human_type][aid_type][stage_type]
    # healthy_user_list = ChineseMedicine_user_info['health']
    # healthy_user_list = [1, 4]
    for use_idx in healthy_user_list:
        # for day_idx in [1]:
        for day_idx in [1]:
            plot = False
            tmp = get_feature_by_user_id(
                dataset, use_idx, yasa_ordered_feat_list[feat_idx],
                days=[day_idx], output=plot, obs_mins=10)
            if plot == True or type(tmp) == type(None):
                continue
            tmp.name = f'{use_idx}_{day_idx}'
            feats = pd.concat([feats, tmp], axis=1)

    output_path = f'./ChineseMedicine/{human_type}_{aid_type}_{stage_type}_'+yasa_ordered_feat_list[feat_idx]
    plot_feat_change(feats, yasa_ordered_feat_list[feat_idx],
                     output_path)
    feats.to_csv(output_path+'.csv')
ChineseMedicine()
