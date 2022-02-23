#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   calc_mean_std_across_files  
@Time        :   2022/2/23 3:36 下午
@Author      :   Xuesong Chen
@Description :   
"""
import pandas as pd

from src import *
import os

dir_path = '/Volumes/ExtremeSSD/EEGAndSound/results/EEG_HRV_correlation/'

assert os.path.exists(f'{dir_path}/mean.csv') == False, print("please remove mean.csv first. ")
assert os.path.exists(f'{dir_path}/std.csv') == False, print("please remove std.csv first. ")
assert os.path.exists(f'{dir_path}/mean_std.csv') == False, print("please remove mean_std.csv first. ")

files = os.listdir(dir_path)
concat_df = pd.DataFrame()
for file in files:
    if file.endswith('csv') and not file.startswith('.'):
        file_path = f'{dir_path}{file}'
        cur_df = pd.read_csv(file_path, index_col=0)
        concat_df = pd.concat([concat_df, cur_df])

concat_df.index.name = 'index'
mean_df = concat_df.groupby('index', sort=False).mean()
std_df = concat_df.groupby('index', sort=False).std()
mean_df.to_csv(f'{dir_path}/mean.csv')
std_df.to_csv(f'{dir_path}/std.csv')

res_array = np.core.defchararray.add(mean_df.values.astype(str), '(')
res_array = np.core.defchararray.add(res_array, std_df.values.astype(str))
res_array = np.core.defchararray.add(res_array, ')')
res_df = pd.DataFrame(res_array, index=mean_df.index, columns=mean_df.columns)
res_df.to_csv(f'{dir_path}/mean_std.csv')
