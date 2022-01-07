#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   check_duration  
@Time        :   2022/1/6 2:06 下午
@Author      :   Xuesong Chen
@Description :   
"""
from src.constants import *
from Reader import EDFReader

file = open('check_result.log', 'w')

for user_id in user_id_list:
    old_reader = EDFReader(
        f'{DATA_PATH}/datasets/edf/{user_id}.edf',
        f'{LOG_PATH}/{user_id}.csv',
        offset=60 * 5,  # 5 mins
    )
    new_reader = EDFReader(
        f'{DATA_PATH}/datasets/edfV3/{user_id}.edf',
        f'{LOG_PATH}/{user_id}.csv',
        offset=60 * 5,  # 5 mins
    )

    old_reader.raw.crop(tmin=0, tmax=10).plot()
    new_reader.raw.crop(tmin=0, tmax=10).plot()
    print(user_id,
          old_reader.raw.last_samp/old_reader.raw.info['sfreq'],
          new_reader.raw.last_samp/new_reader.raw.info['sfreq'],
          file=file)

