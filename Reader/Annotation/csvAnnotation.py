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
        df = pd.read_csv(file_name)
        df['duration'] = df['endTime'] - df['startTime']
        self._anno = mne.Annotations(onset=df['startTime'],
                               duration=df['duration'],
                               description=df['epoch'])


