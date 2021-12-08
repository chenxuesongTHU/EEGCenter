#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   csvAnnotation  
@Time        :   2021/12/8 11:56 上午
@Author      :   Xuesong Chen
@Description :   
"""
import mne
from .base import BaseAnnotation
import pandas as pd

class csvAnnotation(BaseAnnotation):
    def __init__(self, file_name):
        BaseAnnotation.__init__(self, file_name)
        self._raw = mne.io.read_raw_curry(self._file_name)
        if self._anno_file:
            if annotation_file.endswith('cdt'):
                self._anno = mne.read_annotations(self._anno_file)
            self._raw.set_annotations(self._anno)
