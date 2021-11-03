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
    Frequency band division
        delta1=0~2Hz，delta2=2~4Hz，delta=0~4Hz
        theta=4~8Hz
        alpha=8~13Hz
        beta1=13~20Hz，beta2=20~30Hz，beta=13~30Hz
        gamma=30~80Hz
        
    Feature contained
        功率谱密度, Power Spectral Density, psd
        差分熵, Differential Entropy, de
        近似熵, Approximate Entropy, ae
        样本熵, Sample Entropy, se
        模糊熵, Fuzzy Entropy, fe
        排列熵, Permutation Entropy, pe
        LZ复杂度, LZ Complexity, lzc
        
    Feature file format
        output file name: userid_channel.feat
        Each sample occupies one line, and consists of the rest four properties separated by `\t`. 
        - user_id: string; input file name by default;
        - channel: string; such as O1 or O1_02;
        - sample_id: int;
        - task_id: string; the default value is -1, which means exist no task info;
        - feature vector: vector; separated by `,`;
        - label: string;
'''
