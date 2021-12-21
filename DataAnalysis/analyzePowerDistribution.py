#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   analyzePowerDistribution  
@Time        :   2021/12/17 4:33 下午
@Author      :   Xuesong Chen
@Description :   
"""
import pandas as pd

from Reader import EDFReader
from Feature.timeFrequency import TimeFrequency
import matplotlib.pyplot as plt
import numpy as np

user_id = 'p10'
reader = EDFReader(
    f'../data/EEGAndMusic/{user_id}-sound-1201_EEG_cleaned.edf',
    f'/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/{user_id}-sound-1201.csv'
)

raw = reader.raw

tf = TimeFrequency(raw, 5)
dim_info, feats = tf.get_band_power_array()
# 避免极值影响，使用median作为baseline
baseline = np.median(feats, axis=0)
baseline = pd.DataFrame(
    baseline, index=dim_info['channel'], columns=dim_info['feature']
)
baseline.to_csv(f'../data/EEGAndMusic/baseline/{user_id}.csv')

print()