"""
对文件操作的工具
"""

import os
import pandas as pd


class lists_processer:
    """
    用于处理list的类
    """

    def __init__(self, cols=[1, 6]):
        self.cols = cols
        self.lists = self.get_lists()
        pass

    def get_lists(self, dir_path="name_lists"):
        '''
        :param dims: 返回的读取csv中的列编号，默认为姓名、学校
        :return: lists数组
        '''
        # 构造文件名
        list_files = os.listdir("../" + dir_path)  # 返回文件名
        lists = []
        for file in list_files:
            path = "../" + dir_path + "/" + file
            list = pd.read_csv(filepath_or_buffer=path, usecols=self.cols, header=None)  # 将姓名和学校排名靠前
            lists.append(list)
        return lists

    def get_key_words(self):
        '''
        获取一连串的关键字表格
        :return:
        '''
        key_words_list = []
        for list in self.lists:
            list = list.values.tolist()
            for item in list:
                key_words_list.append(' '.join(item))
        return key_words_list

    def get_name_list(self, name_index=0):
        '''
        获取名单list 用于构造百科请求
        :return:
        '''
        name_lists = []
        for list in self.lists:
            list = list.values.tolist()
            for item in list:
                name_lists.append(item[name_index])
        return name_lists

    def get_work_unit_list(self, work_unit_index=1):
        '''
        获取工作单位名称
        :param work_unit_index:
        :return:
        '''
        work_unit_lists = []
        for list in self.lists:
            list = list.values.tolist()
            for item in list:
                work_unit_lists.append(item[work_unit_index])
        return work_unit_lists
