#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   extractFeatures  
@Time        :   2021/10/12 11:31 上午
@Author      :   Xuesong Chen
@Description :   
"""
import os

import Reader
import FeatureExtractor

# STEP 1: 将数据集路径传给Reader中的某个class，获取到统一的数据格式
data_path = "/Users/cxs/EEG睡眠/papers/数据集/1例失眠患者治疗前后脑电数据/"
file_name = os.path.join(data_path, '1.edf')
raw_edf = Reader.EDFReader(file_name)
# print(raw_edf.raw.info)
# print(raw_edf.raw)


# STEP 2: 将统一的数据格式交给FeatureExtractor，按照不同方式进行特征提取，并保存至./data/feats/路径下。
# psd = FeatureExtractor.PowerSpectralDensity(raw_edf.raw)
# print(psd.value.shape)  # (nchan, 5)
raw_edf.raw.resample(100)
print(raw_edf.raw.info)
ae = FeatureExtractor.PermutationEntropy(raw_edf.raw)
