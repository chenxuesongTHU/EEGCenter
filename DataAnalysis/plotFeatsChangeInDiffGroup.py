#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   plotFeatsChangeInDiffGroup  
@Time        :   2021/11/18 11:54 上午
@Author      :   Xuesong Chen
@Description :   比较不同组用户的脑电变化
"""
import pandas as pd

from src import *
from Visualization.utils import *


def plot_feat_change_in_diff_group(feats_list, feature_name, output_path=None):
    plt.figure()
    plt.ylim((-500, 3000))
    for feats in feats_list[:-1]:
        plot_feat_change(feats, feature_name)
    plot_feat_change(feats_list[-1], feature_name, output_path)
    pass


def all_group():
    for time_stage in ['before']:
        group_1_file_path = 'ChineseMedicine/health___eog_abspow.csv'
        group_2_file_path = f'ChineseMedicine/insomnia_ta-VNS_{time_stage}_eog_abspow.csv'
        group_3_file_path = f'ChineseMedicine/insomnia_tn-VNS_{time_stage}_eog_abspow.csv'
        group_1 = pd.read_csv(group_1_file_path, index_col=0)
        group_1.index.name = 'health'
        group_2 = pd.read_csv(group_2_file_path, index_col=0)
        group_2.index.name = f'insomnia_ta-VNS_{time_stage}'
        group_3 = pd.read_csv(group_3_file_path, index_col=0)
        group_3.index.name = f'insomnia_tn-VNS_{time_stage}'
        plot_feat_change_in_diff_group([group_1, group_2, group_3], 'eog_abspow', f'./ChineseMedicine/comparation/{time_stage}')


def one_group():
    for aid_method in ['insomnia_ta-VNS', 'insomnia_tn-VNS']:
        group_1_file_path = 'ChineseMedicine/health___eog_abspow.csv'
        group_2_file_path = f'ChineseMedicine/{aid_method}_before_eog_abspow.csv'
        group_3_file_path = f'ChineseMedicine/{aid_method}_after_eog_abspow.csv'
        group_1 = pd.read_csv(group_1_file_path, index_col=0)
        group_1.index.name = 'health'
        group_2 = pd.read_csv(group_2_file_path, index_col=0)
        group_2.index.name = f'{aid_method}_before'
        group_3 = pd.read_csv(group_3_file_path, index_col=0)
        group_3.index.name = f'{aid_method}_after'
        plot_feat_change_in_diff_group([group_1, group_2, group_3], 'eog_abspow', f'./ChineseMedicine/comparation/{aid_method}')

if __name__ == '__main__':
    # all_group()
    one_group()
