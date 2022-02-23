#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   EEGloader  
@Time        :   2022/2/15 3:38 下午
@Author      :   Xuesong Chen
@Description :   
"""
import sys

from src import *

class EEGLoader():
    def __init__(self, user_id, stimulus_id):
        tag_to_desc.update({'baseline': 'baseline'})
        path = f'{RESULTS_PATH}/EEG/tables/log_power'
        user_info = f'{user_id}_{user_id_to_name[user_id]}'
        if stimulus_id == 'all':
            stimulus_info = 'all_sounds'
        else:
            stimulus_info = f'{stimulus_id}_{tag_to_desc[stimulus_id]}'
        self.df = pd.read_csv(f'{path}/{user_info}_{stimulus_info}.csv', index_col=[0])

    def get_power(self, bands=None, channels=None, times='All', method="median"):
        res = self.df.copy()
        res = res[bands][res['channel'].isin(channels)]
        res = res.groupby('time', sort=False)
        if method == 'mean':
            res = res.mean()
        elif method == 'median':
            res = res.median()
        else:
            print(f'{method} is not a available method!')
            sys.exit()
        return res

# loader = EEGLoader('p01', 'baseline')
# loader.get_power(bands=["Alpha", "Beta"], channels=["O1", "O2"])

