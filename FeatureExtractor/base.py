#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   constants  
@Time        :   2021/10/26 3:20 下午
@Author      :   Xuesong Chen
@Description :   
"""

__all__ = ["FREQ_BANDS", "BaseFeature"]

FREQ_BANDS = {
    "delta": [0.5, 4],  # 1-3
    "theta": [4, 8],  # 4-7
    "alpha": [8, 13],  # 8-12
    "beta": [13, 31],  # 13-30
    "gamma": [31, 81]  # 31-80
}


class BaseFeature:
    def __init__(self, raw):
        self._raw = raw
