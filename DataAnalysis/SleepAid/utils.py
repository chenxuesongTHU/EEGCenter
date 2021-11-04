#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils  
@Time        :   2021/11/4 7:53 下午
@Author      :   Xuesong Chen
@Description :   
"""

def get_stage_onset(anno, stage_name="Sleep stage 2"):
    '''
        get the start position of W2 stage
        获取某个sleep stage开始的位置
    Parameters
    ----------
    anno
    Returns
        @idx
            usage: anno[idx]['onset']
    -------
    '''
    for idx, single_stage in enumerate(anno):
        if single_stage['description'] == stage_name:
            return idx
    print(f'{stage_name} is not exist in this recording!')
    import sys; sys.exit()
