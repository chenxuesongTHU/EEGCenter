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
    def __init__(self, file_name):
        self.raw = mne.io.read_raw_edf(file_name)
