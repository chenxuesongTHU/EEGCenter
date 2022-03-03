#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   test_max_pearsonr  
@Time        :   2022/2/25 2:47 下午
@Author      :   Xuesong Chen
@Description :   
"""

from src.utils import max_pearsonr

x1 = [0,1,2,3,4,5,6,7]
x2 = [1,2,3,4,5,6,9,10]
print(
    max_pearsonr(x1, x2, 1)
)
