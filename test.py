import requests
from bs4 import BeautifulSoup


url='https://www.aladdin-e.com/zh_cn/catalogsearch/result/?q=79-10-7'
#url='https://www.aladdin-e.com/zh_cn/a103525.html'
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
}

SoupResponse = requests.get(url, headers=headers)
soup = BeautifulSoup(SoupResponse.content, 'lxml')


# 查找所有class属性为hd的div标签
div_list = soup.find_all('div', class_='pro-sku')
# 获取每个div中的a中的span（第一个），并获取其文本
for each in div_list:
    #print (each.a.string)
    print(each.a.get('href'))



