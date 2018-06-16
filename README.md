##  [拉勾](http://www.lagou.com/)爬取


### 1. 项目介绍

爬取 [Lagou](www.lagou.com)工作数据,得到最新工作信息 


### 2. 安装支持

1. 安装第三方库

python3 -m pip install -r requirements.txt

### 3. 使用方法

运行spider下py文件，信息存储于Excel中.    ( cd ***/spider/)

1. 运行 m_lagou_spider.py文件，来获取工作数据并生成Excel文件
 
 - python3 m_lagou_spider.py

2. 运行lagou_company_spider.py文件，获取公司详细信息 (python3 lagou_company_spider.py)
3. 运行jobdetail_spider.py文件，获取职位详细信息 (python3 jobdetail_spider.py)

### 4. 成功原因
1. 手机的拉钩网站进行搜索爬虫（'https://m.lagou.com/search.json?city=……）
2. 控制爬取频率，速度相对较慢，爬取一条信息休眠2s
3. 爬取时更改UserAgent


