#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   test_reader  
@Time        :   2021/11/26 4:22 下午
@Author      :   Xuesong Chen
@Description :   
"""
import sys

import matplotlib.pyplot as plt
import pandas as pd

from Reader import BrainVisionReader, YunRuiReader
from src import *

action_list = [
    '开始',
    '睁眼', '睁眼结束',
    '闭眼', '闭眼结束',
    '纯音乐', '纯音乐结束',
    '白噪音', '白噪音结束',
    '中古典乐', '中古典乐结束',
    '自己喜欢的音乐', '自己喜欢的音乐结束',
]

trails = [
    '睁眼',
    '闭眼',
    '纯音乐',
    '白噪音',
    '中古典乐',
    '自己喜欢的音乐'
]

def adjust_annotation(raw):
    anno = raw.annotations
    onset = anno.onset
    # desc = anno.description
    anno.description = np.array(
        action_list
    )
    # anno.description = np.array(
    #     [
    #         'start',
    #         'open eye', 'open eye end',
    #         '闭眼', '闭眼结束',
    #         '纯音乐', '纯音乐结束',
    #         '白噪音', '白噪音结束',
    #         '中古典乐', '中古典乐结束',
    #         '自己喜欢的音乐', '自己喜欢的音乐结束',
    #     ]
    # )
    new_duration = onset[1:] - onset[:-1]
    anno.duration = np.append(new_duration, [0])
    raw.set_annotations(anno)



def save_data():
    bv_file_path = "/Users/cxs/project/EEGDevice/sleep data/1125-sleep data/eeg data/t01-1125.vhdr"
    yr_file_path = "/Users/cxs/project/EEGDevice/sleep data/1125-sleep data/new equipment data/t01-1125.edf"
    bv_reader = BrainVisionReader(bv_file_path)
    yr_reader = YunRuiReader(yr_file_path)
    adjust_annotation(bv_reader.raw)
    yr_reader.raw.info['meas_date'] = bv_reader.raw.info['meas_date']
    # anno.orig_time = yr_reader.raw.info['meas_date']
    yr_reader.raw.set_annotations(bv_reader.raw.annotations)
    anno = bv_reader.raw.annotations
    # for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
    #     if desc in trails:
    #         bv_tmp = bv_reader.raw.copy().pick_channels(['Fpz'])
    #         bv_trail_raw = bv_tmp.crop(tmin=onset, tmax=onset+duration, include_tmax=False)
    #         sls = yasa.SleepStaging(bv_trail_raw,
    #                                 eeg_name='Fpz')
    #         feat = sls.get_features()
    #         feat = feat[['eeg_alpha', 'eeg_beta', 'eeg_fdelta', 'eeg_sdelta', 'eeg_sigma']]
    #         # feat.plot()
    #         feat.to_csv(f'./output/brain_vision/user_1_{desc}_win_siz=1s.csv')
        # print()
    # print()
    for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
        if desc in trails:
            bv_tmp = yr_reader.raw.copy().pick_channels(['EEG'])
            bv_trail_raw = bv_tmp.crop(tmin=onset, tmax=onset+duration, include_tmax=False)
            sls = yasa.SleepStaging(bv_trail_raw,
                                    eeg_name='EEG')
            feat = sls.get_features()
            feat = feat[['eeg_alpha', 'eeg_beta', 'eeg_fdelta', 'eeg_sdelta', 'eeg_sigma']]
            # feat.plot()
            feat.to_csv(f'./output/yun_rui/user_1_{desc}_win_siz=1s.csv')

    sys.exit(0)
    events, event_id = mne.events_from_annotations(
        bv_reader.raw,
        # event_id=annotation_desc_2_event_id,
        # chunk_duration=30.
    )
    bv_epochs = mne.Epochs(
        raw=bv_reader.raw, events=events,
        event_id=event_id,
        tmin=0, tmax=5 * 60
    )
    yr_epochs = mne.Epochs(
        raw=yr_reader.raw, events=events,
        event_id=event_id,
        tmin=0, tmax=5*60
    )
    # epochs.plot_image(picks=['Fpz'])
    # stage = "白噪音"
    for stage in trails:
        bv_epochs[stage].plot(
            picks=['Fpz'],
            scalings=dict(eeg=1e-6),
            # tmin=0,
            # tmax=5 * 60,  # 5 min
        )
        yr_epochs[stage].plot(
            picks=['EEG'],
            scalings=dict(eeg=1e-5),
            # tmin=0,
            # tmax=5 * 60,  # 5 min
        )
        fig_bv = bv_epochs[stage].load_data().plot_psd(
            picks=['Fpz'],
            tmin=20,
            tmax=5*60,       # 5 min
            # show=False
        )
        # plt.title('brain vision')
        fig_yr = yr_epochs[stage].load_data().plot_psd(
            picks=['EEG'],
            tmin=20,
            tmax=5 * 60,  # 5 min
            # show=False
        )
        print()
        # plt.show()
        # plt.title('yun rui')
        # epochs[stage].plot(
        #     picks=['Fpz'],
        #     scalings=dict(eeg=1e-6)
        # )
        # print(
        #     np.mean(epochs[stage].get_data(picks=['Fpz'])[0][0]) * 10e6, '微伏'
        # )
    # reader.raw.pick('Fpz').plot_psd(
    #     # start=60,
    #     # duration=60,
    #     # picks=['FPz'],
    #     # scalings=dict(
    #     #     eeg=1e-4, resp=1e3, eog=1e-4, emg=1e-7,
    #     #               misc=1e-1)
    # )
    # plt.show()
    # print()


def cmp():
    for stage in trails:
        bv = pd.read_csv(f'./output/brain_vision/user_1_{stage}_win_siz=1s.csv', index_col=0)
        yr = pd.read_csv(f'./output/yun_rui/user_1_{stage}_win_siz=1s.csv', index_col=0)

        for feat in bv.columns:
            plt.figure()
            bv_df = bv[feat]
            yr_df = yr[feat]
            # plt.plot(bv_df.values)
            # plt.plot(yr_df.values)
            bv_df.plot(label='brain vision')
            yr_df.plot(label='yun rui')
            plt.legend()
            plt.title(f'{stage}_{feat}')
            plt.savefig(f'./output/cmp_result_1s/{stage}_{feat}.png')
            plt.close()

if __name__ == '__main__':
    # save_data()
    cmp()

