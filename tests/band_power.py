#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   band_power  
@Time        :   2021/12/31 4:24 下午
@Author      :   Xuesong Chen
@Description :   
"""
import numpy as np
from yasa.spectral import bandpower
from mne.time_frequency.psd import psd_array_welch
import matplotlib.pyplot as plt

a = [0] * 19 + [1] + [0] * 20
a = np.array(a)
a = a.reshape([1, -1])
# a = np.vstack([a, a])
psds, freqs = psd_array_welch(a, sfreq=20, n_per_seg=20)
psds = psds.squeeze()
freqs = freqs.squeeze()
plt.plot(list(freqs), list(psds))
plt.show()
print(psds)
