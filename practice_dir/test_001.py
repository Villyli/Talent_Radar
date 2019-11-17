# 获取list

import os
import pandas as pd
import requests
from lxml import etree
import re


def get_lists(cols=[1, 6], dir_path="name_lists"):
    '''
    :param dims: 返回的读取csv中的列编号，默认为姓名、学校
    :return:
    '''
    # 构造文件名
    list_files = os.listdir("../" + dir_path)  # 返回文件名
    lists = []
    for file in list_files:
        # path = os.path.join(os.getcwd(), dir_path, file)
        # path = path.replace("\\\\", "/")
        path = "../" + dir_path + "/" + file
        list = pd.read_csv(filepath_or_buffer=path, usecols=cols, header=None)  # 将姓名和学校排名靠前
        lists.append(list)
    return lists


def build_baidu_request():
    lists = get_lists()
    user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    test_value = lists[0].values.tolist()[0]
    wd = ' '.join(test_value)
    test_response = requests.get('https://www.baidu.com/s',
                                 params={
                                     'wd': wd,
                                     'pn': 0  # pn:显示结果页数默认为0 其他每页递增rn 即：rn为20时第1页 pn=0 第2页 pn=20 第3页 pn=40
                                 },
                                 headers={
                                     'User-Agent': user_Agent
                                 })
    test_response_text = test_response.text
    # 去除<em>标签
    test_response_text = test_response_text.replace("<em>", "")
    test_response_text = test_response_text.replace("</em>", "")
    test_response_text = test_response_text.replace("\r", '')

    """
    使用正则表达式去除所有标签，获得纯文本
    https://blog.csdn.net/qq_42603652/article/details/81394872
    """
    # pattern = re.compile(r'\s|\n|<.*?>|[a-z]*|[A-Z]*|[0-9]*', re.S)  # 使re.S . 匹配包括换行在内的所有字符
    # test_response_text = test_response_text.decode('utf-8')

    '''
    直接找出所有中文来进行判断
    '''
    pattern = re.compile(r'([\u4e00-\u9fa5]+\s*[\u4e00-\u9fa5])+')
    test_response = re.findall(pattern, test_response_text)
    test_response_text = pattern.match(test_response_text)

    # 获取首页搜索结果的URLshow
    selector = etree.HTML(test_response_text)
    # TODO 有些学校邀请他做学术报告，那么官网上也有他的信息 解决策略--获取第一个edu的链接进入

    urlshows = selector.xpath(r"//*[@class='c-showurl']/text()")
    for url in urlshows:
        url = str(url)
        if re.match(r"(.*).edu.cn(.*)", url) != None:  # 构造的这是学校官网
            print(url)
    # 为什么构造的user_Agent没有传进去
    # TODO 获取百度百科的文本，同名怎么办？

    # TODO 正则表达式判断urlshow为edu的，从学校官网获取信息
    # TODO 获取新闻报道相关
    print(lists[0])
    """
    构造百度的请求
    :return:
    """


def get_chinese_segment(url):
    """
    获取页面的中文片段
    :param url:
    :return:
    """
    user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    response = requests.get(
        url,
        headers={
            'User-Agent': user_Agent
        }
    )
    response.encoding = ('utf-8')  # 解决乱码问题
    text = response.text

    pattern = re.compile(r'(>[\u4e00-\u9fa5]+\s*[\u4e00-\u9fa5])+<')
    text = re.findall(pattern, text)
    pass


def get_response_text(url):
    '''
    从链接返回html页面
    :param url:
    :return:
    '''
    user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    response = requests.get(
        url,
        headers={
            'User-Agent': user_Agent
        }
    )
    response.encoding = ('utf-8')  # 解决乱码问题
    text = response.text
    return text


def delete_tags_scripts(url):
    '''
    去除所有标签 是获取中文的另一种思路
    :param url:
    :return:
    '''
    text = get_response_text(url)
    # 先去除<script> </script>的内容\
    # TODO 某些脚本提取不出来
    # pattern = re.compile('<script.*?>.*</script>')只能提取表达式在尖括号内的脚本
    pattern = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')  # 完美去除所有脚本
    scripts = pattern.findall(text)
    text = pattern.sub('', text)
    # 去除<>标签
    pattern = re.compile(r'\s|\n|<.*?>', re.S)
    text = pattern.sub(' ', text)
    # 去除脚本中的注释 分为两种 // 和/* */
    # pattern = re.compile(r'(/\*)(.*)(\*/)')
    # zhushi_1 = pattern.findall(text)
    # pattern = re.compile('// *[\u4e00-\u9fa5a-zA-Z1-9]* ?')  # 正则表达式会编译空格
    # zhushi_2 = pattern.findall(text)

    # 去除多余的空格
    pattern = re.compile(r'\s+')  # 使用+号
    text = pattern.sub(' ', text)
    text = text.lstrip()
    return text
    pass


if __name__ == "__main__":
    get_lists()
    # build_baidu_request()
    # get_chinese_segment("http://maths.ccnu.edu.cn/info/1040/1485.htm")
    delete_tags_scripts("http://maths.ccnu.edu.cn/info/1040/1485.htm")
