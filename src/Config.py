#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   Config  
@Time        :   2021/11/9 7:56 下午
@Author      :   Xuesong Chen
@Description :   
"""

import configparser


class Config:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read("../config.ini")

    def get(self, section, item):
        return self.cf.get(section, item)


if __name__ == '__main__':
    config = Config()
    print(
        config.get('dataset', 'dodh')
    )
