#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils  
@Time        :   2021/11/4 7:03 下午
@Author      :   Xuesong Chen
@Description :   
"""
from scipy import stats


def is_equal_variance(_list_1, _list_2):
    p_value = stats.levene(_list_1, _list_2)[1]
    if p_value < 0.05:
        return False
    else:
        return True
