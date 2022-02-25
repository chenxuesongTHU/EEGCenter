#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   entropy  
@Time        :   2022/2/24 11:23 上午
@Author      :   Xuesong Chen
@Description :   
"""

import neurokit2 as nk
import numpy as np

rri_list_1 = np.array([1,2,3,1,2,3])
rri_list_2 = np.array([1,2,4,1,2,3])

print(
    nk.entropy_approximate(rri_list_1)
)

print(
    nk.entropy_approximate(rri_list_2)
)

import numpy as np


class ApEn():

    def __init__(self, U, m, r):
        self.U = U
        self.m = m
        self.r = r
        self.N = len(U)


    def _maxdist(self, x_i, x_j):
        return max([abs(ua - va) for ua, va in zip(x_i, x_j)])

    def _phi(self, m):
        x = [[self.U[j] for j in range(i, i + m - 1 + 1)] for i in range(self.N - m + 1)]
        C = [len([1 for x_j in x if self._maxdist(x_i, x_j) <= self.r]) / (self.N - m + 1.0) for x_i in x]
        return (self.N - m + 1.0)**(-1) * sum(np.log(C))

    def get_val(self):
        return abs(self._phi(self.m+1) - self._phi(self.m))

# Usage example
for i in range(10000):
    u = 3 * np.random.random_sample(100)
    m = 2
    r = 2
    ae = ApEn(u, m, r)
    phi_2 = ae._phi(2)
    phi_3 = ae._phi(3)
    print(phi_2, phi_3)
    assert ae._phi(2) >= ae._phi(3)
    # print(ApEn(_list, 2, 3))


