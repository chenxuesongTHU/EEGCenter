#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   EDFReader  
@Time        :   2021/10/9 4:04 下午
@Author      :   Xuesong Chen
@Description :   
"""

import mne


class EDFReader:
    def __init__(self, file_name, annotation_file):
        self.__raw = mne.io.read_raw_edf(file_name)
        self.__anno = mne.read_annotations(annotation_file)

    @property
    def raw(self):
        return self.__raw
