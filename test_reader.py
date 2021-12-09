#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   test_reader  
@Time        :   2021/11/26 4:22 下午
@Author      :   Xuesong Chen
@Description :   
"""

from Reader import EDFReader
from Reader.Annotation import csvAnnotation
import matplotlib.pyplot as plt

plt.ion()

reader = EDFReader(
    './data/EEGAndMusic/p02-sound-1201_EEG_cleaned.edf',
    '/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/p02-sound-1201.csv'
)
# reader.raw.plot()
anno = reader.raw.annotations
for desc, duration, onset in zip(anno.description, anno.duration, anno.onset):
    tmp = reader.raw.copy()
    trail_raw = tmp.crop(tmin=onset, tmax=onset + duration, include_tmax=False)
    trail_raw.plot()
    print()
print()
