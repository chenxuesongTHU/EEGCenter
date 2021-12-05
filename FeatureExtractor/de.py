from mne.time_frequency import psd_welch
import numpy as np
from .base import *


class DifferentialEntropy(BaseFeature):
    def __init__(self, raw, picks):
        BaseFeature.__init__(self, raw, picks=picks)

        psds, freqs = psd_welch(self.raw, fmin=0.5, fmax=80., picks=picks)
        psds /= np.sum(psds, axis=-1, keepdims=True)

        de_feat_list = []
        for fmin, fmax in FREQ_BANDS.values():
            psds_band = psds[:, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
            des_band = np.log2(100 * psds_band)
            de_feat_list.append(des_band.reshape(len(psds), -1))

        self._value = np.concatenate(de_feat_list, axis=1)
