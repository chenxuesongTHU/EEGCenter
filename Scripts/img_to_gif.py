#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   img_to_git  
@Time        :   2021/12/14 6:51 下午
@Author      :   Xuesong Chen
@Description :   
"""
import functools
import os

import imageio

from src.sleep.constants import *

def file_cmp(x, y):
    x_idx = float(x.split('_')[-2])
    y_idx = float(y.split('_')[-2])
    if x_idx > y_idx:
        return 1
    elif x_idx == y_idx:
        return 0
    else:
        return -1

# all_file = os.listdir(f'../output/music_and_eeg/')

user_id = 'p02'
root_path = f'../output/music_and_eeg/norm/{user_id}_{user_id_to_name[user_id]}'
os.makedirs(root_path, exist_ok=True)
os.makedirs(f'{root_path}/gif/', exist_ok=True)
for tag, desc in tag_to_desc.items():
    if tag not in ['A1', 'B1']:
        continue
    images = []
    filenames = sorted(
        (fn for fn in os.listdir(root_path) if fn.endswith('.png') and fn.startswith(tag)))
    filenames = sorted(filenames,
                       key=functools.cmp_to_key(file_cmp)
                       )
    for filename in filenames:
        filename = os.path.join(root_path, filename)
        images.append(imageio.imread(filename))
    imageio.mimsave(f'{root_path}/gif/{tag}_{desc}.gif', images, duration=0.2)
