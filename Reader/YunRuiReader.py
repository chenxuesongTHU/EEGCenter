#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   YunRuiReader  
@Time        :   2021/11/26 5:58 下午
@Author      :   Xuesong Chen
@Description :   
"""

import mne
from .base import BaseReader

class YunRuiReader(BaseReader):
    def __init__(self, file_name, annotation_file=None):
        BaseReader.__init__(self, file_name, annotation_file)
        self._raw = mne.io.read_raw_edf(self._file_name)
        if self._anno_file:
            if annotation_file.endswith('edf'):
                self._anno = mne.read_annotations(self._anno_file)
            self._raw.set_annotations(self._anno)


