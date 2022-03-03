#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   utils  
@Time        :   2021/11/4 7:03 下午
@Author      :   Xuesong Chen
@Description :   
"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr

# from scipy.stats.mstats_basic import pearsonr
from statsmodels.tsa.stattools import grangercausalitytests
from tqdm import tqdm


def is_equal_variance(_list_1, _list_2):
    p_value = stats.levene(_list_1, _list_2)[1]
    if p_value < 0.05:
        return False
    else:
        return True


def smooth_dataframe(data, rolling_length=15):
    assert rolling_length % 2 != 0, 'rolling length只能是奇数'
    data = data.rolling(rolling_length, center=True).mean()

    # padding操作：将滑动平均未涉及的值设置为第一个mean值。
    rolling_start_idx = int((rolling_length - 1) / 2)
    for idx in range(rolling_start_idx):
        data.iloc[idx, :] = data.iloc[rolling_start_idx, :]
    for idx in range(rolling_start_idx):
        data.iloc[-idx - 1, :] = data.iloc[-rolling_start_idx - 1, :]

    return data


def nan_pearsonr(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    x[np.where(np.isinf(x))] = np.nan
    y[np.where(np.isinf(y))] = np.nan
    nan_idx_x = np.argwhere(np.isnan(x))
    nan_idx_y = np.argwhere(np.isnan(y))
    nan_idx = np.vstack([nan_idx_x, nan_idx_y]).squeeze()
    x = np.delete(x, nan_idx)
    y = np.delete(y, nan_idx)
    return pearsonr(x, y)


def max_pearsonr(x, y, n_bias_samples, step):
    crop_x = x[n_bias_samples: -n_bias_samples]
    n_crop_x = len(crop_x)
    res = []
    for start_idx in range(0, 2 * n_bias_samples, step):
        r = nan_pearsonr(crop_x, y[start_idx: start_idx + n_crop_x])[0]
        res.append(r)
    if abs(max(res)) > abs(min(res)):
        return max(res)
    else:
        return min(res)


def calc_pearsonr_from_df(df, n_bias_samples=0, step=1):
    columns = list(df.columns)
    correlation_df = pd.DataFrame(index=columns, columns=columns)

    for i, index_feat_name in enumerate(list(columns)):
        for column_feat_name in list(columns[i + 1:]):
            if n_bias_samples == 0:
                _pearson_val = nan_pearsonr(
                    df[index_feat_name], df[column_feat_name]
                )[0]
            else:
                _pearson_val = max_pearsonr(
                    df[index_feat_name], df[column_feat_name], n_bias_samples, step
                )
            correlation_df.at[index_feat_name, column_feat_name] = _pearson_val
            correlation_df.at[column_feat_name, index_feat_name] = _pearson_val
    correlation_df = correlation_df.fillna(1)
    return correlation_df


def get_max_GCI_from_two_cols(df, maxlag=2, test_method='params_ftest'):
    '''
    获取两列df的因果关系
    # todo 不能用p value评价效果
    Parameters
    ----------
    df
    maxlag
    test_method :   候选项详见 grangercausalitytests

    Returns
    -------

    '''
    test_result = grangercausalitytests(df, maxlag=maxlag, verbose=False)
    '''
        Granger causality index: GCI
        假设要判定X->Y的因果性，那么我们应寻找最大的GCI，GCI>0说明存在因果性，若GCI的值越大，说明因果性越强。
    '''
    GCI_list = []
    for i in range(1, maxlag+1):
        GCI_list.append(np.log(np.var(test_result[i][1][0].resid) / np.var(test_result[i][1][1].resid)))
    return max(GCI_list)


def calc_max_GCI_from_df(df, maxlag=5):
    columns = list(df.columns)
    correlation_df = pd.DataFrame(index=columns, columns=columns)

    for index_feat_name in tqdm(columns):
        for column_feat_name in columns:
            _p_val = get_max_GCI_from_two_cols(df[[index_feat_name, column_feat_name]], maxlag=maxlag)
            correlation_df.at[index_feat_name, column_feat_name] = _p_val

    return correlation_df
