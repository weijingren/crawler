from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# browser = webdriver.Chrome()
browser = webdriver.Firefox()
#url1='https://www.cnblogs.com/zhaof/p/6953241.html'
# url2='https://www.aladdin-e.com/zh_cn/e298823.html'
url2='https://www.aladdin-e.com/zh_cn/f109226.html'

#browser.get(url1)



browser.get(url2)

#lis= browser.find_elements(By.CLASS_NAME,'s-price price')
#产品信息表头
#print(lis1.find_element_by_tag_name('thead').text)

#产品信息
#print(browser.find_element_by_class_name('product-info').text)
pname=browser.find_element_by_class_name('product-info').text.split('|')[0]
cas=browser.find_element_by_class_name('product-info').text.split('|')[1]
brand=browser.find_element_by_class_name('product-info').text.split('|')[2]

purity=browser.find_element_by_class_name('product-package').text

        
#密度信息
#密度信息
product_attribute1=browser.find_element_by_id('product-attribute-specs-table').find_element_by_tag_name('tbody')

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
#print(len(lis2))
# print(lis2[0].text)
unable1=lis2[0].text
unable2='该产品暂无可销售选项。'

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


browser.close()
