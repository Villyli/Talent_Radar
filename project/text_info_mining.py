"""
文本信息提取相关类
"""

import re


class text_processor():

    # TODO 清除列表中的信息 如张希 中国科学技术大学
    @staticmethod
    def get_clean_info(html_text: str):
        """
        去除页面中的脚本
        去除标签
        去除多余空白字符\s
        :param html_text:
        :return:
        """
        # 完美去除所有脚本
        pattern = re.compile(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>')
        scripts = pattern.findall(html_text)
        text = pattern.sub('', html_text)
        # 去除<option></option>的内容
        pattern = re.compile(r'<option\b[^<]*(?:(?!<\/option>)<[^<]*)*<\/option>')
        text = pattern.sub('', text)
        # 去除<style></style>内容
        pattern = re.compile(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>')
        text = pattern.sub('', text)
        # 去除<style></style>内容
        # 去除<>标签
        pattern = re.compile(r'\s|\n|<.*?>', re.S)
        text = pattern.sub(' ', text)
        # 去除多余的空格
        pattern = re.compile(r'\s+')  # 使用+号
        text = pattern.sub(' ', text)
        text = text.lstrip()
        return text

    # TODO 可能是学校的百度百科 考虑用bert辨别人的名字和学校
    def get_BaiDuBaiKe_url(self, text: str):
        '''
        获取搜索结果中的百度百科页面信息
        :param text:
        :return:
        '''
