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

# user_id_list = ['p01', 'p02', 'p03', 'p06']

channel_names = [
    'AF3', 'AF4', 'AF7', 'AF8', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CPz',
    'Cz', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'FC1', 'FC2', 'FC3', 'FC4', 'FC5', 'FC6', 'FT10', 'FT7',
    'FT8', 'FT9', 'Fp1', 'Fp2', 'Fpz', 'Fz', 'O1', 'O2', 'Oz', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'PO3',
    'PO4', 'PO7', 'PO8', 'POz', 'Pz', 'T7', 'T8', 'TP7', 'TP8', 'VEO']

occipital_region = ['O1', 'O2', 'PO3', 'PO4', 'PO7', 'PO8', 'POz', 'Oz']
frontal_region = ['Fp1', 'Fp2', 'Fpz']
temporal_region = ['FT10', 'FT7', 'FT8', 'FT9', 'T7', 'T8', 'TP7', 'TP8']
brain_region_info = {
    'All': channel_names,
    'Frontal': frontal_region,
    'Occipital': occipital_region,
    'Temporal': temporal_region,
}
DATA_PATH = "/Volumes/ExtremeSSD/EEGAndSound/"
EDF_PATH = "/Volumes/ExtremeSSD/EEGAndSound/datasets/edfV3/"
FIF_PATH = "/Volumes/ExtremeSSD/EEGAndSound/datasets/fifV3/"
ECG_PATH = "/Volumes/ExtremeSSD/EEGAndSound/datasets/ecg/"
PPG_PATH = "/Volumes/ExtremeSSD/EEGAndSound/datasets/ppg/"
LOG_PATH = "/Volumes/ExtremeSSD/EEGAndSound/datasets/useful_log/"
RESULTS_PATH = "/Volumes/ExtremeSSD/EEGAndSound/results/"

RAW_ECG_PATH = "/Volumes/ExtremeSSD/EEGAndSound/raw datasets/ecg/"
RAW_EEG_PATH = "/Volumes/ExtremeSSD/EEGAndSound/raw datasets/eeg/"
RAW_TOBII_PATH = "/Volumes/ExtremeSSD/EEGAndSound/raw datasets/log/"
