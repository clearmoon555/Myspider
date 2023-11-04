#打包文件
#!pip install pyinstaller
#!pyinstaller --onefile your_script.py



import requests
import logging
import re
from urllib.parse import urljoin
import json
from os import makedirs
from os.path import exists
import multiprocessing



'''
level=logging.INFO：这将日志级别设置为INFO
这意味着具有INFO级别或更高级别（例如，WARNING、ERROR、CRITICAL）的消息将被记录下来
具有较低级别（例如DEBUG）的消息将不会被记录
%(asctime)s：将被替换为日志消息创建的时间，以人类可读的格式显示
%(levelname)s：将被替换为消息的日志级别（例如，INFO、WARNING、ERROR）
%(message)s：将被替换为实际的日志消息。
'''
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
#设置要爬取的url以及爬取的页数
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10



'''
定义一个较通用的爬取页面的方法，叫做 scrape_page
它接收一个 url 参数，返回页面的 html 代码
这里首先判断了状态码是不是 200，如果是，则直接返回页面的 HTML 代码
如果不是，则会输出错误日志信息
'''
def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)



'''
接收一个 page 参数，即列表页的页码
我们在方法里面实现列表页的 URL 拼接
然后调用 scrape_page 方法爬取
'''
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)



'''
通过正则表达式匹配需要的url的一部分
储存在列表中
用urljoin方法连接成完整url
'''
def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern, html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url 
#return 用于从函数中返回一个值并结束函数，而 yield 用于创建生成器函数，允许逐个生成值而保持函数状态



def scrape_detail(url):
    return scrape_page(url)



'''
parse_detail 方法用于解析详情页，它接收一个参数为 html，解析其中的内容，并以字典的形式返回结果
'''
def parse_detail(html):
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)
    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(1) if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()) if re.search(score_pattern, html) else None
    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }



RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)
#使用 exists 函数检查 RESULTS_DIR 目录是否已经存在。如果目录不存在，它使用 makedirs 函数创建该目录



'''
用json文件格式存储数据
'''
def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
#ensure_ascii 设置为 False，可以保证的中文字符在文件中能以正常的中文文本呈现
#indent 为 2，则是设置了 JSON 数据的结果有两行缩进



def main(page):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        logging.info('saving data to json data')
        save_data(data)
        logging.info('data saved successfully')



if __name__ == '__main__':
    pool = multiprocessing.Pool()
    #多进程加速
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()
    pool.join()
