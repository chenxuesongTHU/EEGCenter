#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   system_cmd  
@Time        :   2022/1/7 2:23 下午
@Author      :   Xuesong Chen
@Description :   
"""
from src.sleep.constants import *
from src.constants import *
import os

def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = os.path.join(path_data, i) #当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            try:
                os.remove(file_data)
            except:
                pass
        else:
            del_file(file_data)
            os.removedirs(file_data)

for user_id in user_id_list:
    print(user_id)
    target_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}/img/stimulus_level/norm_among_stimulus'
    if os.path.exists(target_path):
        try:
            del_file(target_path)
        except:
            continue