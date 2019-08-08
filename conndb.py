import pymssql #引入pymssql模块
     
def conn():
    connect = pymssql.connect(server='211.5.9.240', user='temp', password='1qaz2WSX3edc',database='Pdatabase2') #服务器名,账户,密码,数据库名
    # if connect:
    #     print("连接成功!")
    return connect
     
if __name__ == '__main__':
    conn = conn()

