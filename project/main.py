import crawler
import file_tools
import requests
from lxml import etree
from text_info_mining import text_processor
from crawler import uniform_html_processor

list_processer = file_tools.lists_processer()
baidu_page_processor = crawler.baidu_page_processor()  # 每次处理单页面


def main():
    key_words_list = list_processer.get_key_words()
    name_lists = list_processer.get_name_list()
    attrib_lists = list_processer.get_work_unit_list()
    name_attrib_dict = dict(zip(name_lists, attrib_lists))
    # official_site_info(key_words_list)
    baike_site_info(name_attrib_dict)


def official_site_info(key_words_list):
    for key_words in key_words_list:
        # 抓取百度搜索界面
        html_text = baidu_page_processor.get_baidu_result_page(key_words)
        # TODO 302 not found 如果是百度百科 那么会导致网页重定向
        # TODO 筛选可靠的链接
        # 学校官网 第一个包含edu的网站？ 研究所呢
        offical_page_url = baidu_page_processor.get_unit_offcial_site_page(html_text)
        response = requests.get(offical_page_url)
        encodingValue = uniform_html_processor.get_html_encoding(response.text)
        response.encoding = (encodingValue)  # 判断网页编码 gb2312 gbk
        offical_page = response.text
        offical_page_info = text_processor.get_clean_info(offical_page)
        pass


# TODO 百科页面结果
def baike_site_info(name_attrib_dict):
    for name, attrib in name_attrib_dict.items():
        # 获取百度百科多义词界面
        baike_page = ''
        count = 0
        html_text = baidu_page_processor.get_baidu_baike_result(keyword=name, attribute='')
        if baidu_page_processor.whether_baike_polysemant(html_text) == False:
            baike_page = html_text
        else:  # 如果是多义词，则根据属性值筛选
            url = baidu_page_processor.polysemant_page_select(html_text, str(attrib))
            if (url == ''):
                print(name + attrib)
                baike_page = '未找到符合条件的百科人物'
                count += 1
            else:
                baike_page = uniform_html_processor.get_html_by_url(url)
            # <div class="polysemantList-header-title">
        baike_page_clean_info = text_processor.get_clean_info(baike_page)
        pass
    print(count)


if __name__ == '__main__':
    main()
