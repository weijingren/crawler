#引入pymssql模块
import pymssql


connect = pymssql.connect(server='211.5.9.240', user='temp', password='1qaz2WSX3edc',database='Pdatabase2') #服务器名,账户,密码,数据库名
if connect:
    print("连接成功!")

cursor = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
sql = "SELECT CAS号 FROM Pdatabase2.dbo.CAS20190719"
cursor.execute(sql)   #执行sql语句
row = cursor.fetchone()  #读取查询结果,
while row:              #循环读取所有结果
    link="https://www.aladdin-e.com/zh_cn/catalogsearch/result/?q="+row[0]
    print(link)   #输出结果

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
}
url1='https://www.aladdin-e.com/zh_cn/catalogsearch/result/?q=79-37-8'
#url2='https://www.aladdin-e.com/zh_cn/o104558.html'


SoupResponse = requests.get(url1, headers=headers)
soup = BeautifulSoup(SoupResponse.content, 'lxml')

#根据CAS号搜索产品后获取产品链接网址
result1 = soup.find_all("div",class_="pro-sku")
for each1 in result1:
    result2=each1.find_all("a",class_="product")
    print(result2[0].string)
    print(result2[0].get("href"))
     
 
 
    row = cursor.fetchone()

cursor.close()   
connect.close()