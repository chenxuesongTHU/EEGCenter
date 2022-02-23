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


def smooth_dataframe(data, rolling_length=15):

    assert rolling_length % 2 != 0, 'rolling length只能是奇数'
    data = data.rolling(rolling_length, center=True).mean()

    # padding操作：将滑动平均未涉及的值设置为第一个mean值。
    rolling_start_idx = int((rolling_length - 1)/2)
    for idx in range(rolling_start_idx):
        data.iloc[idx, :] = data.iloc[rolling_start_idx, :]
    for idx in range(rolling_start_idx):
        data.iloc[-idx-1, :] = data.iloc[-rolling_start_idx-1, :]

    return data