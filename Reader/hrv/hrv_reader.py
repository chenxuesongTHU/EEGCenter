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
