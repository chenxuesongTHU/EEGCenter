#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   constants  
@Time        :   2021/12/18 3:15 下午
@Author      :   Xuesong Chen
@Description :   
"""

bands_name = [
    # 'Theta', 'Alpha', 'Sigma', 'Beta', 'Gamma',
    'Delta', 'Theta', 'Alpha', 'Sigma', 'Beta', 'Gamma'
]

bands_freqs = {
    'Delta': (0.5, 4),
    'Theta': (4, 8),
    'Alpha': (8, 12),
    'Sigma': (12, 16),
    'Beta': (16, 30),
    'Gamma': (30, 40)
}

user_id_list = ['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07',
                'p08', 'p09', 'p10', 'p11', 'p13', 'p14', 'p16', 'p17']

occipital_region = ['O1', 'O2', 'PO3', 'PO4', 'PO7', 'PO8', 'POz', 'Oz']

DATA_PATH = "/Volumes/ExtremeSSD/EEGAndSound/"
EDF_PATH = "/Volumes/ExtremeSSD/EEGAndSound/datasets/edfV3/new/not_used"
FIF_PATH = "/Volumes/ExtremeSSD/EEGAndSound/datasets/fifV3/"
LOG_PATH = "/Volumes/ExtremeSSD/EEGAndSound/datasets/useful_log/"
RESULTS_PATH = "/Volumes/ExtremeSSD/EEGAndSound/results/"
