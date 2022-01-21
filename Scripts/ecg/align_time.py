#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   align_time  
@Time        :   2022/1/17 3:02 下午
@Author      :   Xuesong Chen
@Description :   
"""

from collections import defaultdict

from src.constants import *
from src.sleep.constants import *

user_ids = list(start_time_bias.keys())


def read_ecg_file(file_path):
    file = open(file_path, 'r')
    line = file.readline()
    line = line.strip()
    res = []
    for n in line.split(','):
        if n == '':
            continue
        res.append(float(n))
    return res


def read_eeg_marker(file_path):
    file = open(file_path, 'r')
    samp_freq = 500
    res = defaultdict(lambda: {})
    for line in file.readlines():
        if line.startswith('Mk1'):
            start_time = line.split(',')[-1]
        if line.startswith('Mk2'):
            trigger_start_sample_id = int(line.split(',')[-3])  # first_trigger
            res['device']['start_time_bias'] = (-1) * trigger_start_sample_id / samp_freq  # 单位为s
        if line.startswith('Mk3'):
            trigger_end_sample_id = int(line.split(',')[-3])
            res['device']['end_time_bias'] = (trigger_end_sample_id - trigger_start_sample_id) / samp_freq  # 单位为s

    return res


def read_tobii_marker(file_path, events):
    '''
    此部分的时间单位为s，该函数实现相较于trigger, 不同事件时间偏移量的计算
    Parameters
    ----------
    file_path
    events: list

    Returns
    -------

    '''
    import pandas as pd
    df = pd.read_excel(file_path)
    df.fillna("", inplace=True)

    res = defaultdict(lambda: {})
    '''开始时间的trigger获取'''
    _tmp = df[df['StudioEvent'] == 'EventMarkerOn']
    first_trigger_start_time = _tmp.iloc[0]['RecordingTimestamp'] / 1000

    for event in events:

        ''' baseline获取 '''
        if event == 'baseline':
            _tmp = df[df['StudioEventData'].str.contains('Instruction Element_1')]
            baseline_start_time = _tmp.iloc[0]['RecordingTimestamp'] / 1000
            res[event]['start_time_bias'] = baseline_start_time - first_trigger_start_time
            _tmp = df[df['StudioEventData'].str.contains('Instruction Element_1_')]
            baseline_end_time = _tmp.iloc[-1]['RecordingTimestamp'] / 1000
            res[event]['end_time_bias'] = baseline_end_time - first_trigger_start_time
            # 如果为300s的baseline，可直接使用此方法
            res[event]['start_time_bias'] = res[event]['end_time_bias'] - 300
        else:
            _tmp = df[df['StudioEventData'].str.contains(event)]
            _start_time = _tmp.iloc[0]['RecordingTimestamp'] / 1000
            _end_time = _tmp.iloc[-1]['RecordingTimestamp'] / 1000
            res[event]['start_time_bias'] = _start_time - first_trigger_start_time
            res[event]['end_time_bias'] = _end_time - first_trigger_start_time

    return res


for user_id in user_ids[-3:-2]:
    tobii_marker = read_tobii_marker(f'{RAW_TOBII_PATH}/{user_id}.xlsx', ['baseline', 'A1'])
    eeg_marker = read_eeg_marker(f'{RAW_EEG_PATH}/{user_id}.vmrk')
    _file_path = RAW_ECG_PATH + f'{user_id}.pulse'
    ecg_signal_list = read_ecg_file(_file_path)
    _time_bias = start_time_bias[user_id]
    # hrv设备开的早，因此当_time_bias<0时，直接将ecg_signal_list向后截取即可
    start_samp_idx = int(-1 * _time_bias * hrv_samp_freq)
    assert start_samp_idx >= 0
    ecg_signal_list = ecg_signal_list[start_samp_idx:]
    trigger_start_idx = int(-1 * eeg_marker['device']['start_time_bias'] * hrv_samp_freq)
    trigger_end_idx = int(eeg_marker['device']['end_time_bias'] * hrv_samp_freq) + trigger_start_idx

    # 有效数据段
    useful_data = ecg_signal_list[trigger_start_idx: trigger_end_idx]

    # baseline数据段
    baseline_start_idx = trigger_start_idx + int(tobii_marker['baseline']['start_time_bias'] * hrv_samp_freq)
    baseline_end_idx = trigger_start_idx + int(tobii_marker['baseline']['end_time_bias'] * hrv_samp_freq)
    baseline_data = ecg_signal_list[baseline_start_idx: baseline_end_idx]

    baseline_data = [str(_) for _ in baseline_data]
    useful_data = [str(_) for _ in useful_data]
    store_baseline_str = ','.join(baseline_data)
    store_useful_data_str = ','.join(useful_data)

    output_file = open(f'{ECG_PATH}{user_id}.pulse', 'w')
    print(store_baseline_str, file=output_file)
    print(store_useful_data_str, file=output_file)
    output_file.close()
