#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   tsne  
@Time        :   2021/11/24 5:06 下午
@Author      :   Xuesong Chen
@Description :   
"""
# coding='utf-8'
import pandas as pd
from DataAnalysis.SleepAid.constants import *
"""t-SNE对手写数字进行可视化"""
from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D  # 进行3D图像绘制

from sklearn.preprocessing import MinMaxScaler

def get_data():
    digits = datasets.load_digits(n_class=6)
    data = digits.data
    label = digits.target
    n_samples, n_features = data.shape
    return data, label, n_samples, n_features

def get_physionet():
    df = pd.read_csv('../FeatureExtractor/Sleep/data/20min.csv', nrows=400)
    df = df.loc[(df['epoch'] < 20) & (10 < df['epoch'])]
    data = df[yasa_ordered_feat_list[:4]]         # 删除伪label和time col
    # data = data[0:3]
    label = list(df['epoch']-10)
    n_samples, n_features = data.shape
    return data, label, n_samples, n_features


def plot_embedding(data, label, title):
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)

    fig = plt.figure()
    ax = plt.subplot(111)
    for i in range(data.shape[0]):
        plt.text(data[i, 0], data[i, 1], str(label[i]),
                 color=plt.cm.Set1(label[i] / 10.),
                 fontdict={'weight': 'bold', 'size': 9})
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    plt.show()
    # return fig

def plot_embedding_3D(data, label, title):

    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)

    fig = plt.figure()
    ax = Axes3D(fig)
    # 将数据对应坐标输入到figure中，不同标签取不同的颜色，MINIST共0-9十个手写数字
    ax.scatter(data[:, 0], data[:, 1], data[:, 2],
               c=plt.cm.Set1(np.array(label)/10))

    # 关闭了plot的坐标显示
    # plt.axis('off')
    plt.title(title)
    plt.show()


def main():
    data, label, n_samples, n_features = get_data()
    # data, label, n_samples, n_features = get_physionet()
    print('Computing t-SNE embedding')
    tsne = TSNE(n_components=3, init='pca', random_state=0)
    t0 = time()
    result = tsne.fit_transform(data)
    # fig = plot_embedding(result, label,
    #                      't-SNE embedding of the digits (time %.2fs)'
    #                      % (time() - t0))
    fig = plot_embedding_3D(result, label,
                         't-SNE embedding of the digits (time %.2fs)'
                         % (time() - t0))
    plt.show()


if __name__ == '__main__':
    # get_data()
    main()