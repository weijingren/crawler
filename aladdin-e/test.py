from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup #静态网页解析库
import requests


# 定义存储抓取信息的列表，其中列表中均为字典类型
data_info_list=[]
#根据CAS值到指定网站搜索数据

cas="7631-86-9"
#cas="22519-64-8"
# CAS搜索链接地址
cas0=cas #保存CAS号
casurl="https://www.aladdin-e.com/zh_cn/catalogsearch/result/?q="+cas


#伪装头部信息
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
}

#打开链接地址获取网页内容
SoupResponse = requests.get(casurl, headers=headers)
soup = BeautifulSoup(SoupResponse.content, 'lxml')

#根据CAS号搜索产品后获取产品链接网址
#通过beautifulsoup库定位搜索产品的链接地址


url_list=[casurl]

if soup.find("ul",class_="items pages-items"):
    result1=soup.find("ul",class_="items pages-items").find_all("a",class_="page")
    # print (type(result1))
    for each1 in result1:
        url_list.append(each1.get("href"))

for x in url_list:
    print(x)

for x_url in url_list:
    #打开链接地址获取网页内容
    SoupResponse = requests.get(x_url, headers=headers)
    soup = BeautifulSoup(SoupResponse.content, 'lxml')


    #根据CAS号搜索产品后获取产品链接网址
    #通过beautifulsoup库定位搜索产品的链接地址


    result1 = soup.find_all("div",class_="pro-sku")
    for each1 in result1:
        result2=each1.find_all("a",class_="product")
        # 获取产品编号
        productno=result2[0].string
        # 获取产品链接
        producturl=result2[0].get("href")
        print (producturl)
        

