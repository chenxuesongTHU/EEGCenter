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
raw_edf = Reader.EDFReader(file_name)
print(raw_edf.raw)

# STEP 2: 将统一的数据格式交给FeatureExtractor，按照不同方式进行特征提取并保存

print(raw_edf.raw)
de = FeatureExtractor.DifferentialEntropy(raw_edf.raw)
