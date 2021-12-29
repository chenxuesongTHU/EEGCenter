#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   brainRegionCorrelation  
@Time        :   2021/12/23 12:25 上午
@Author      :   Xuesong Chen
@Description :   
"""
import matplotlib
import pandas as pd
import seaborn as sns

from Feature import TimeFrequency
from Feature.utils import remove_outliers
from Reader import EDFReader

# matplotlib.use('MacOSX')
matplotlib.use('TkAgg')
import numpy as np
from src.sleep.constants import *
from src.constants import *

user_id = 'p02'
stimulus = 'A1'

reader = EDFReader(
    f'../data/EEGAndMusic/{user_id}-sound-1201_EEG_cleaned.edf',
    f'/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/{user_id}-sound-1201.csv'
)

event_raw = reader.get_event_raw(stimulus)

eeg_signals = event_raw.get_data(picks=occipital_region).squeeze()
df = pd.DataFrame(np.corrcoef(eeg_signals), index=occipital_region, columns=occipital_region)
df.to_csv('occipital_region_relation.csv')
print()

