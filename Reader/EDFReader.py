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
from .Annotation import csvAnnotation


class EDFReader(BaseReader):
    def __init__(self, file_name, annotation_file=None):
        BaseReader.__init__(self, file_name, annotation_file)
        self._raw = mne.io.read_raw_edf(self._file_name)
        if self._anno_file:
            if annotation_file.endswith('edf'):
                self._anno = mne.read_annotations(self._anno_file)
            if annotation_file.endswith('csv'):
                self._anno = csvAnnotation(annotation_file).annotation
            self._raw.set_annotations(self._anno)
