#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   plotFeatChangeInSingleUser  
@Time        :   2021/11/18 8:05 下午
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib.pyplot as plt
import pandas as pd

from DataAnalysis.SleepAid.datasets import *
from src import *

def get_user_df(user_idx, stage):
    df = pd.read_csv(f'./ChineseMedicine/singleUser/data/{user_idx}.csv', index_col=0)
    return df
    # plt.title(user_idx)

for aid_type in ['ta-VNS', 'tn-VNS']:
    before = ChineseMedicine_user_info['insomnia'][aid_type]['before']
    after = ChineseMedicine_user_info['insomnia'][aid_type]['after']
    for before_idx, after_idx in zip(before, after):

        try:
            plt.figure()
            df_before = get_user_df(before_idx, 'before')
            df_after = get_user_df(after_idx, 'after')
            plt.plot(df_before.index, df_before.values, label='before')
            plt.plot(df_after.index, df_after.values, label='after')
            plt.legend()
            plt.title(f'{before_idx}-{after_idx}')
            plt.savefig(f'./ChineseMedicine/singleUser/img/{aid_type}/{before_idx}-{after_idx}.png')
        except:
            continue

