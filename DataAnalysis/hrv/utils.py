#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils  
@Time        :   2022/1/25 6:46 下午
@Author      :   Xuesong Chen
@Description :   
"""

from src.sleep.constants import *

def binary_search(nums, target):
    n = len(nums)
    left = 0
    right = n - 1
    ans = n
    while (left <= right):
        mid = left + ((right - left) >> 1)
        if target <= nums[mid]:
            ans = mid
            right = mid - 1
        else:
            left = mid + 1
    return ans


def get_1d_peak_by_annotation(peaks, anno, sound_id):
    time_info = anno.get_timestamp_by_stimuli(sound_id)
    start_samp_idx = int(time_info['start_time'] * hrv_samp_freq)
    end_samp_idx = int(time_info['end_time'] * hrv_samp_freq)
    start_idx = binary_search(peaks, start_samp_idx)
    end_idx = binary_search(peaks, end_samp_idx)
    assert start_samp_idx <= peaks[start_idx]
    assert end_samp_idx <= peaks[end_idx]
    return peaks[start_idx: end_idx]


def get_1d_data_by_annotation(data, anno, sound_id):
    time_info = anno.get_timestamp_by_stimuli(sound_id)
    start_samp_idx = int(time_info['start_time'] * hrv_samp_freq)
    end_samp_idx = int(time_info['end_time'] * hrv_samp_freq)
    return data[start_samp_idx: end_samp_idx]

