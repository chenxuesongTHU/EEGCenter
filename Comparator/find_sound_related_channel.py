#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   find_sound_related_channel  
@Time        :   2022/2/23 5:27 下午
@Author      :   Xuesong Chen
@Description :   
"""
from math import log


def calcShanonEnt(dataSet):
    '''
    计算给定数据集的香农熵
    :param dataSet:
    :return:shanonEnt
    '''
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shanonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shanonEnt -= prob * log(prob, 2)
    return shanonEnt


print(
    calcShanonEnt(['1', '2', '2', '2'])
)

print(
    calcShanonEnt(['1', '1', '2', '2'])
)
