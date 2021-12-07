# -*- coding: utf-8 -*-
# @Time    : 2021-12-04 21:02
# @Author  : Jerry Chen
# @FileName: CntReader.py
# @Software: PyCharm


import mne
from .base import BaseReader


class CntReader(BaseReader):
    def __init__(self, file_name, annotation_file=None):
        BaseReader.__init__(self, file_name, annotation_file)
        self._raw = mne.io.read_raw_cnt(self._file_name)
        if self._anno_file:
            if annotation_file.endswith('cdt'):
                self._anno = mne.read_annotations(self._anno_file)
            self._raw.set_annotations(self._anno)
