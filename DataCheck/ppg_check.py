#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   ppg_check  
@Time        :   2022/1/21 1:46 下午
@Author      :   Xuesong Chen
@Description :   
"""
import pandas as pd
from src.constants import *
from src.sleep.constants import *
from Reader.hrv.hrv_reader import read_ecg_file

src_path = ECG_PATH
for user_id in hrv_user_id_list:
    df = pd.read_csv(f'{PPG_PATH}/{user_id}.csv')
    # ECG_PATH + f'{user_id}.pulse'
    ppg_baseline, ppg_data = read_ecg_file(f'{src_path}/{user_id}.pulse')
    data_duration = len(ppg_data) / hrv_samp_freq
    print(user_id, data_duration, df['relax_endTime'].max())
