from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup #静态网页解析库
import requests



def fn_aladdin( cas ):

    # 定义存储抓取信息的列表，其中列表中均为字典类型
    data_info_list=[]
    #根据CAS值到指定网站搜索数据

    # cas="10025-82-8"
    # CAS搜索链接地址
    casurl="https://www.aladdin-e.com/zh_cn/catalogsearch/result/?q="+cas


    #伪装头部信息
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
    }

    #打开链接地址获取网页内容
    SoupResponse = requests.get(casurl, headers=headers)
    soup = BeautifulSoup(SoupResponse.content, 'lxml')


    #对于有翻页的信息，存入翻页链接
    url_list=[casurl]
    if soup.find("ul",class_="items pages-items"):
        result1=soup.find("ul",class_="items pages-items").find_all("a",class_="page")

        for each1 in result1:
            url_list.append(each1.get("href"))

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

            print (productno,producturl)
            #设置打开浏览器，Chrome、Firefox二选一即可
            #browser = webdriver.Chrome()
            browser = webdriver.Firefox()
            browser.get(producturl)

            # 获取包装价格信息
            #产品名称
            
            if browser.title == '404 网页发生错误':
                browser.close()
                continue
            # 中文名称
            desc=browser.find_element_by_class_name('base').text
            # 英文名称
            desc_e=browser.find_element_by_class_name('product-name2-regent').text
            #产品编号
            productno=browser.find_element_by_class_name('product-info').text.split('|')[0].replace('产品编号 ','')
            #产品CAS
            #cas=browser.find_element_by_class_name('product-info').text.split('|')[1]
            #产品品牌
            brand=browser.find_element_by_class_name('product-info').text.split('|')[2]
            #纯度
            purity=browser.find_element_by_class_name('product-package').text
            
            #密度
            product_attribute1=browser.find_element_by_id('product-attribute-specs-table').find_element_by_tag_name('tbody')

            density='null'
            if len(product_attribute1.find_elements_by_tag_name('tr')) > 0:
                i=0
                j=len(product_attribute1.find_elements_by_tag_name('tr'))
                while i < j:
                    if product_attribute1.find_elements_by_tag_name('tr')[i].find_elements_by_tag_name('td')[0].text == '密度':
                        density=product_attribute1.find_elements_by_tag_name('tr')[i].find_elements_by_tag_name('td')[1].text
                        i=j
                    i+=1
                    
            else:
                density='null'


            #产品-包装信息
            lis1 = browser.find_element_by_tag_name('table')
            lis2 = lis1.find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')
            unable1=lis2[0].text
            unable2='该产品暂无可销售选项。'
            # 产品无包装
            if unable1 != unable2:
                i=0
                j=len(lis2)
                while i < j:
                    #货号/包装
                    pack = lis2[i].find_elements_by_tag_name('td')[0].text
                    #库存
                    qty = lis2[i].find_elements_by_tag_name('td')[1].text.replace("\n","")
                    #价格有原价与现价之分   
                    #原价
                    oprice=''
                    #现价
                    sprice=''

                    lis3=lis2[i].find_elements_by_tag_name('td')[2].find_elements_by_tag_name('p')
                    #print(len(lis3))
                    
                    n=len(lis3)
                    if n == 2:
                        oprice=lis3[0].text
                        sprice=lis3[1].text
                    elif n == 1:
                        oprice=lis3[0].text
                        sprice='现价:'
                    oprice=oprice.replace('原价: ','').replace('￥ ','').replace(',','')
                    # 定义字典来存储抓取的信息
                    # CAS号，产品编号，纯度，密度，英文名称，中文名称，包装，价格
                    data_info={'cas':cas,'productno':productno,'purity':purity,'density':density,'desc_e':desc_e,'desc':desc,'pack':pack,'price':oprice}

                    # 保存包装信息
                    data_info_list.append(data_info)
                    i+=1
            browser.close()
    return data_info_list



     
if __name__ == '__main__':
    aladdin = fn_aladdin
