#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   constants  
@Time        :   2021/12/14 4:47 下午
@Author      :   Xuesong Chen
@Description :   
"""

# 预实验
desc_to_tag = {
    '粉噪音': 'A1',
    '郭德纲相声': 'B1',
    '喜马拉雅': 'A2',
    '蒋勋细说红楼梦': 'B2',
    '睡眠协会': 'A3',
    '斗破苍穹': 'B3',
    '巴赫钢琴曲': 'A4',
    '鬼吹灯': 'B4'
}

tag_to_desc = {
    'A1': '粉噪音',
    'B1': '郭德纲相声',
    'A2': '喜马拉雅',
    'B2': '蒋勋细说红楼梦',
    'A3': '睡眠协会',
    'B3': '斗破苍穹',
    'A4': '巴赫钢琴曲',
    'B4': '鬼吹灯',

}

# desc_to_tag = {
#     '粉噪音': 'A1',
#     '喜马拉雅': 'A2',
#     '催眠协会': 'A3',
#     '古典音乐': 'A4',
#     '郭德纲相声': 'B1',
#     '蒋勋细说红楼梦': 'B2',
#     '斗破苍芎': 'B3',
#     '鬼吹灯': 'B4'
# }
#
# tag_to_desc = {
#     'A1': '粉噪音',
#     'A2': '喜马拉雅',
#     'A3': '催眠协会',
#     'A4': '古典音乐',
#     'B1': '郭德纲相声',
#     'B2': '蒋勋细说红楼梦',
#     'B3': '斗破苍芎',
#     'B4': '鬼吹灯',
#
# }

user_id_to_name = {
    'p01': '李桂圆',
    'p02': '刘宇航',
    'p03': '韦卓凡',
    'p04': '姚美秋',
    'p05': '李艺林',
    'p06': '徐帅',
    'p07': '周永',
    'p08': '章婉音',
    'p09': '季俊亚',
    'p10': '陈雪松',
    'p11': '韩可人',
    'p12': '周雅玲',
    'p13': '周佳',
    'p14': '贾隆兴',
    'p15': '马骁',
    'p16': '王琛',
    'p17': '王玉斌',
}

''' HRV domain '''
# PPG-BP
start_time_bias = {
    'p01': -5,
    'p02': -2,
    'p03': 0,
    'p04': 0,
    'p05': -1,
    'p10': -1,
    'p11': -1,
    # 'p15': 0,
    'p16': 0,
    'p17': 0
}

hrv_user_id_list = list(start_time_bias.keys())

hrv_samp_freq = 497
