from mne.time_frequency import psd_welch
import numpy as np

FREQ_BANDS = {
    "delta": [0.5, 4],  # 1-3
    "theta": [4, 8],  # 4-7
    "alpha": [8, 13],  # 8-12
    "beta": [13, 31],  # 13-30
    "gamma": [31, 81]  # 31-80
}


class DifferentialEntropy:
    def __init__(self, raw):
        self.raw = raw

        psds, freqs = psd_welch(self.raw, picks='eeg', fmin=0.5, fmax=80.)
        psds /= np.sum(psds, axis=-1, keepdims=True)
        de_feat_list = []

        for fmin, fmax in FREQ_BANDS.values():
            psds_band = psds[:, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
            des_band = np.log2(100 * psds_band)
            de_feat_list.append(des_band.reshape(len(psds), -1))

        self.value = np.concatenate(de_feat_list, axis=1)
