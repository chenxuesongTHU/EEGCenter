#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   rename_file  
@Time        :   2022/1/17 2:36 下午
@Author      :   Xuesong Chen
@Description :   
"""
import os
from src.sleep import constants
from src.constants import *

dir_path = '/Volumes/ExtremeSSD/EEGAndSound/raw datasets/log/'

for user_id in user_id_list:
    files = os.listdir(dir_path)
    for file in files:
        if user_id in file:
            postfix = file.split('.')[-1]
            new_name = user_id + '.' + postfix
            os.rename(f'{dir_path}{file}', f'{dir_path}{new_name}')
