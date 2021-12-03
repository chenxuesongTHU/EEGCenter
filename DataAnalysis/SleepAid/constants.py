#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   constants
@Time        :   2021/11/4 7:04 下午
@Author      :   Xuesong Chen
@Description :
"""

annotation_desc_2_event_id = {'Sleep stage W': 1,
                              'Sleep stage 1': 2,
                              'Sleep stage 2': 3,
                              'Sleep stage 3': 4,
                              'Sleep stage 4': 4,
                              'Sleep stage R': 5}

event_id_2_annotation_desc = {1: 'Sleep stage W',
                              2: 'Sleep stage 1',
                              3: 'Sleep stage 2',
                              4: 'Sleep stage 3',
                              5: 'Sleep stage R',
                              0: 'unknow',
                              }

Chinese_medicine_2_event_id = {
    10: 1,
    1: 2,
    2: 3,
    3: 4,
    5: 5,
    0: 0,
    6: 5, #
}
face_color_legend = {
    'W': 1,
    'N1': 2,
    'N2': 3,
    'N3': 4,
    'REM': 5
}
color_dic = {
    1: 'y',
    2: 'g',
    3: 'r',
    4: 'c',
    5: 'm',
}

sfreq = 100  # 采样率
chunk_duration = 60

yasa_feat_list = [
    'eeg_abspow', 'eeg_abspow_c7min_norm', 'eeg_abspow_p2min_norm', 'eeg_alpha', 'eeg_alpha_c7min_norm',
    'eeg_alpha_p2min_norm', 'eeg_at', 'eeg_at_c7min_norm', 'eeg_at_p2min_norm', 'eeg_beta',
    'eeg_beta_c7min_norm', 'eeg_beta_p2min_norm', 'eeg_db', 'eeg_db_c7min_norm', 'eeg_db_p2min_norm',
    'eeg_ds', 'eeg_ds_c7min_norm', 'eeg_ds_p2min_norm', 'eeg_dt', 'eeg_dt_c7min_norm',
    'eeg_dt_p2min_norm', 'eeg_fdelta', 'eeg_fdelta_c7min_norm', 'eeg_fdelta_p2min_norm', 'eeg_hcomp',
    'eeg_hcomp_c7min_norm', 'eeg_hcomp_p2min_norm', 'eeg_higuchi', 'eeg_higuchi_c7min_norm',
    'eeg_higuchi_p2min_norm', 'eeg_hmob', 'eeg_hmob_c7min_norm', 'eeg_hmob_p2min_norm', 'eeg_iqr',
    'eeg_iqr_c7min_norm', 'eeg_iqr_p2min_norm', 'eeg_kurt', 'eeg_kurt_c7min_norm', 'eeg_kurt_p2min_norm',
    'eeg_nzc', 'eeg_nzc_c7min_norm', 'eeg_nzc_p2min_norm', 'eeg_perm', 'eeg_perm_c7min_norm',
    'eeg_perm_p2min_norm', 'eeg_petrosian', 'eeg_petrosian_c7min_norm', 'eeg_petrosian_p2min_norm',
    'eeg_sdelta', 'eeg_sdelta_c7min_norm', 'eeg_sdelta_p2min_norm', 'eeg_sigma', 'eeg_sigma_c7min_norm',
    'eeg_sigma_p2min_norm', 'eeg_skew', 'eeg_skew_c7min_norm', 'eeg_skew_p2min_norm', 'eeg_std',
    'eeg_std_c7min_norm', 'eeg_std_p2min_norm', 'eeg_theta', 'eeg_theta_c7min_norm',
    'eeg_theta_p2min_norm', 'eog_abspow', 'eog_abspow_c7min_norm', 'eog_abspow_p2min_norm', 'eog_alpha',
    'eog_alpha_c7min_norm', 'eog_alpha_p2min_norm', 'eog_beta', 'eog_beta_c7min_norm',
    'eog_beta_p2min_norm', 'eog_fdelta', 'eog_fdelta_c7min_norm', 'eog_fdelta_p2min_norm', 'eog_hcomp',
    'eog_hcomp_c7min_norm', 'eog_hcomp_p2min_norm', 'eog_higuchi', 'eog_higuchi_c7min_norm',
    'eog_higuchi_p2min_norm', 'eog_hmob', 'eog_hmob_c7min_norm', 'eog_hmob_p2min_norm', 'eog_iqr',
    'eog_iqr_c7min_norm', 'eog_iqr_p2min_norm', 'eog_kurt', 'eog_kurt_c7min_norm', 'eog_kurt_p2min_norm',
    'eog_nzc', 'eog_nzc_c7min_norm', 'eog_nzc_p2min_norm', 'eog_perm', 'eog_perm_c7min_norm',
    'eog_perm_p2min_norm', 'eog_petrosian', 'eog_petrosian_c7min_norm', 'eog_petrosian_p2min_norm',
    'eog_sdelta', 'eog_sdelta_c7min_norm', 'eog_sdelta_p2min_norm', 'eog_sigma', 'eog_sigma_c7min_norm',
    'eog_sigma_p2min_norm', 'eog_skew', 'eog_skew_c7min_norm', 'eog_skew_p2min_norm', 'eog_std',
    'eog_std_c7min_norm', 'eog_std_p2min_norm', 'eog_theta', 'eog_theta_c7min_norm',
    'eog_theta_p2min_norm', 'time_hour', 'time_norm', 'epoch', 'time']

yasa_ordered_feat_list = [
    'eog_abspow', 'eeg_petrosian', 'eeg_abspow',  # significant top 3
    'eeg_beta', 'eeg_petrosian_c7min_norm', 'eeg_fdelta',
    'eog_fdelta_c7min_norm', 'eeg_db', 'eeg_perm',
    'eog_petrosian',
]
