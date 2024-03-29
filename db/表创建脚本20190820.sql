
USE Pdatabase2
GO
--任务批次表
--DROP TABLE dbo.CrawlerTaskBatch
CREATE TABLE dbo.CrawlerTaskBatch(
ID INT IDENTITY(1,1),   --自增ID
BatchName VARCHAR(100) NOT NULL,    --任务批次名称
BatchNote VARCHAR(300) NOT null,    --任务批次注释，用以说明该次抓取数据的原因
Epid VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,  --创建任务批次任务员工ID
BrandID VARCHAR(50) NOT NULL,   --抓取数据的品牌编号
URL VARCHAR(100) NOT NULL,  --抓取数据网站链接地址
CreateTime  DATETIME NOT NULL DEFAULT GETDATE() --任务批次创建时间
)

--任务批次明细表
--DROP TABLE dbo.CrawlerTaskBatchDetail
CREATE TABLE dbo.CrawlerTaskBatchDetail(
ID INT IDENTITY(1,1),   --自增ID
Crawler_Type INT NOT null,  --抓取目标数据类型,根据CAS号或产品编号抓取数据,1:CAS,2:产品编号
Crawler_Key VARCHAR(100) NOT NULL,  --抓取目标数据，一般为CAS号或产品编号
Mark INT NOT NULL DEFAULT 0,    --0:未执行抓取，1:成功执行抓取，2:抓取失败
BatchID INT NOT NULL ,--关连的批次任务ID,CrawlerTaskBatch表的ID字段
Epid VARCHAR(50) NOT NULL DEFAULT SYSTEM_USER,  --员工ID
CreateTime DATETIME NOT NULL DEFAULT GETDATE(), --创建时间，批次明细时间
UpdateTime DATETIME --批次明细处理时间，即修改mark字段的时间
)


----抓取数据结果表
--DROP TABLE dbo.CrawlerReault
CREATE TABLE dbo.CrawlerReault(
id INT IDENTITY(1,1),   --自增ID
BatchDid INT NOT NULL,   --任务批次明细ID,dbo.CrawlerTaskBatchDetail表的ID字段
BrandID VARCHAR(50) NOT NULL,   --抓取数据的品牌编号
CAS NVARCHAR(50) NOT NULL,    --CAS号
ProductNO VARCHAR(50) NOT NULL,  --产品编号
DescC NVARCHAR(200),    --中文名称
DescE NVARCHAR(200),    --英文名称
Purity NVARCHAR(100),   --纯度
Density NVARCHAR(100),  --密度
Pack NVARCHAR(100),     --包装
Price NVARCHAR(100),    --价格
MarketCode VARCHAR(20), --区或
CreateTime DATETIME     --创建时间
)


--最终呈现表
--产品表
--DROP TABLE dbo.CrawlerProduct
CREATE TABLE dbo.CrawlerProduct(
id int IDENTITY(1,1),   --自增ID
BrandID VARCHAR(50) NOT NULL,   --抓取数据的品牌编号
ProductNO VARCHAR(50) NOT NULL,  --产品编号
DescC NVARCHAR(200),    --中文名称
DescE NVARCHAR(200),    --英文名称
Purity NVARCHAR(100),   --纯度
Density NVARCHAR(100),  --密度
ResultID INT NOT NULL,  --关连数据结果ID,dbo.CrawlerReault表的ID字段
BatchID INT NOT NULL,   --关连的批次任务ID,CrawlerTaskBatch表的ID字段
CreateTime DATETIME     --创建时间
)

--包装价格表
--DROP TABLE dbo.CrawlerPack
CREATE TABLE dbo.CrawlerPack(
id int IDENTITY(1,1),   --自增ID
ProductNO VARCHAR(50) NOT NULL,  --产品编号
PackNr INT NOT NULL, --套
Quantity float NOT NULL, --规格数量
Unit NVARCHAR(20),      --包装单位
Price FLOAT NOT NULL,   --价格
MarketCode VARCHAR(20),  --区或
ResultID INT NOT NULL,  --关连数据结果ID,dbo.CrawlerReault表的ID字段
BatchID INT NOT NULL,   --关连的批次任务ID,CrawlerTaskBatch表的ID字段
CreateTime DATETIME     --创建时间
)




--用以查询品牌编号
SELECT * FROM zcl_mess.dbo.manufactory
WHERE code='R16'
--创建任务批次
--SELECT top 100 * FROM dbo.CrawlerTaskBatch
INSERT INTO dbo.CrawlerTaskBatch (BatchName,BatchNote,BrandID,URL)
VALUES('C_阿拉丁_20190820','阿拉丁价格数据抓取，目标为自有品牌所有CAS号', 'R16','https://www.aladdin-e.com/')

SELECT IDENT_CURRENT('CrawlerTaskBatch')


--创建任务批次明细
--SELECT TOP 100 * FROM dbo.CrawlerTaskBatchDetail

INSERT INTO dbo.CrawlerTaskBatchDetail(Crawler_Type,Crawler_Key,Mark,BatchID)
SELECT DISTINCT 1,REPLACE(CAS,' ',''),0,IDENT_CURRENT('CrawlerTaskBatch') FROM [211.5.7.250].OPDATA.dbo.PProducts
WHERE cas IS NOT NULL AND cas <> 'N/A'

SELECT top 10 a.id,a.Crawler_Key,b.BrandID
FROM    Pdatabase2.dbo.CrawlerTaskBatchDetail a
        INNER JOIN Pdatabase2.dbo.CrawlerTaskBatch b ON a.BatchID=b.ID
WHERE b.BatchName='C_阿拉丁_20190820' and a.mark=1


--保存抓取数据结果
INSERT INTO Pdatabase2.dbo.CrawlerReault(BatchDid,BrandID,CAS,ProductNO,DescC,DescE,Purity,Density,Pack,Price,MarketCode,CreateTime)
VALUES(   0,'',N'','',N'',N'',N'',N'',N'',N'','',GETDATE())

SELECT * FROM Pdatabase2.dbo.CrawlerReault


--向呈现表中插入最终数据