"""
实现爬虫的文件
"""
import requests
import re
from lxml import etree


class baidu_page_processor:
    """
    处理百度结果页的类
    """

    def __init__(self):
        pass

    def get_baidu_result_page(self, key_words: list):
        '''
        根据关键字构造百度搜索的结果
        :param key_words: 关键字
        :return: 百度搜索的页面
        '''
        user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
        wd = ''.join(key_words)
        response = requests.get('https://www.baidu.com/s',
                                params={
                                    'wd': wd,
                                    'pn': 0  # pn:显示结果页数默认为0 其他每页递增rn 即：rn为20时第1页 pn=0 第2页 pn=20 第3页 pn=40
                                },
                                headers={
                                    'User-Agent': user_Agent
                                })
        html_text = response.text
        return html_text

    def get_baidu_baike_result(self, keyword: str, attribute: str):
        """
        构造百度百科的请求，返回百度百科多义词项网页
        :param name:姓名
        :param attribute: 单位之类的关键词
        :return:
        """
        user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
        response = requests.get('https://baike.baidu.com/item/' + keyword,
                                params={
                                    'force': '1'
                                },
                                headers={
                                    'User-Agent': user_Agent
                                })
        html_text = response.text
        uniform_html_processor.get_html_encoding(html_text)
        response.encoding = (uniform_html_processor.get_html_encoding(html_text))
        html_text = response.text
        return html_text

    def whether_baike_polysemant(self, html: str):
        '''
        判断百科页面是否有多义词
        :return: 是否有多义词
        '''
        selector = etree.HTML(html)
        if len(selector.xpath("//*[@class='lemmaWgt-subLemmaListTitle']/text()")) == 0:  # 如果没有多义词
            return False
        else:
            return True

    def polysemant_page_select(self, html: str, unit: str):
        """
        根据单位名字-筛选百度百科链接
        匹配算法：暂时定为包含关机字
        :return:
        """
        selector = etree.HTML(html)
        polysement_lists = selector.xpath('//*[@class="para"]//a/text()')
        url_lists = selector.xpath('//*[@class="para"]//a/@href')
        data_lemmaid_lists = selector.xpath('//*[@class="para"]//a/@data-lemmaid')
        url = ''
        # 寻找匹配的人物
        i = 0
        for item in polysement_lists:
            item_str = str(item)
            if re.search(unit, item_str) != None:  # 如果匹配成功
                url = "https://baike.baidu.com" + str(url_lists[i])
                break
            i += 1
        return url

    def get_unit_offcial_site_page(self, page: str):
        """
        在结果页中获取工作单位官网页，包含查询人的信息
        策略为：搜索结果第1项,且不是百度百科,如果是百度百科，那么重新搜索
        :return:
        """
        selector = etree.HTML(page)
        # 抽取搜索结果第1项
        target_divs = selector.xpath('//div[@class="result c-container "]')
        for i in range(len(target_divs)):
            sorce_url = selector.xpath('//*[@class="c-showurl"]/text()')[i]
            if re.search("baike.baidu.com", sorce_url) == None:  # 不是百科
                break
        index = i + 1
        target_urls = selector.xpath('//div[@class="result c-container "]//a/@href')
        url = target_urls[0]
        return url


class uniform_html_processor:
    '''
    定义网页处理的静态类 https://jingyan.baidu.com/article/c45ad29c6b9eda051753e294.html
    '''

    @staticmethod
    def get_html_by_url(url: str):
        '''
        通过url请求返回网页
        :param url:
        :return:
        '''
        user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
        response = requests.get(url,
                                headers={
                                    'User-Agent': user_Agent
                                })
        response.encoding = 'utf-8'
        return response.text

    @staticmethod
    def get_html_encoding(html: str):
        """
        获取网页编码方式
        :param html:
        :return:
        """
        selector = etree.HTML(html)
        attribValues = selector.xpath('//meta/@*')
        encodingValue = ''  # 编码取值
        pattern = re.compile('(utf-8)|gb2312|gbk', re.I)
        for item in attribValues:
            string = str(item)
            result = pattern.search(string)
            if (result == None):
                continue
            else:
                encodingValue = result.group()
        return encodingValue
