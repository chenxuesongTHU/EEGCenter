#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   analyzePowerDistribution  
@Time        :   2021/12/17 4:33 下午
@Author      :   Xuesong Chen
@Description :   生成baseline
"""
import pandas as pd

from Reader import EDFReader
from Feature.timeFrequency import TimeFrequency
import matplotlib.pyplot as plt
import numpy as np
from Feature.utils import remove_outliers
from src.constants import *

for user_id in user_id_list:
    reader = EDFReader(
        f'{EDF_PATH}/{user_id}.edf',
        f'{LOG_PATH}/{user_id}.csv'
    )

    raw = reader.raw
    raw = raw.crop(0, 5*60)
    tf = TimeFrequency(raw, 4, step_sec=1)
    dim_info, feats = tf.get_band_power_array()
    # 避免极值影响，仅使用65%的数据求平均
    feats = remove_outliers(feats, axis=0, max_deviations=1)
    baseline = np.mean(feats, axis=0)
    # baseline = np.median(feats, axis=0)
    baseline = pd.DataFrame(
        baseline, index=dim_info['channel'], columns=dim_info['feature']
    )
    baseline.to_csv(f'{RESULTS_PATH}/baseline/{user_id}.csv')

    print()
