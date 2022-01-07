#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   bad_channels  
@Time        :   2021/12/31 2:04 下午
@Author      :   Xuesong Chen
@Description :   
"""
from mne.preprocessing import find_bad_channels_maxwell

from src.constants import *
from src.sleep.constants import *

from Reader import EDFReader
import mne

# user_id = user_id_list[0]
user_id = 'p08'

reader = EDFReader(
    f'{EDF_PATH}/{user_id}.edf',
    f'{LOG_PATH}/{user_id}.csv',
    offset=60 * 5,  # 5 mins
)

# reader.raw.set_channel_types({'VEO': 'eog'})
# ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
# reader.raw.set_montage(ten_twenty_montage)

auto_noisy_chs, auto_flat_chs, auto_scores = find_bad_channels_maxwell(
    reader.raw, return_scores=True, verbose=True)

print(auto_noisy_chs)  # we should find them!
print(auto_flat_chs)  # none for this dataset