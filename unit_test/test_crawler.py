import project.crawler as crawler
import requests
from project.crawler import uniform_html_processor
from lxml import etree
import re


class Test_baidu_page_processor:

    def test_get_unit_offcial_site_page(self):
        baidu_processor = crawler.baidu_page_processor()
        html = baidu_processor.get_baidu_result_page(['周远扬', '华中师范大学'])
        url = baidu_processor.get_unit_offcial_site_page(html)
        assert type(url) is str

    def test_get_baidi_baike_result(self):
        baidu_processor = crawler.baidu_page_processor()
        html = baidu_processor.get_baidu_baike_result(keyword='周远扬', attribute='')
        assert 1 == 1
        pass

    def test_polysement_page_select(self):
        '''
        测试多义词选择
        :return:
        '''
        baidu_processor = crawler.baidu_page_processor()
        html = baidu_processor.get_baidu_baike_result(keyword='张文明', attribute='')
        url = baidu_processor.polysemant_page_select(html, unit="上海交通大学")
        text = uniform_html_processor.get_html_by_url(url)
        assert 1 == 1
        pass


class Test_uniform_html_processor:

    def test_get_pages_by_urls(self):
        response = requests.get(
            "http://www.baidu.com/link?url=UtgVceQJJeRehgdFGdBfzaS1ebvX9TFAsp-SJFUM7c2U8bK8jT8B_5hImO5KRocLogUZ5niMlT41rCk4YVSEf_")
        # response = requests.get("http://www.baidu.com/link?"
        #                         "url=vTKFrgM-K_KQtUhcxEHwSgs5mNlIFQyXhb0S3lECSpF0kKtaVwLvKVpMSj_OWZ2xfH9bSdkywURSwoE2bOyo5a")
        selector = etree.HTML(response.text)
        attribValues = selector.xpath('//meta/@*')
        encodingValue = ''  # 编码取值
        pattern = re.compile('(utf-8)|gb2312|gbk', re.I)
        for item in attribValues:
            string = str(item)
            result = pattern.search(string)
            if (result == None):
                continue
            else:
                attribValues = result.group()
            pass

        encodingType = ['utf-8', 'gb2312', 'gbk']  # 字符编码
        response.encoding = ('utf-8')
        assert type(response.text) is str
        pass
