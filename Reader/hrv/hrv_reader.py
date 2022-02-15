#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   hrv_reader  
@Time        :   2022/1/17 7:05 下午
@Author      :   Xuesong Chen
@Description :   
"""


def read_ecg_file(file_path):
    file = open(file_path, 'r')
    baseline = file.readline().strip()
    data = file.readline().strip()
    res_baseline = []
    res_data = []
    for n in baseline.split(','):
        if n == '':
            continue
        assert float(n) == int(float(n))
        res_baseline.append(int(float(n)))
    for n in data.split(','):
        if n == '':
            continue
        assert float(n) == int(float(n))
        res_data.append(int(float(n)))

    return res_baseline, res_data


def read_ppg_and_peak(file_path):
    file = open(file_path, 'r')
    baseline_data = file.readline().strip()
    baseline_peak = file.readline().strip()
    data = file.readline().strip()
    data_peak = file.readline().strip()
    res_baseline = {
        'data': [],
        'peak': []
    }
    res_data = {
        'data': [],
        'peak': []
    }

    # baseline
    for n in baseline_data.split(','):
        if n == '':
            continue
        res_baseline['data'].append(int(float(n)))

    for n in baseline_peak.split(','):
        if n == '':
            continue
        res_baseline['peak'].append(int(float(n)))

    # data
    for n in data.split(','):
        if n == '':
            continue
        res_data['data'].append(int(float(n)))
    for n in data_peak.split(','):
        if n == '':
            continue
        res_data['peak'].append(int(float(n)))

    return res_baseline, res_data


if __name__ == '__main__':
    read_ppg_and_peak('/Volumes/ExtremeSSD/EEGAndSound/datasets/ppg/p01.ppg')
