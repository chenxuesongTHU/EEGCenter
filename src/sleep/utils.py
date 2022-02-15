#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils  
@Time        :   2021/12/22 10:08 下午
@Author      :   Xuesong Chen
@Description :   
"""
import pandas as pd
from collections import defaultdict

def get_user_ratings(user_id, stimulus_id=None):
    root_path = "/Users/cxs/project/EEGCenterV2/EEGCenter"
    sound_orders_df = pd.read_csv(f'{root_path}/data/EEGAndMusic/ratings/soundsOrder.csv')
    questionnaires = pd.read_csv(f'{root_path}/data/EEGAndMusic/ratings/questionnaires.csv')
    sound_order = sound_orders_df[sound_orders_df['被试编号'] == user_id]
    sound_order = sound_order.values.squeeze()[3:]
    res = []
    sleep_score_before = int(questionnaires[questionnaires['用户'] == user_id]['实验前困倦程度'].values.squeeze())
    res.append({'实验前困倦程度': sleep_score_before})
    for sound_id in sound_order:
        dic = {
            '标号': sound_id,
            '困倦': 0,
            '熟悉': 0,
            '喜爱': 0,
        }
        for type in ['困倦', '熟悉', '喜爱']:
            tmp = int(questionnaires[questionnaires['用户'] == user_id][f'{sound_id}{type}程度'].values.squeeze())
            dic[type] = tmp
        res.append(dic)
        if stimulus_id and stimulus_id == sound_id:
            return dic
    return res

def get_sound_order(user_id):
    root_path = "/Users/cxs/project/EEGCenterV2/EEGCenter"
    sound_orders_df = pd.read_csv(f'{root_path}/data/EEGAndMusic/ratings/soundsOrder.csv')
    questionnaires = pd.read_csv(f'{root_path}/data/EEGAndMusic/ratings/questionnaires.csv')
    sound_order = sound_orders_df[sound_orders_df['被试编号'] == user_id]
    sound_order = sound_order.values.squeeze()[3:]
    return list(sound_order)

if __name__ == '__main__':
    # res = get_user_ratings('p01')
    res = get_sound_order('p01')
    print(res)