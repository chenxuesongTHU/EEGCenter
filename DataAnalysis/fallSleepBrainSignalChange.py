#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   brainSignalChange  
@Time        :   2021/11/4 7:51 下午
@Author      :   Xuesong Chen
@Description :   
"""
import os.path

import matplotlib.patches as mpatches
from mne.datasets.sleep_physionet.age import fetch_data

from DataAnalysis.SleepAid.utils import *
from DataAnalysis.SleepAid.datasets import *
from DataAnalysis.Visualization.utils import *
from src import *
from Reader.EDFReader import EDFReader
from Scripts import convert_label_to_annotations


# physionet

def get_raw_and_annotation(dataset, user_id, days=1):
    raw = None
    annotation = None

    if dataset == 'physionet':
        [alice_files] = fetch_data(subjects=[user_id], recording=days)
        raw = mne.io.read_raw_edf(alice_files[0])
        annotation = mne.read_annotations(alice_files[1])

    if dataset == 'dodh':
        config = Config()
        annotation = convert_label_to_annotations(filename_list[0])
        file = os.path.join(config.get('dataset', 'dodh'), f'{filename_list[0]}.edf')
        reader = EDFReader(file)
        raw = reader.raw

    if dataset == 'dodo':
        print()

    return raw, annotation


mapping = {'EOG horizontal': 'eog',
           'Resp oro-nasal': 'resp',
           'EMG submental': 'emg',
           'Temp rectal': 'misc',
           'Event marker': 'misc'}


def get_feature_by_user_id(user_id, feature_name, days=None, obs_mins=20, plot=False):
    if days is None:
        days = [1]

    # [physionet, dodh, dodh]
    raw, annotation = get_raw_and_annotation('dodh', user_id, days)

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

    sls = yasa.SleepStaging(raw,
                            eeg_name="C3_M2",
                            # eeg_name="EEG Pz-Oz",
                            eog_name="EOG1",
                            # eog_name="EOG horizontal",
                            # emg_name="EMG1-EMG2",
                            # metadata=dict(age=29, male=True)
                            )

    feat = sls.get_features()

    feat.index *= chunk_duration / 60  # 将index修改为分钟

    if not plot:
        return feat[feature_name]

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
    plt.show()


# user id in [0, ?]
ALICE, BOB = 0, 1
feats = pd.DataFrame()
for use_idx in range(0, 10):
    # for day_idx in [1]:
    for day_idx in [1]:
        plot = False
        tmp = get_feature_by_user_id(
            use_idx, yasa_ordered_feat_list[1],
            days=[day_idx], plot=plot, obs_mins=10)
        if plot == True:
            continue
        tmp.name = f'{use_idx}_{day_idx}'
        feats = pd.concat([feats, tmp], axis=1)

plot_feat_change(feats, yasa_ordered_feat_list[1])
