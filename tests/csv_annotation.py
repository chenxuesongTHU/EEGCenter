#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   csv_annotation  
@Time        :   2022/1/24 4:08 下午
@Author      :   Xuesong Chen
@Description :   
"""
from Reader.Annotation import csvAnnotation

if __name__ == '__main__':
    timestamp = csvAnnotation('/Volumes/ExtremeSSD/EEGAndSound/datasets/ppg/p02.csv')
    _ = timestamp.get_timestamp_by_stimuli('A1')
