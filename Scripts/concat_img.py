#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   concat_img  
@Time        :   2021/12/29 7:55 下午
@Author      :   Xuesong Chen
@Description :   
"""

import os
from PIL import Image
from src.constants import *
from src.sleep.constants import *

# 单个图片的大小为150*150

def image_concat(path):

    images = []
    imagefile = []
    # 存储所有图片文件名称
    for root, dirs, files in os.walk(path):
        for f in files:
            if f == 'all_sound.png':
                continue
            if f.startswith('._') == False:
                images.append(f)
    images = sorted(images)
    for i in range(len(images)):
        imagefile.append(path + '/' + images[i])

    (width, height) = Image.open(imagefile[0]).size
    TARGET_WIDTH = len(imagefile) * width
    TARGET_HEIGHT = height

    target = Image.new('RGB', (TARGET_WIDTH, TARGET_HEIGHT))
    left = 0
    right = width
    for image in imagefile:
        # print(image)
        # 将现有图片复制到新的上面 参数分别为图片文件和复制的位置(左上角, 右下角)
        target.paste(Image.open(image), (left, 0, right, TARGET_HEIGHT))
        left += width
        right += width
        # 图片的质量 0~100
    quantity_value = 100
    target.save(path + '/all_sound.png', quantity=quantity_value)


if __name__ == '__main__':
    for user_id in user_id_list:
        target_path = f'{RESULTS_PATH}/{user_id}_{user_id_to_name[user_id]}' \
                      f'/img/stimulus_level/norm_among_stimulus/column_oriented'
        image_concat(target_path)
