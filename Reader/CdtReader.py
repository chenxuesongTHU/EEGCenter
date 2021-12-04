# -*- coding: utf-8 -*-
# @Time    : 2021-12-04 15:39
# @Author  : Jerry Chen
# @FileName: CdtReader.py
# @Software: PyCharm

import mne
from .base import BaseReader


class CdtReader(BaseReader):
    def __init__(self, file_name, annotation_file=None):
        BaseReader.__init__(self, file_name, annotation_file)
        self._raw = mne.io.read_raw_curry(self._file_name)
        if self._anno_file:
            if annotation_file.endswith('cdt'):
                self._anno = mne.read_annotations(self._anno_file)
            self._raw.set_annotations(self._anno)
