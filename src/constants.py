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

'''
AF表示前额叶和额叶的中间区域，
C（Central）表示中央区，
CP表示中央叶和顶叶的中间区域，
F（Frontal）表示额区，
FC表示额叶和中央叶的中间区域，
FP（Prefrontal）表示前额区，
FT表示额叶和颞叶的中间区域，
O（Occipital）表示枕区，
P（Parietal）表示顶区，
PO表示顶区和枕区的中间区域，
T（Temporal）表示颞区，
TP表示颞叶和顶叶的中间区域，
'''
# FP
pre_frontal_region = [
    'Fp1', 'Fp2', 'Fpz'
]

# AF
between_fp_f_region = [
    'AF3', 'AF4', 'AF7', 'AF8'
]

# F
frontal_region = [
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Fz'
]

# FC
between_f_c_region = [
    'FC1', 'FC2', 'FC3', 'FC4', 'FC5', 'FC6'
]

# C
central_region = [
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'Cz'
]

# CP
between_c_p_region = [
    'CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CPz'
]

# FT
frontal_temporal_region = [
    'FT10', 'FT7', 'FT8', 'FT9'
]

# T
temporal_region = [
    'T7', 'T8'
]

# TP
between_t_p_region = [
    'TP7', 'TP8'
]

# P
parietal_region = [
    'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'Pz'
]

# PO
between_p_o_region = [
    'PO3', 'PO4', 'PO7', 'PO8', 'POz'
]

# O
occipital_region = [
    'O1', 'O2', 'Oz'
]

# VEO
veo_region = [
    'VEO'
]

brain_region = {
    'FP': pre_frontal_region,
    'AF': between_fp_f_region,
    'F' : frontal_region,
    'FC': between_f_c_region,
    'C' : central_region,
    'CP': between_c_p_region,
    'FT': frontal_temporal_region,
    'T' : temporal_region,
    'TP': between_t_p_region,
    'P' : parietal_region,
    'PO': between_p_o_region,
    'O' : occipital_region
}


brain_region_info = {
    'All': channel_names,
    'Frontal': frontal_region,
    'Occipital': occipital_region,
    'Temporal': temporal_region,
}
DATA_PATH = "/Volumes/ExtremeSSD/EEGAndSound/"
# DATA_PATH = "/media/pc/ExtremeSSD/EEGAndSound"
DATA_PATH = "/home/cxs/data/eeg/EEGAndSound"
EDF_PATH = f"{DATA_PATH}/datasets/edfV3/"
FIF_PATH = f"{DATA_PATH}/datasets/fifV3/"
ECG_PATH = f"{DATA_PATH}/datasets/ecg/"
PPG_PATH = f"{DATA_PATH}datasets/ppg/"
LOG_PATH = f"{DATA_PATH}/datasets/useful_log/"
RESULTS_PATH = f"{DATA_PATH}/results/"

RAW_ECG_PATH = f"{DATA_PATH}/raw datasets/ecg/"
RAW_EEG_PATH = f"{DATA_PATH}/raw datasets/eeg/"
RAW_TOBII_PATH = f"{DATA_PATH}/raw datasets/log/"
