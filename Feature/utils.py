#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils
@Time        :   2021/12/22 2:25 下午
@Author      :   Xuesong Chen
@Description :
"""
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import normalize
from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import robust_scale
from scipy import stats

import matplotlib; matplotlib.use('TkAgg')


__all__ = ['remove_outliers']

def remove_outliers(arr, axis=0, max_deviations=2):
    # 将异常值用mean值代替
    mean = np.mean(arr, axis=axis, keepdims=True)
    standard_deviation = np.std(arr, axis=axis, keepdims=True)
    distance_from_mean = abs(arr - mean)
    outliers = distance_from_mean > max_deviations * standard_deviation
    a = np.where(outliers, mean, arr)
    return a

def robust_scaler(arr):
    transformer = robust_scale(np.arange(1, 10))
    transformer.transform(arr)

if __name__ == '__main__':
    arr_1 = np.array(
        [
            [1., 1, 2, 1, 1, 1, 20],
            [1., -10, 1, 1, 1, 1, 1],
            [1., 1, 1, 1, 1, 1, 1],
            [1., 1, 1, 1, 1, 1, 1],
            [1., 1, 1, 1, 1, 1, 1],
            [1., 1, 1, 1, 1, 1, 1],
        ]
    )

    arr_2 = np.array(
        [
            [
                [1, 1],
                [1, 1],
            ],
            [
                [1, 1],
                [1, 1],
            ],
            [
                [1, 1],
                [1, 1],
            ],
            [
                [1, 1],
                [1, 1],
            ],
            [
                [1, 1],
                [1, 1],
            ],
            [
                [-10, 1],
                [1, 1],
            ],

        ]
    )
    # print(
    #     remove_outliers(arr, axis=0)
    # )
    # min_max_scaler = preprocessing.MinMaxScaler()
    # v_scaled = minmax_scale(X=arr_1, feature_range=(-1, 1))
    # res = robust_scale(np.arange(1, 10))
    alpha = 2
    beta = 5
    # res = stats.beta(alpha, beta)
    fig, axes = plt.subplots(3, 1)
    SAMPLE_SIZE = 100000
    res = [random.betavariate(alpha, beta) for _ in range(1, SAMPLE_SIZE)]
    axes[0].hist(res, bins=100)
    # plt.show()
    # plt.subplots()
    data = np.arange(0, 18)
    data.reshape((2,3,3))
    print()
    v_scaled = minmax_scale(X=res, feature_range=(-1, 1))
    axes[1].hist(v_scaled, bins=100)
    v_robust_scale = robust_scale(X=res)
    axes[2].hist(v_robust_scale, bins=100)
    plt.legend()
    plt.show()

    print(res)

