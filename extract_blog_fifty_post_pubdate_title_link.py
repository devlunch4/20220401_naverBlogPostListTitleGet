import datetime
import logging
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

########
# logging setting
# create logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s -%(filename)s:%(lineno)s - %(funcName)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# add file handler
now = datetime.datetime.now()
current_time = now.strftime('%Y-%m-%d_%H%M%S')

# logs folder check
log_dir = './logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

# set logging file_handler

file_handler = logging.FileHandler(f'./logs/{current_time}_doc_to_txt.log', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')
########


def xml_parser_get_title_list(input_account_name):
    logger.info('input_account_name:[' + input_account_name + ']')
    html = urlopen('https://rss.blog.naver.com/' + input_account_name + '.xml')
    bs = BeautifulSoup(html, "html.parser")

    res_title_list = bs.findAll('title')  # 블로그 포스트 제목 추출; blog title tag extract
    res_title_list.pop(0)  # 첫번째 블로그 제목 타이틀 제거; first title tag deleted
    res_title_list.pop(0)  # 두번째 블로그 제목 타이틀 제거; second title tag deleted
    print('len(res_title_list): ', len(res_title_list))
    return res_title_list


def xml_parser_get_pub_date_list(input_account_name):
    html = urlopen('https://rss.blog.naver.com/' + input_account_name + '.xml')
    bs = BeautifulSoup(html, "html.parser")
    res_pub_date_list = bs.findAll('pubdate')  # 블로그 포스트 작성일 추출; blog post pub date extract
    res_pub_date_list.pop(0)  # 현재시각 제거; now time deleted
    print('len(res_pub_date_list): ', len(res_pub_date_list))
    return res_pub_date_list


def xml_parser_get_guid_list(input_account_name):
    html = urlopen('https://rss.blog.naver.com/' + input_account_name + '.xml')
    bs = BeautifulSoup(html, "html.parser")
    res_guid_list = bs.findAll('guid')  # 블로그 포스트 링크 추출; blog post link extract
    print('len(res_guid_list): ', len(res_guid_list))
    return res_guid_list


def xml_parser_get_bs_all(input_account_name):
    html = urlopen('https://rss.blog.naver.com/' + input_account_name + '.xml')
    bs = BeautifulSoup(html, "html.parser")  # xml all extract
    return bs


def reset_pub_date(input_pub_date_type):  # Thu, 13 Jan 2022 23:41:00 +0900
    split_date = str(input_pub_date_type).split(' ')
    res_year = str(split_date[3])  # 년; year
    res_month = str(split_date[2])  # 월; month
    res_day = str(split_date[1])  # 일; day
    m_dic = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul ': '07',
             'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    for item in m_dic.items():  # 딕셔너리를 통한 숫자로 변경
        res_month = res_month.replace(item[0], item[1])

    res_date = res_year + '/' + res_month + '/' + res_day
    return res_date


def main(input_account_name):
    # print(xml_parser_get_bs_all(account_name))

    pub_date_list = xml_parser_get_pub_date_list(input_account_name)
    title_list = xml_parser_get_title_list(input_account_name)
    site_list = xml_parser_get_guid_list(input_account_name)

    #
    new_list = []
    if len(pub_date_list) == len(title_list) == len(site_list):
        for date, title, site in zip(pub_date_list, title_list, site_list):
            print(reset_pub_date(date.getText()) + '\t' + title.getText() + '\t' + site.getText())
            new_list.append(reset_pub_date(date.getText()) + '\t' + title.getText() + '\t' + site.getText())
            # print(reset_pub_date(date.getText()))
            # print(title.getText())
            # print(site.getText())

    print()
    new_list.reverse()
    print()
    for new_item in new_list:
        print(new_item)


if __name__ == '__main__':
    account_name = 'n_cloudplatform'
    main(account_name)
