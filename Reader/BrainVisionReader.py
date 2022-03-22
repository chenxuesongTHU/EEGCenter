#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   BrainVisionReader  
@Time        :   2021/11/26 3:37 下午
@Author      :   Xuesong Chen
@Description :   
"""

import mne

from .Annotation import csvAnnotation
from .base import BaseReader

'''
'AF3', 'AF4', 'AF7', 'AF8', 
'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 
'CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CPz', 'Cz', 
'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 
'FC1', 'FC2', 'FC3', 'FC4', 'FC5', 'FC6', 
'FT10', 'FT7', 'FT8', 'FT9', 
'Fp1', 'Fp2', 'Fpz', 'Fz', 
'O1', 'O2', 'Oz', 
'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 
'PO3', 'PO4', 'PO7', 'PO8', 'POz', 'Pz', 
'Status', 
'T7', 'T8', 'TP7', 'TP8', 
'VEO']
'''


class BrainVisionReader(BaseReader):
    def __init__(self, file_name, annotation_file=None):
        BaseReader.__init__(self, file_name, annotation_file)
        self._raw = mne.io.read_raw_brainvision(self._file_name)
        if self._anno_file:
            offset = self._raw.annotations.onset[1]
            orig_time = self._raw.annotations.orig_time
            if annotation_file.endswith('edf'):
                self._anno = mne.read_annotations(self._anno_file)
            if annotation_file.endswith('csv'):
                self._anno = csvAnnotation(annotation_file).annotation
            if offset != 0:
                self._anno.onset += offset
                # self._anno.orig_time = orig_time
            self._raw.set_annotations(self._anno)
