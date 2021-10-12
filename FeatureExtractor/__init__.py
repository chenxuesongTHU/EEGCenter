#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   __init__.py  
@Time        :   2021/10/12 11:29 上午
@Author      :   Xuesong Chen
@Description :   
"""

'''
    频率划分方法：
        delta1=0~2Hz，delta2=2~4Hz，delta=0~4Hz
        theta=4~8Hz
        alpha=8~13Hz
        beta1=13~20Hz，beta2=20~30Hz，beta=13~30Hz
        gamma=30~80Hz
        
    特征：
        差分熵
        功率谱密度, Power Spectral Density, psd
        近似熵app，
        样本熵SampEn ，
        排列熵PmEn ，
        LZ复杂度lzc
'''
# TODO:
#  shuqi: 把这个地方以"中文名, 英文名, 缩写"的形式完善下，
#  每个特征对应一个class，每个class下支持不同窗口时长的特征提取