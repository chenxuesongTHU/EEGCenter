import numpy as np
from .base import BaseFeature


class FuzzyEntropy(BaseFeature):
    def __init__(self, raw, picks):
        """
            win_size 滑动时窗的长度
            r 阈值系数 取值范围一般为：0.1~0.25
            n 计算模糊隶属度时的维度
        """
        BaseFeature.__init__(self, raw, picks=picks)
        win_size = 1000
        r = 0.15
        n = 2

        # 将x转化为数组
        data = self._raw.get_data(picks=picks)
        entropy_list = []
        for i in range(data.shape[0]):
            x = data[i, :]
            # 将x以m为窗口进行划分
            entropy = 0  # 近似熵
            for temp in range(2):
                X = []
                for i in range(len(x) - win_size + 1 - temp):
                    X.append(x[i:i + win_size + temp])
                X = np.array(X)
                # 计算X任意一行数据与其他行数据对应索引数据的差值绝对值的最大值
                D_value = []  # 存储差值
                for index1, i in enumerate(X):
                    sub = []
                    for index2, j in enumerate(X):
                        if index1 != index2:
                            sub.append(max(np.abs(i - j)))
                    D_value.append(sub)
                # 计算模糊隶属度
                D = np.exp(-np.power(D_value, n) / r)
                # 计算所有隶属度的平均值
                Lm = np.average(D.ravel())
                entropy = abs(entropy) - Lm
            entropy_list.append(entropy)
        self._value = np.array(entropy_list)
