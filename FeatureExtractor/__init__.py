#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   __init__.py  
@Time        :   2021/10/12 11:29 上午
@Author      :   Xuesong Chen
@Description :   
"""

from .de import DifferentialEntropy
from .psd import PowerSpectralDensity
from .ae import ApproximateEntropy
from .se import SampleEntropy
from .pe import PermutationEntropy
from .lzc import LZComplexity

'''
    频率划分方法：
        delta1=0~2Hz，delta2=2~4Hz，delta=0~4Hz
        theta=4~8Hz
        alpha=8~13Hz
        beta1=13~20Hz，beta2=20~30Hz，beta=13~30Hz
        gamma=30~80Hz
        
    特征：
        差分熵, Differential Entropy, de
        功率谱密度, Power Spectral Density, psd
        近似熵, Approximate Entropy, ae
        样本熵, Sample Entropy, se
        排列熵, Permutation Entropy, pe
        LZ复杂度, LZ Complexity, lzc
'''
