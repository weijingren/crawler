from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import datetime
from tinydb import TinyDB, Query
import urllib3
import xlsxwriter
import requests
#browser = webdriver.Chrome()
#browser = webdriver.Firefox()

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
}
url1='https://www.aladdin-e.com/zh_cn/catalogsearch/result/?q=12129-51-0'
#url2='https://www.aladdin-e.com/zh_cn/o104558.html'


SoupResponse = requests.get(url1, headers=headers)
soup = BeautifulSoup(SoupResponse.content, 'lxml')

#根据CAS号搜索产品后获取产品链接网址
result1 = soup.find_all("div",class_="pro-sku")
for each1 in result1:
    result2=each1.find_all("a",class_="product")
    print(result2[0].string)
    print(result2[0].get("href"))
    



