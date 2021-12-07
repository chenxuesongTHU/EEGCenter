import numpy as np
from .base import BaseFeature


class ApproximateEntropy(BaseFeature):
    def __init__(self, raw, picks):
        """
            win_size 滑动时窗的长度
            r 阈值系数 取值范围一般为：0.1~0.25
        """
        BaseFeature.__init__(self, raw, picks=picks)
        win_size = 100
        r = 0.15

        # 将raw转化为数组
        data = self._raw.get_data(picks=picks)
        entropy_list = []
        for i in range(data.shape[0]):
            x = data[i, :]
            # 将x以win_size为窗口进行划分
            entropy = 0  # 近似熵
            for temp in range(2):
                X = []
                for i in range(len(x) - win_size + 1 - temp):
                    X.append(x[i:i + win_size + temp])
                # X = np.array(X)
                # 计算X任意一行数据与所有行数据对应索引数据的差值绝对值的最大值
                D_value = []  # 存储差值
                for i in X:
                    sub = []
                    for j in X:
                        sub.append(max(np.abs(i - j)))
                    D_value.append(sub)
                # 计算阈值
                F = r * np.std(x, ddof=1)
                # 判断D_value中的每一行中的值比阈值小的个数除以len(x)-win_size+1的比例
                num = np.sum(D_value < F, axis=1) / (len(x) - win_size + 1 - temp)
                # 计算num的对数平均值
                Lm = np.average(np.log(num))
                entropy = abs(entropy) - Lm
            print(entropy)
            entropy_list.append(entropy)
        print(entropy_list)
        self._value = np.array(entropy_list)
