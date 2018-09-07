#-*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-09-05  10:06
"""
# chsErpUpdateData.py use
# class updateChsErpOrder()-----------------------------
selectSqlOrder = '''
                select 
                    a.INSIDERID,b.REALMONEY,b.RSAID,b.CREDATE,sum(c.COSTINGMONEY) as COSTINGMONEY
                from 
                    erp_member as a,erp_order as b,erp_order_detail as c
                where  
                    a.INSIDERID=b.INSIDERID and b.RSAID = c.RSAID 
                group by b.RSAID
                '''

insertSqlOrder = '''
                insert into 
                    chs_erp_order(INSIDERID,REALMONEY,RSAID,CREDATE,COSTINGMONEY)
                values(%s,%s,%s,%s,%s)  
                on duplicate key update
                    INSIDERID=values(INSIDERID),
                    REALMONEY=values(REALMONEY),
                    COSTINGMONEY=values(COSTINGMONEY),
                    RSAID=values(RSAID),
                    CREDATE=values(CREDATE)
                '''
# class updateChsErpAmountData() ------------------------------
selectSqlAmount = '''
                SELECT 
                    INSIDERID,sum(REALMONEY),sum(COSTINGMONEY),COUNT(INSIDERID),max(CREDATE),min(CREDATE),
                        (
                            SELECT 
                                COUNT(INSIDERID) as YEARFRE 
                            FROM 
                                chs_erp_order as c 
                            WHERE 
                                TIMESTAMPDIFF(DAY,c.CREDATE,NOW())<=365 AND c.INSIDERID = a.INSIDERID
                        ) as YEARFRE 
                FROM 
                    chs_erp_order as a 
                GROUP BY INSIDERID
                '''

insertSqlAmount = '''
                insert into 
                    chs_erp_amount_data(INSIDERID,SUMREALMONEY,SUMCOSTINGMONEY,FREQUENCY,MAXTIME,MINTIME,YEARFRE)
                values(%s,%s,%s,%s,%s,%s,%s)  
                on duplicate key update
                    INSIDERID=values(INSIDERID),
                    SUMREALMONEY=values(SUMREALMONEY),
                    SUMCOSTINGMONEY=values(SUMCOSTINGMONEY),
                    FREQUENCY=values(FREQUENCY),
                    MAXTIME=values(MAXTIME),
                    MINTIME=values(MINTIME),
                    YEARFRE=values(YEARFRE)
                '''
# class updateChsErpGoodsMember() ---------------------
# selectSqlMember = '''
#                 SELECT
#                     t1.INSIDERID,t1.RSAID,t1.RSADTLID,t1.GOODSID,t1.GOODSNAME,t1.GOODSQTY,t1.GOODSUNIT,c.FUNCTIONID,c.FUNCTION_1
#                 FROM
#                     chs_erp_goods_function_index AS c
#                 RIGHT JOIN
#                     (
#                         SELECT
#                             t.INSIDERID,b.RSAID, b.RSADTLID, b.GOODSID, b.GOODSNAME, b.GOODSQTY, b.GOODSUNIT
#                         FROM
#                             (SELECT INSIDERID ,RSAID ,CREDATE from chs_erp_order  where CREDATE>'%s')t
#                 LEFT JOIN
#                     erp_order_detail AS b
#                 ON t.RSAID= b.RSAID
#                     )t1
#                 ON t1.GOODSID = c.GOODSID
#                 '''
# insertSqlMember ='''
#                 INSERT INTO
#                     chs_erp_goods_member(INSIDERID, RSAID, RSADTLID, GOODSID, GOODSNAME, GOODSQTY, GOODSUNIT, FUNCTIONID, FUNCTION)
#                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
#                 on duplicate key update
#                     INSIDERID=values(INSIDERID),
#                     RSAID=values(RSAID),
#                     RSADTLID=values(RSADTLID),
#                     GOODSID=values(GOODSID),
#                     GOODSNAME=values(GOODSNAME),
#                     GOODSQTY=values(GOODSQTY),
#                     GOODSUNIT=values(GOODSUNIT),
#                     FUNCTIONID=values(FUNCTIONID),
#                     FUNCTION=values(FUNCTION)
#                 '''

selectSqlMember = '''
                SELECT 
                    t.INSIDERID,b.RSAID, b.RSADTLID, b.GOODSID, b.GOODSNAME, b.GOODSQTY, b.GOODSUNIT 
                FROM 
                    (SELECT INSIDERID ,RSAID ,CREDATE from chs_erp_order  where CREDATE>'%s')t
                LEFT JOIN 
                    erp_order_detail AS b 
                ON t.RSAID= b.RSAID
                '''
insertSqlMember ='''
                INSERT INTO 
                    chs_erp_goods_member(INSIDERID, RSAID, RSADTLID, GOODSID, GOODSNAME, GOODSQTY, GOODSUNIT)
                VALUES(%s,%s,%s,%s,%s,%s,%s)
                on duplicate key update
                    INSIDERID=values(INSIDERID),
                    RSAID=values(RSAID),
                    RSADTLID=values(RSADTLID),
                    GOODSID=values(GOODSID),
                    GOODSNAME=values(GOODSNAME),
                    GOODSQTY=values(GOODSQTY),
                    GOODSUNIT=values(GOODSUNIT)
                '''
updateUseClass='''
                UPDATE 
                    chs_erp_goods_member 
                SET 
                    USECLASSAGE = ( 
                        CASE 
                            WHEN GOODSNAME LIKE '%幼儿%' OR GOODSNAME LIKE '%小儿%' OR GOODSNAME LIKE '%儿童%' THEN 1
                            WHEN GOODSNAME LIKE '%老年%' OR GOODSNAME LIKE '%老人%' THEN 2
                            ELSE 0
                        END )
               '''
# class updateChsErpGoodsNum()--------------------

selectSqlNum = '''SELECT INSIDERID,count(INSIDERID) FROM chs_erp_goods_member GROUP BY INSIDERID'''
insertSqlNum ='''
                   insert into chs_erp_goods_num(INSIDERID,GOODSNUM)
                   values(%s,%s)
                   on duplicate key update
                   INSIDERID=values(INSIDERID),
                   GOODSNUM=values(GOODSNUM)
                   '''
# class updateChsErpGoodsClass()------------------
selectSqlClass = '''
                select 
                    t.INSIDERID,
                    t1.OTHER,
                    t2.CHILDREN,
                    t3.OLDMEN
                from
                    (select DISTINCT INSIDERID from chs_erp_goods_member)t
                LEFT JOIN
                    (SELECT INSIDERID ,case when count(USECLASSAGE)>0 then count(USECLASSAGE) else 0 end as OTHER from chs_erp_goods_member where USECLASSAGE=0 GROUP BY INSIDERID)t1
                ON 
                    t.INSIDERID=t1.INSIDERID
                LEFT JOIN 
                    (SELECT INSIDERID ,case when count(USECLASSAGE)>0 then count(USECLASSAGE) else 0 end  as CHILDREN from chs_erp_goods_member where USECLASSAGE=1 GROUP BY INSIDERID)t2
                ON 
                    t.INSIDERID = t2.INSIDERID
                LEFT JOIN
                    (SELECT INSIDERID ,case when count(USECLASSAGE)>0 then count(USECLASSAGE) else 0 end as OLDMEN from chs_erp_goods_member where USECLASSAGE=2 GROUP BY INSIDERID)t3
                ON 
                    t.INSIDERID = t3.INSIDERID
                '''
insertSqlClass = '''
                insert into 
                    chs_erp_goods_class(INSIDERID,OTHER,CHILDREN,OLDMEN)
                values(%s,%s,%s,%s)
                on duplicate key update
                    INSIDERID=values(INSIDERID),
                    OTHER=values(OTHER),
                    CHILDREN=values(CHILDREN),
                    OLDMEN=values(OLDMEN)
                '''
# -----------------------------------------------------------------
# class UpdateChsErpStore()
selectSqlStore = '''
                SELECT 
                    PLACEPOINTID,PLACEPOINTNAME,PLACEPOINTNO,ADDRESS 
                FROM 
                erp_placepoint
                '''
insertSqlStore = '''
                insert into 
                    chs_erp_store(PLACEPOINTID,PLACEPOINTNAME,PLACEPOINTNO,ADDRESS,STOREAMOUNT,PROFIT)
                values(%s,%s,%s,%s,%s,%s)
                on duplicate key update
                    PLACEPOINTID = values(PLACEPOINTID),
                    PLACEPOINTNAME = values(PLACEPOINTNAME),
                    PLACEPOINTNO = values(PLACEPOINTNO),
                    ADDRESS = values(ADDRESS),
                    STOREAMOUNT = values(STOREAMOUNT),
                    PROFIT = values(PROFIT)
                ;'''
selectSqlEvaluate = '''select * from chs_erp_evaluate'''
insertSqlEvaluate = '''
                    insert into
                        chs_erp_evaluate
                            (
                                INSIDERID,INSIDERCARDNO,INSIDERNAME,
                                IDCARD,MOBILE,SEX,MAILADDRESS,INSCARDTYPEID,
                                BIRTHDATE,NEWBIRTHDATE,CREDATE,LASTCONSUMDATE,
                                FREQUENCY,MEANDAY,INTEGRAL,ADDINTEGRAL,SUMREALMONEY,
                                SUMPROFIT,STOREAMOUNT,STOREPROFIT,AGE,LASTINTERVAL,
                                CREATINTERVAL,PLACEPOINTID,UNITPRICE,YEARFRE,
                                GOODSNUM,CLASSOTHER,CLASSCHILDREN,CLASSOLDMEN,
                                HISTORYSCORE,IDENTITYSCORE,COSTSCORE,BEHAVIORSCORE,MEMBERSCORE
                            )
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE
                        INSIDERID=values(INSIDERID),
                        INSIDERCARDNO=values(INSIDERCARDNO),
                        INSIDERNAME=values(INSIDERNAME),
                        IDCARD=values(IDCARD),
                        MOBILE=values(MOBILE),
                        SEX=values(SEX),
                        MAILADDRESS=values(MAILADDRESS),
                        INSCARDTYPEID=values(INSCARDTYPEID),
                        BIRTHDATE=values(BIRTHDATE),
                        NEWBIRTHDATE=values(NEWBIRTHDATE),
                        CREDATE=values(CREDATE),
                        LASTCONSUMDATE=values(LASTCONSUMDATE),
                        FREQUENCY=values(FREQUENCY),
                        MEANDAY=values(MEANDAY),
                        INTEGRAL=values(INTEGRAL),
                        ADDINTEGRAL=values(ADDINTEGRAL),
                        SUMREALMONEY=values(SUMREALMONEY),
                        SUMPROFIT=values(SUMPROFIT),
                        STOREAMOUNT=values(STOREAMOUNT),
                        STOREPROFIT=values(STOREPROFIT),
                        AGE=values(AGE),
                        LASTINTERVAL=values(LASTINTERVAL),
                        CREATINTERVAL=values(CREATINTERVAL),
                        PLACEPOINTID=values(PLACEPOINTID),
                        UNITPRICE=values(UNITPRICE),
                        YEARFRE=values(YEARFRE),
                        GOODSNUM=values(GOODSNUM),
                        CLASSOTHER=values(CLASSOTHER),
                        CLASSCHILDREN=values(CLASSCHILDREN),
                        CLASSOLDMEN=values(CLASSOLDMEN),
                        HISTORYSCORE=values(HISTORYSCORE),
                        IDENTITYSCORE=values(IDENTITYSCORE),
                        COSTSCORE=values(COSTSCORE),
                        BEHAVIORSCORE=values(BEHAVIORSCORE),
                        MEMBERSCORE=values(MEMBERSCORE)
                    '''
