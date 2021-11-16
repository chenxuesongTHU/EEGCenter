import numpy as np
import math
from collections import Counter
from .base import BaseFeature


class PermutationEntropy(BaseFeature):
    def __init__(self, raw):
        """
            win_size 滑动时窗的长度
            t 时间间隔
        """
        BaseFeature.__init__(self, raw)
        win_size = 1000
        t = 1

        # 将转化为数组,方便数据处理
        data = self._raw.get_data()
        entropy_list = []
        for i in range(data.shape[0]):
            x = data[i, :]
            # 将x转化为矩阵
            X = []
            if t == 1:
                length = int(len(x) - win_size + 1)
            else:
                length = int((len(x) - win_size + 1) / t) + 1
            for i in range(length):
                X.append(x[i * t:i * t + win_size])
            # 检查X的长度是否大于m!,如果是则分开计算
            loop = 1
            if len(X) > math.factorial(win_size):
                loop = int(len(X) / math.factorial(win_size)) + 1
            # 对X每一行进行由小到大排序，并返回排序后的索引,并将索引转化为字符串
            index = []
            for i in X:
                index.append(str(np.argsort(i)))
            # 计算排列熵
            entropy = [0] * loop
            for temp in range(loop):
                # 计算索引每一种的个数
                if loop == 1 or temp == loop - 1:
                    count = Counter(index[temp * math.factorial(win_size):])
                else:
                    count = Counter(index[temp * math.factorial(win_size):(temp + 1) * math.factorial(win_size)])
                # 计算每一个排列熵
                for i in count.keys():
                    entropy[temp] += -(count[i] / math.factorial(win_size)) * math.log(
                        count[i] / math.factorial(win_size),
                        math.e)
            entropy_list.append(entropy)
        self._value = np.array(entropy_list)
