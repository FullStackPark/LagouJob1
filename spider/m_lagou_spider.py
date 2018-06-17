"""
a web spider for mobile lagou
多行注释，

很多很多行

"""

# 单行注释

# 指明编码方式

# -*- coding: utf-8 -*-
# !/usr/bin/env python

# 导入第三方库
import os
import sys
import time
import requests

sys.path.append('../') # 纯粹是为了下一行好用才加的这一句

from util.file_reader import parse_job_xml

# 将模块路径加到当前模块扫描的路径里
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))


from spider.jobdetail_spider import crawl_job_detail

import pandas as pd
from util import log
from config.config import *

# 以上，翻来覆去就是为了导入各种乱八七糟


try:
    # 导入parse模块并命名为parse
    from urllib import parse as parse
except:
    import urllib as parse
    sys.reload()
    sys.setdefaultencoding('utf-8')



# 从拉勾网爬取职位信息
def crawl_jobs(positionName):
    # 定义一个列表
    JOB_DATA = list()
    # 创建max_page_number对象，返回最大页数
    max_page_number = get_max_pageNo(positionName)
    log.info("%s, 共有 %s 页记录, 共约 %s 记录", positionName, max_page_number, max_page_number * 15)
    cookies = get_cookies()

    for i in range(1, max_page_number + 1):
        # url请求
        request_url = 'https://m.lagou.com/search.json?city=%E5%85%A8%E5%9B%BD&positionName=' + parse.quote(
            positionName) + '&pageNo=' + str(i) + '&pageSize=15'
        # 请求头部
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Host': 'm.lagou.com',
            'Referer': 'https://m.lagou.com/search.html',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, '
                          'like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'
        }
        # 发送请求
        response = requests.get(request_url, headers=headers, cookies=cookies)
        # 返回判断
        if response.status_code == 200:
            # 在JOB_DATA中添加positionId、positionName、createTime、salary、companyId、companyName、companyFullName
            for each_item in response.json()['content']['data']['page']['result']:
                JOB_DATA.append([each_item['positionId'], each_item['positionName'], each_item['city'],
                                 each_item['createTime'], each_item['salary'],
                                 each_item['companyId'], each_item['companyName'], each_item['companyFullName']])
                # try:
                    # crawl_job_detail(each_item['positionId'], positionName)
                # except:
                #     pass
            print('crawling page %d done...' % i)
            # 休眠
            time.sleep(TIME_SLEEP)
        elif response.status_code == 403:
            log.error('request is forbidden by the server...')
        else:
            log.error(response.status_code)

    return JOB_DATA

# 定义cookies,返回首次访问后的cookie
def get_cookies():
    headers = {
        'Host': 'm.lagou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
    }
    url = 'https://m.lagou.com/'
    response = requests.get(url, headers=headers, timeout=10)

    return response.cookies

# 返回某个工作的最大页数
def get_max_pageNo(positionName):
    # cookies为首次访问的cookies
    # cookie 不是WYY 说的甜点，是服务器去识别一个客户的基本的方法
    cookies = get_cookies()
    # url请求
    # %E5 这是个什么东东呢？
    # 确认过眼神，下面这个地址，确实可以访问
    # https://m.lagou.com/search.json?city=全国&positionName=机器学习&pageNo=1&pageSize=15
    request_url = 'https://m.lagou.com/search.json?city=%E5%85%A8%E5%9B%BD&positionName=' + parse.quote(
        positionName) + '&pageNo=1&pageSize=15'

    # 开始，伪装自己
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': 'm.lagou.com',
        'Referer': 'https://m.lagou.com/search.html',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) '
                      'Version/8.0 Mobile/12A4345d Safari/600.1.4',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive'
    }

    # 发送请求
    response = requests.get(request_url, headers=headers, cookies=cookies, timeout=10)
    
    # 上面代码执行结束之后，response-响应里面就包含了，我们需要的东西

    print("Getting data from %s successfully~" % positionName + request_url)
    

    if response.status_code == 200:
        max_page_no = int(int(response.json()['content']['data']['page']['totalCount']) / 15 + 1)
        return max_page_no

    elif response.status_code == 403:
        log.error('request is forbidden by the server...')
        return 0
    else:
        log.error(response.status_code)
        return 0

# 爬取职位信息，将内容保存在当前目录的data文件夹下
if __name__ == '__main__':
    # 读取这个文件，把定义好的要爬取的职位的信息加载进来
    craw_job_list = parse_job_xml('../config/job.xml')
    # 上一行代码执行结束之后，就会有8个职位在 craw_job_list
    
    # 挨个遍历

    for job in craw_job_list:
        # 创建joblist对象
        joblist = crawl_jobs(job)
        # 上一行的 joblist 里面就包含了所有页的所有的职位的信息






        col = [
            u'职位编码',
            u'职位名称',
            u'所在城市',
            u'发布日期',
            u'薪资待遇',
            u'公司编码',
            u'公司名称',
            u'公司全称']
        # 创建DataFrame对象，列名为col数组
        df = pd.DataFrame(joblist, columns=col)
        path = "./data/"
        # 文件保存路径
        # 
        df.to_excel(path + job + ".xlsx", sheet_name=job, index=False)
