#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   timeFrequency  
@Time        :   2021/12/17 1:_res[bands_name] = 58 下午
@Author      :   Xuesong Chen
@Description :   
"""

import numpy as np
from yasa.others import sliding_window
from yasa.spectral import bandpower, stft_power
import pandas as pd
from Reader import EDFReader
from src.constants import bands_name


class TimeFrequency:
    """
    Automatic time-frequency feature extractor of MNE raw data.

    To run the feature extractor, you must install the
    `yasa <https://github.com/raphaelvallat/yasa>`_ packages.
    `antropy <https://github.com/raphaelvallat/antropy>`_ packages.

    .. versionadded:: 0.1.0

    Parameters
    ----------
    raw : :py:class:`mne.io.BaseRaw`
        An MNE Raw instance.
    win_sec : int or float
        The length of the sliding window, in seconds, used for the Welch PSD
        calculation. Ideally, this should be at least two times the inverse of
        the lower frequency of interest (e.g. for a lower frequency of interest
        of 0.5 Hz, the window length should be at least 2 * 1 / 0.5 =
        4 seconds).
    step_sec : int or float
        The sliding window step length, in seconds.
        If None (default), ``step`` is set to ``window``,
        which results in no overlap between the sliding windows.
    relative : boolean
        If True, bandpower is divided by the total power between the min and
        max frequencies defined in ``band``.
    bands : list of tuples
        List of frequency bands of interests. Each tuple must contain the
        lower and upper frequencies, as well as the band name
        (e.g. (0.5, 4, 'Delta')).


    Notes
    -----

    **1. Features extraction**

    For each win_sec-seconds epoch and each channel, the following features are
    calculated:

    * power in different bands

    The data are automatically downsampled to 100 Hz for faster
    computation.

    References
    ----------
    If you use YASA's default classifiers, these are the main references for
    the `National Sleep Research Resource <https://sleepdata.org/>`_:

    * Dean, Dennis A., et al. "Scaling up scientific discovery in sleep
      medicine: the National Sleep Research Resource." Sleep 39.5 (2016):
      1151-1164.

    * Zhang, Guo-Qiang, et al. "The National Sleep Research Resource: towards
      a sleep data commons." Journal of the American Medical Informatics
      Association 25.10 (2018): 1351-1358.

    Examples
    --------

    >>> import mne
    >>> import yasa
    >>> # Load an EDF file using MNE
    >>> raw = mne.io.read_raw_edf("myfile.edf", preload=True)
    >>> # Initialize the sleep staging instance
    >>> sls = yasa.SleepStaging(raw, eeg_name="C4-M1", eog_name="LOC-M2",
    ...                         emg_name="EMG1-EMG2",
    ...                         metadata=dict(age=29, male=True))
    >>> # Get the predicted sleep stages
    >>> hypno = sls.predict()
    >>> # Get the predicted probabilities
    >>> proba = sls.predict_proba()
    >>> # Get the confidence
    >>> confidence = proba.max(axis=1)
    >>> # Plot the predicted probabilities
    >>> sls.plot_predict_proba()

    """

    def __init__(self, raw, win_sec, step_sec=None, relative=False, bands=None):
        if bands is None:
            bands = [(1, 4, 'Delta'), (4, 8, 'Theta'), (8, 12, 'Alpha'),
                     (12, 16, 'Sigma'), (16, 30, 'Beta'), (30, 40, 'Gamma')]
            # bands = [(4, 8, 'Theta'), (8, 12, 'Alpha'),
            #          (12, 16, 'Sigma'), (16, 30, 'Beta'), (30, 40, 'Gamma')]
        self.raw = raw
        self.sfreq = raw.info['sfreq']
        self.ch_names = raw.ch_names
        self.win_sec = win_sec
        self.times, self.epochs = sliding_window(
            raw.get_data()*1e6,  # convert V to micro V
            sf=self.sfreq,
            window=win_sec, step=step_sec
        )
        # 将times的时刻调整为窗口的中间时刻
        self.times += win_sec / 2
        self.relative = relative
        self.bands = bands

    def get_band_power(self, log_power=False):

        feat_list = []
        for i in range(len(self.epochs)):
            _res = bandpower(self.epochs[i], sf=self.sfreq,
                      ch_names=self.ch_names,
                      win_sec=self.win_sec, relative=self.relative,
                      bands=self.bands)
            if log_power:
                _res[bands_name] = _res[bands_name].apply(lambda x: np.log(x))
                # _res[]
            feat_list.append(_res)

        return feat_list

    def get_band_power_array(self):
        '''
        get the band_power features in np.array format
        Returns
        -------
        (time, channel, feature) :
            three dimension of the array

        feature array :
            3D array of the band_power features
        '''
        feat_list = []
        feat_name_list = None
        for i in range(len(self.epochs)):
            df = bandpower(self.epochs[i], sf=self.sfreq,
                      ch_names=self.ch_names,
                      win_sec=self.win_sec, relative=self.relative,
                      bands=self.bands)
            if not feat_name_list:
                feat_name_list = list(df.columns)
            feat_list.append(df.to_numpy(dtype=float))
        dim_dic = {
            'time': list(self.times),
            'channel': self.ch_names,
            'feature': feat_name_list,
        }
        return dim_dic, np.array(feat_list)


    def get_frequency_power(self, band=(0, 40)):

        bands = []
        for i in range(band[0], band[1]):
            bands.append((i, i+1, f'{i}_{i+1}'))

        feat_list = []
        for i in range(len(self.epochs)):
            feat_list.append(bandpower(self.epochs[i], sf=self.sfreq,
                                            ch_names=self.ch_names,
                                            win_sec=self.win_sec, relative=self.relative,
                                            bands=bands))
        return feat_list


if __name__ == '__main__':
    user_id = 'p02'
    reader = EDFReader(
        f'../data/EEGAndMusic/{user_id}-sound-1201_EEG_cleaned.edf',
        f'/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/{user_id}-sound-1201.csv',
        offset=300
    )
    raw = reader.raw
    raw = raw.crop(tmin=0, tmax=10, include_tmax=False)
    tf = TimeFrequency(raw, win_sec=4, step_sec=1)
    feat = tf.get_band_power()
    print()
    # tf.get_band_power_array()

