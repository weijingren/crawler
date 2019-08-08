
import pymssql #引入pymssql模块
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup #静态网页解析库
import requests
import conndb

#从数据库中轮询CAS号记录
# connect = pymssql.connect(server='211.5.9.240', user='temp', password='1qaz2WSX3edc',database='Pdatabase2') #服务器名,账户,密码,数据库名
# connect1 = pymssql.connect(server='211.5.9.240', user='temp', password='1qaz2WSX3edc',database='Pdatabase2') #服务器名,账户,密码,数据库名
# connect2 = pymssql.connect(server='211.5.9.240', user='temp', password='1qaz2WSX3edc',database='Pdatabase2') #服务器名,账户,密码,数据库名

connect = conndb.conn()

c0 = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
sql = "SELECT top 1 cas FROM Pdatabase2.dbo.阿拉丁CAS号20190801  "
c0.execute(sql)   #执行sql语句
row = c0.fetchone()  #读取查询结果
while row:              #循环读取所有结果

    # CAS搜索链接地址
    print(row[0])
    cas0=row[0] #保存CAS号
    casurl="https://www.aladdin-e.com/zh_cn/catalogsearch/result/?q="+row[0]
    #print(casurl)   #输出结果
    #伪装头部信息
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
    }

    SoupResponse = requests.get(casurl, headers=headers)
    soup = BeautifulSoup(SoupResponse.content, 'lxml')

    #根据CAS号搜索产品后获取产品链接网址
    # 通过beautifulsoup库定位搜索产品的链接地址
    result1 = soup.find_all("div",class_="pro-sku")
    for each1 in result1:
        result2=each1.find_all("a",class_="product")
        # 保存产品编号
        productno=result2[0].string
        producturl=result2[0].get("href")
        #输出CAS与产品链接信息
        # print(cas+"-->>"+casurl+"\t"+productno+"-->>"+producturl)

        #设置打开浏览器
        #browser = webdriver.Chrome()
        browser = webdriver.Firefox()

        browser.get(producturl)
        # if browser.find_element_by_class_name('page-head-alt'):
        #     pname=browser.find_element_by_class_name('page-head-alt')
        #     fail404=pname.find_element_by_tag_name('strong').text
        #     if fail404 == '404错误':
        #         browser.close()
        #         continue


        # 获取包装价格信息
        #产品信息
        #print(browser.find_element_by_class_name('product-info').text)
        #产品名称
        
        if browser.title == '404 网页发生错误':
            browser.close()
            continue
        pname=browser.find_element_by_class_name('product-info').text.split('|')[0]
        #产品CAS
        cas=browser.find_element_by_class_name('product-info').text.split('|')[1]
        #产品品牌
        brand=browser.find_element_by_class_name('product-info').text.split('|')[2]
        #纯度信息
        purity=browser.find_element_by_class_name('product-package').text
        
        #密度信息
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
                # 输出包装信息
                print(pname+'-->'+cas+'-->'+brand+'-->'+purity+'-->'+density+'-->'+pack+'-->'+oprice+'-->'+sprice)
                i+=1

                
                # 保存抓取数据
                connect1 = conndb.conn()
                c1=connect1.cursor()
                insertsql = "INSERT INTO dbo.spiderdata(MoriginalID,CAS,Brand,Purity,pack,Oprice,Sprice,density) \
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                c1.execute(insertsql, (pname,cas0,brand,purity,pack,oprice,sprice,density))
                connect1.commit()
                c1.close()
                connect1.close()
    
        browser.close()



            
    #标记CAS已抓取
    connect2 = conndb.conn()
    c2=connect2.cursor()
    updatesql = "update Pdatabase2.dbo.阿拉丁CAS号20190801 set mark=1 where cas='%s'"%row[0]
    c2.execute(updatesql)
    connect2.commit()
    c2.close()
    connect2.close()   
    #轮询CAS号

    row = c0.fetchone()

c0.close()   
connect.close()
