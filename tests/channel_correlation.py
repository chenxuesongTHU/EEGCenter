#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   channel_correlation  
@Time        :   2022/3/22 11:32 上午
@Author      :   Xuesong Chen
@Description :   
"""

import matplotlib
from scipy.stats import pearsonr

from Reader import BrainVisionReader
from src import *
from src.utils import calc_phrase_bias_from_df

matplotlib.use('TkAgg')


def plot_average(raw):
    plt.figure()
    df = raw.to_data_frame()
    df.drop('time', axis=1, inplace=True)
    plt.plot(df.mean(axis=1)[:1000])
    plt.show()


user_id = 'p01'
# reader = FIFReader(
#     f'{FIF_PATH}/{user_id}.fif',
# )
# plot_average(reader.raw)
bv_reader = BrainVisionReader(f'{RAW_EEG_PATH}/{user_id}.vhdr', f'{LOG_PATH}/{user_id}.csv')
# raw = bv_reader.raw.load_data().notch_filter(freqs=(50, 100, 150, 200))
tmp_raw = bv_reader.get_event_raw('A1')
tmp_raw = tmp_raw.load_data().filter(0.5, 40)
avg_raw = tmp_raw.copy().set_eeg_reference(ref_channels='average', projection=False)
ear_raw = tmp_raw.copy().set_eeg_reference(ref_channels=['TP9', 'TP10'])

tmp_df = tmp_raw.to_data_frame()
avg_df = avg_raw.to_data_frame()
ear_df = ear_raw.to_data_frame()

print(pearsonr(tmp_df['Fp1'], avg_df['Fp1']))
print(pearsonr(tmp_df['Fp1'], ear_df['Fp1']))
print(pearsonr(avg_df['Fp1'], ear_df['Fp1']))

# avg_raw.pick_channels(['O2', 'Oz', 'Fpz', 'O1']).plot()
# ear_raw.pick_channels(['O1', 'Oz', 'Fpz', 'O2']).plot()

avg_cov, avg_bias = calc_phrase_bias_from_df(avg_raw.to_data_frame(), n_bias_samples=int(bp_samp_freq * 0.01),
                                   step=1)
ear_cov, ear_bias = calc_phrase_bias_from_df(ear_raw.to_data_frame(), n_bias_samples=int(bp_samp_freq * 0.01),
                                   step=1)

avg_cov.to_csv('avg_cov.csv')
avg_bias.to_csv('avg_bias.csv')
ear_cov.to_csv('ear_cov.csv')
ear_bias.to_csv('ear_bias.csv')

# plot_average(tmp_raw)
# tmp_raw = raw.copy().crop(tmin=8*60, tmax=13*60)
# avg_ref = tmp_raw.set_eeg_reference()
# tmp_cor, tmp_bias = calc_phrase_bias_from_df(tmp_raw.to_data_frame(), n_bias_samples=int(bp_samp_freq * 0.01),
#                                              step=1)
