#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   FIFReader
@Time        :   2022/1/6 5:34 下午
@Author      :   Xuesong Chen
@Description :   
"""

import mne
from .base import BaseReader
from .Annotation import csvAnnotation
import numpy as np

class FIFReader(BaseReader):
    def __init__(self, file_name, annotation_file=None, offset=0):
        '''

        Parameters
        ----------
        file_name
        annotation_file
        offset: float
            annotation的onset应该前移还是后移动
        '''
        BaseReader.__init__(self, file_name, annotation_file)
        self._raw = mne.io.read_raw_fif(self._file_name)
        self._raw.set_channel_types({'VEO': 'eog'})
        ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')
        self._raw.set_montage(ten_twenty_montage)
        self._anno = self.raw.annotations

    # def get_event_raw(self, event_name):
    #     '''
    #     获取指定event阶段的raw
    #     Parameters
    #     ----------
    #     tag_name: Annotation中指定阶段的名称
    #
    #     Returns
    #     -------
    #     event_raw: Raw
    #     '''
    #     tmp_raw = self.raw.copy()
    #     event_idx = np.where(self._anno.description == event_name)
    #     start_time = self._anno.onset[event_idx][0]
    #     duration = self._anno.duration[event_idx][0]
    #     tmax = min(start_time+duration, tmp_raw.last_samp/tmp_raw.info['sfreq'])
    #     return tmp_raw.crop(tmin=start_time, tmax=tmax, include_tmax=False)
    #
