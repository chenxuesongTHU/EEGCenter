#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   base  
@Time        :   2021/12/8 11:56 上午
@Author      :   Xuesong Chen
@Description :   
"""


class BaseAnnotation:
    def __init__(self, file_name):
        self._file_name = file_name
        self._anno = None

    @property
    def annotation(self):
        return self._anno
