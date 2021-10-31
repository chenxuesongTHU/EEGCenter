#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   EDFReader  
@Time        :   2021/10/9 4:04 下午
@Author      :   Xuesong Chen
@Description :   
"""

import mne
from .base import BaseReader


class EDFReader(BaseReader):
    def __init__(self, file_name, annotation_file=None):
        BaseReader.__init__(self, file_name, annotation_file)
        self._raw = mne.io.read_raw_edf(self._file_name)
        if self._anno_file:
            self._anno = mne.read_annotations(self._anno_file)
