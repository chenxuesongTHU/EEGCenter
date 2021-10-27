#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   extractFeatures  
@Time        :   2021/10/12 11:31 上午
@Author      :   Xuesong Chen
@Description :   
"""

import matplotlib.pyplot as plt

import Reader
import FeatureExtractor

# STEP 1: 将数据集路径传给Reader中的某个class，获取到统一的数据格式
data_path = "./data/raw/sample"
file_name = data_path + '/1.edf'
anno_file_name = data_path + '/'
raw_edf = Reader.EDFReader(file_name)
print(raw_edf.raw.info)


# STEP 2: 将统一的数据格式交给FeatureExtractor，按照不同方式进行特征提取，并保存至./data/feats/路径下。数据格式见./data/feats/featsFormat.md

print(raw_edf.raw)
psd = FeatureExtractor.PowerSpectralDensity(raw_edf.raw)
print(psd.value)
