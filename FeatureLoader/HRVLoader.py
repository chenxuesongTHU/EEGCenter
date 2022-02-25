#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   HRVLoader  
@Time        :   2022/2/15 3:37 下午
@Author      :   Xuesong Chen
@Description :   
"""
import numpy as np

from src import *


class HRVLoader():
    def __init__(self, user_id, stimulus_id):
        tag_to_desc.update({'baseline': 'baseline'})
        path = f'{RESULTS_PATH}/hrv/tables/time_domain_feats/60s'
        user_info = f'{user_id}_{user_id_to_name[user_id]}'
        if stimulus_id == 'all':
            stimulus_info = "all_sounds"
        else:
            stimulus_info = f'{stimulus_id}_{tag_to_desc[stimulus_id]}'
        self.df = pd.read_csv(f'{path}/{user_info}_{stimulus_info}.csv', index_col=[0], na_values='nan')
        self.df.replace(np.inf, np.nan, inplace=True)     # np.inf替换为nan用于删除
        self.df.dropna(axis=1, how='any', inplace=True)   # 删掉包含nan的列
        assert sum(self.df.isnull().any()) == 0

    def get_specific_feature(self, feature_name):
        return pd.DataFrame(self.df[feature_name])

    def get_available_features(self):
        return list(self.df.columns)

    def get_all_features(self):
        return self.df

# loader = HRVLoader('p01', 'baseline')
# feats = loader.get_available_features()
# print()
