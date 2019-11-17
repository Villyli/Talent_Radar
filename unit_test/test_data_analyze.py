# 用于简单的数据统计
import matplotlib.pyplot as plt
from file_tools import lists_processer
import numpy as np


class Test_dataAnalyze():

    def test_analyze_units(self):
        # 统计单位数量'
        list_pro = lists_processer()
        unit_lists = list_pro.get_work_unit_list()
        dic = {}
        for item in unit_lists:
            if item in dic:
                dic[item] += 1
            else:
                dic[item] = 1
        keys = list(dic.keys())
        values = np.array(list(dic.values()))
        plt.bar(keys, values)
        plt.show()
        assert 1 == 1
        pass
