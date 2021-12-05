from mne.time_frequency import psd_welch
import numpy as np
from .base import *


class PowerSpectralDensity(BaseFeature):
    def __init__(self, raw, picks):
        BaseFeature.__init__(self, raw, picks)

        psds, freqs = psd_welch(self._raw, fmin=0.5, fmax=80., picks=picks)
        psds /= np.sum(psds, axis=-1, keepdims=True)

        psd_feat_list = []
        for fmin, fmax in FREQ_BANDS.values():
            psds_band = psds[:, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
            psd_feat_list.append(psds_band.reshape(len(psds), -1))

        self._value = np.concatenate(psd_feat_list, axis=1)
