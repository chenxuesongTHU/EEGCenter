#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   convert_csv_to_epoch_timestamp  
@Time        :   2021/12/8 12:05 下午
@Author      :   Xuesong Chen
@Description :   
"""

import argparse
import os

import pandas as pd

parser = argparse.ArgumentParser(
    description='提取csv文件中关注的epoch的开始和结束时间',
    usage='example: python3 convert_csv_to_epoch_timestamp.py',
    # epilog='底部显示信息'
)

parser.add_argument('-c', '--tag_col', dest='tag_col', type=str, default='C', help='epoch所在列的列名')
parser.add_argument('-t', '--tags', dest='tags', nargs='+', type=str,
                    default=['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4'],
                    help='所关注的epoch名称')
parser.add_argument('-sp', '--src_path', dest='src_path', type=str,
                    # default='/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/original/',
                    default='/Volumes/ExtremeSSD/EEGAndSound/datasets/log/',
                    help='trigger文件夹路径')
parser.add_argument('-dp', '--dst_path', dest='dst_path', type=str,
                    # default='/Users/cxs/project/EEGCenterV2/EEGCenter/data/EEGAndMusic/annotations/new/',
                    default='/Volumes/ExtremeSSD/EEGAndSound/datasets/useful_log/',
                    help='生成文件的存储路径')
params = parser.parse_args()
files = os.listdir(params.src_path)
for file_name in files:
    print(file_name.split('.')[0])
    file_path = f'{params.src_path}{file_name}'
    src_df = pd.read_csv(file_path, encoding='GB2312', usecols=['Time', params.tag_col])
    dst_df = pd.DataFrame(index=params.tags, columns=['startTime', 'endTime', 'relax_startTime', 'relax_endTime'])
    dst_df.index.name = 'epoch'
    abbr_to_col = {
        's': 'startTime',
        'e': 'endTime'
    }
    pre_tag = None
    for idx, row in src_df.iterrows():
        time = row['Time']
        trigger = row[params.tag_col]
        epoch, start_or_end = trigger.split('-')
        if pre_tag:
            if epoch.endswith('_1') and start_or_end == 's':
                dst_df.loc[pre_tag, 'relax_'+abbr_to_col[start_or_end]] = time / 1000
            if epoch.endswith('_2') and start_or_end == 'e':
                dst_df.loc[pre_tag, 'relax_'+abbr_to_col[start_or_end]] = time / 1000
                pre_tag = None
        if epoch in dst_df.index:
            pre_tag = epoch
            dst_df.loc[epoch, abbr_to_col[start_or_end]] = time / 1000   # 时间单位为s
    dst_df.to_csv(f'{params.dst_path}{file_name}')

