from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#browser = webdriver.Chrome()
browser = webdriver.Firefox()
url='https://www.aladdin-e.com/zh_cn/o104558.html'
#url='https://www.cnblogs.com/zhaof/p/6953241.html'

browser.get(url)

#lis= browser.find_elements(By.CLASS_NAME,'s-price price')

lis1 = browser.find_element_by_tag_name('table')

#产品信息表头
print(lis1.find_element_by_tag_name('thead').text)

#产品包装信息
lis2 = lis1.find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')
#for lis3 in lis2:
#print(len(lis2))
#print(lis2[0].text)

i=lis2[0].find_elements_by_tag_name('td')[0].text+'\t'+\
    lis2[0].find_elements_by_tag_name('td')[1].text+'\t'+\
    lis2[0].find_elements_by_tag_name('td')[2].text+'\t'+\
    lis2[0].find_elements_by_tag_name('td')[3].text+'\t'
print(i.replace("\n",""))
#print(lis2[1].find_elements_by_tag_name('td')[0].text)
#print(lis2[2].find_elements_by_tag_name('td')[0].text)


    #print(len(lis3))
    #lis4=lis3.find_elements_by_tag_name('td')
    #print(type(lis4))
    #print(lis4[0].text)

    #for lis5 in lis4:
        #print(lis5.find_element_by_class_name('col').text)
    #print(lis3.find_element_by_class_name('ajaxUpdatePrice_27930').text)
    #print(lis3.find_element_by_class_name('col qty').text)
    

browser.close()
