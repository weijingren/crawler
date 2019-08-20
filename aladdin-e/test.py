import pymssql #引入pymssql模块
import conndb
import aladdin
    


#从数据库中轮询CAS号记录

connect = conndb.conn()

c0 = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
sql = " \
        SELECT top 10 a.id,a.Crawler_Key,b.BrandID \
        FROM    Pdatabase2.dbo.CrawlerTaskBatchDetail a \
                INNER JOIN Pdatabase2.dbo.CrawlerTaskBatch b ON a.BatchID=b.ID \
        WHERE b.BatchName='C_阿拉丁_20190820' and a.mark=0 \
        "
c0.execute(sql)   #执行sql语句
row = c0.fetchone()  #读取查询结果
while row:
    print ('开始抓取——》：',row[1])
    lst=aladdin.fn_aladdin(row[1])
    for x in lst:
        # print (x)
        print(x['cas'],'——》',x['productno'],'——》',x['pack'],'——》',x['price'])
        # 保存抓取数据
        connect1 = conndb.conn()
        c1=connect1.cursor()
        insertsql = "INSERT INTO Pdatabase2.dbo.CrawlerReault(BatchDid,BrandID,CAS,ProductNO,DescC,DescE,Purity,Density,Pack,Price,MarketCode) \
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        c1.execute(insertsql, (row[0],row[2],x['cas'],x['productno'],x['desc'],x['desc_e'],x['purity'],x['density'],x['pack'],x['price'],'CN'))
        connect1.commit()
        c1.close()
        connect1.close()
        print ('已保存抓取数据')
    #标记CAS已抓取
    connect2 = conndb.conn()
    c2=connect2.cursor()
    updatesql = "update Pdatabase2.dbo.CrawlerTaskBatchDetail set mark=1 where id='%s'"%row[0]
    c2.execute(updatesql)
    connect2.commit()
    c2.close()
    connect2.close()   

    # 轮询下一CAS
    row = c0.fetchone()
c0.close()   
connect.close()

