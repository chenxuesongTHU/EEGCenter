#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   generate_special_time_info  
@Time        :   2022/1/13 2:48 下午
@Author      :   Xuesong Chen
@Description :   
"""
import sys
from collections import defaultdict

from src.sleep.constants import *
from src.constants import *

def get_sound_id(sound):
    for _id, _name in tag_to_desc.items():
        if sound in _name or _name in sound:
            return _id
    sys.exit(-1)


def get_special_time_spans():
    file = open(f'{DATA_PATH}/data/timeAlignment.txt', 'r')
    # user id -> sound id -> band name -> list
    special_time_spans = defaultdict(lambda:
                                     defaultdict(lambda:
                                                 defaultdict(lambda: [])))

    bands = ['alpha_peak', 'alpha_valley', 'theta_peak']

    for line in file.readlines():
        line = line.strip()
        cells = line.split('\t')
        user_id = cells[0]
        sound = cells[1]
        sound_id = get_sound_id(sound)
        cur_band_id = 0
        times = []
        for _cell in cells[2:]:
            if _cell == "":
                continue
            elif _cell != '-1':
                times.append(int(_cell))
            else:
                print(user_id, sound_id, bands[cur_band_id])
                if user_id == 'p16' and sound_id == 'A3':
                    print()
                if times == []:
                    cur_band_id += 1
                    continue
                special_time_spans[user_id][sound_id][bands[cur_band_id]] = times
                times = []
                cur_band_id += 1

    return special_time_spans

get_special_time_spans()

