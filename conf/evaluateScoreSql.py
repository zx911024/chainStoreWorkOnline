#-*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-09-05  09:17
"""
# =======================================================
# evaluateScore.py USE
# expain:updateSql
# identitySql,buyHistorySql,costScoreSql,bheaviorScoreSql
# 更新身份特性分数150
identitySql = '''
              UPDATE 
                chs_erp_evaluate 
              SET 
                IDENTITYSCORE=
                # 有无身份证25分
                (
                    CASE 
                        WHEN IDCARD is not null THEN 25
                        ELSE 7
                    END
                )+
                # 有无手机号码50分
                # -------------
                (
                    CASE 
                        WHEN MOBILE is not null THEN 25
                        ELSE 8
                    END
                )+
                # 有无性别数据50分
                (
                    CASE 
                        WHEN SEX != Null THEN 25
                        ELSE 8
                    END
                )+
                # 有无地址50分
                (
                    CASE 
                        WHEN MAILADDRESS != Null THEN 25
                        ELSE 7
                    END
                )+
                # 卡类型25分
                (
                    CASE 
                        WHEN INSCARDTYPEID!=1 THEN (17/171)*INSCARDTYPEID+8
                        ELSE 8
                    END
                ) + 
                # 年龄25分
                (
                    CASE 
                        WHEN age>100 THEN 0
                        WHEN age<=10 THEN 0
                        WHEN age<=100 AND age>80 THEN (8)
                        WHEN age<=80 AND age>60 THEN (15)
                        WHEN age<=60 AND age>40 THEN (20)
                        WHEN age<=40 AND age>25 THEN (25)
                        WHEN age<=25 AND age>10 THEN (8)
                        ELSE 7
                    END
                );
              '''
# 更新购药历史分数500
buyHistorySql = '''
            UPDATE 
                chs_erp_evaluate 
            SET 
                HISTORYSCORE=
                #办卡间隔时间25分
                (
                    CASE 
                        WHEN CREATINTERVAL>7000 THEN 0
                        WHEN CREATINTERVAL<0 THEN 0
                        WHEN CREATINTERVAL<=7000 AND CREATINTERVAL>0 THEN 
                            (
                                15/(SELECT a.MAXFQ FROM((SELECT MAX(CREATINTERVAL)AS MAXFQ FROM chs_erp_evaluate where CREATINTERVAL<=7000)a))*CREATINTERVAL+10
                            )
                        ELSE 5
                    END
                )+
                #购药次数65分
                (
                    CASE 
                        WHEN FREQUENCY=0 THEN 0
                        WHEN FREQUENCY>0 THEN 
                            (
                                35/(SELECT a.MAXFQ FROM((SELECT MAX(FREQUENCY)AS MAXFQ FROM chs_erp_evaluate)a))*FREQUENCY+30
                            )
                        ELSE 10
                    END
                )+
                #平均间隔天数55分
                (
                    CASE
                        WHEN MEANDAY<5 OR MEANDAY>365 THEN 5
                        WHEN MEANDAY>=5 AND MEANDAY<=365 THEN
                            (
                                (30/(SELECT (1/a.MAXMD) FROM((SELECT MIN(MEANDAY) AS MAXMD FROM chs_erp_evaluate WHERE MEANDAY>=5 AND MEANDAY<365)a)))*(1/MEANDAY)+25
                            )
                        ELSE 5
                    END
                )+
                # 会员当前积分40分
                (
                    CASE
                        WHEN INTEGRAL>=0 THEN 
                            (
                                25/(SELECT a.MAXINT FROM((SELECT MAX(INTEGRAL) AS MAXINT FROM chs_erp_evaluate)a))*INTEGRAL +15
                            )
                        ELSE 10
                    END
                )+
                # 会员累积积分25分
                (
                    CASE
                        WHEN ADDINTEGRAL >=100000  THEN 25
                        WHEN ADDINTEGRAL>=0 AND ADDINTEGRAL<100000 THEN 
                            (
                                17/(SELECT a.MAXADDINT FROM((SELECT MAX(ADDINTEGRAL) AS MAXADDINT FROM chs_erp_evaluate WHERE ADDINTEGRAL<=100000)a))*ADDINTEGRAL +8
                            )
                        ELSE 8
                    END
                )+
                # 最后一次消费时间与当前时间的间隔100分
                (
                    CASE
                        WHEN LASTINTERVAL=0 THEN 100 
                        WHEN LASTINTERVAL>=365 THEN 5
                        WHEN LASTINTERVAL>0 AND LASTINTERVAL<365 THEN 
                            (
                                (60/(SELECT (1/a.MAXLAST) FROM((SELECT MIN(LASTINTERVAL) AS MAXLAST FROM chs_erp_evaluate where LASTINTERVAL>0 AND LASTINTERVAL<365)a)))*(1/LASTINTERVAL)+40
                            )
                        ELSE 5
                    END
                )+
                # 客单价90分
                (
                    CASE
                        WHEN UNITPRICE>=10000 THEN 90
                        WHEN UNITPRICE<=0 THEN 0
                        WHEN UNITPRICE>0 and UNITPRICE<=10000 THEN
                            (
                                55/(SELECT a.MAXLAST FROM((SELECT MAX(UNITPRICE) AS MAXLAST FROM chs_erp_evaluate where UNITPRICE>0 and UNITPRICE<=10000)a))*UNITPRICE+35
                            )
                        ELSE 35
                    END
                )+
                # 年购药次数100分
                (
                    CASE
                        WHEN YEARFRE>=0 THEN 
                            (
                                65/(SELECT a.MAXLAST FROM((SELECT MAX(YEARFRE) AS MAXLAST FROM chs_erp_evaluate)a))*YEARFRE+35
                            )
                        ELSE 30
                    END
                )
                '''
# -- 贡献费用评分
costScoreSql = '''
            UPDATE 
                chs_erp_evaluate 
            SET 
                COSTSCORE=
                # 购药总金额68分
                (
                    CASE 
                        WHEN SUMREALMONEY>=100000 THEN 68
                        WHEN SUMREALMONEY>=0 AND SUMREALMONEY<100000 THEN
                            (
                                45/(SELECT a.MAXREAL FROM((SELECT MAX(SUMREALMONEY) AS MAXREAL FROM chs_erp_evaluate WHERE SUMREALMONEY<100000)a))*SUMREALMONEY+23
                            )
                        WHEN SUMREALMONEY<0 THEN 0
                        ELSE 23
                    END
                )+
                # 购药利润总金额85分
                (
                    CASE 
                        WHEN SUMPROFIT>=100000 THEN 85
                        WHEN SUMPROFIT>=0 AND SUMPROFIT<100000 THEN
                            (
                                50/(SELECT a.MAXPRO FROM((SELECT MAX(SUMPROFIT) AS MAXPRO FROM chs_erp_evaluate WHERE SUMPROFIT <100000)a))*SUMPROFIT +35
                            )
                        WHEN SUMPROFIT<0 THEN 10
                        ELSE 35
                    END
                )+
                # 门店消费情况
                (
                    CASE 
                        WHEN STOREAMOUNT>=0  THEN
                            (
                                9/(SELECT a.MAXSTOA FROM((SELECT MAX(STOREAMOUNT) AS MAXSTOA FROM chs_erp_evaluate)a))*STOREAMOUNT 
                            )
                        ELSE 0
                    END
                )+
                (
                    CASE 
                        WHEN STOREPROFIT>=0  THEN
                            (
                                8/(SELECT a.MAXSTOP FROM((SELECT MAX(STOREPROFIT) AS MAXSTOP FROM chs_erp_evaluate)a))*STOREPROFIT 
                            )
                        ELSE 0
                    END
                )
            '''

bheaviorScoreSql = '''
                -- 药品偏好评分
                UPDATE 
                    chs_erp_evaluate 
                SET 
                    BEHAVIORSCORE=
                    (
                        CASE 
                            WHEN GOODSNUM>=10000 THEN 90
                            WHEN GOODSNUM>=0 AND GOODSNUM<10000 THEN
                                (
                                    50/(SELECT a.MAXREAL FROM((SELECT MAX(GOODSNUM) AS MAXREAL FROM chs_erp_evaluate WHERE GOODSNUM<10000)a))*GOODSNUM+40
                                )
                    ELSE 20
                    END
                )+
                # 购买其他药品情况
                (
                CASE 
                    WHEN CLASSOTHER>=10000 THEN 36
                    WHEN CLASSOTHER>0 AND CLASSOTHER<10000 THEN(
                        20/(SELECT a.MAXPRO FROM((SELECT MAX(CLASSOTHER) AS MAXPRO FROM chs_erp_evaluate WHERE CLASSOTHER <10000)a))*CLASSOTHER+16
                    )
                    ELSE 16
                    END
                )+
                # 购买小孩药品情况
                (
                CASE 
                    WHEN CLASSCHILDREN>0  THEN
                        (
                            10/(SELECT a.MAXSTOA FROM((SELECT MAX(CLASSCHILDREN) AS MAXSTOA FROM chs_erp_evaluate)a))*CLASSCHILDREN +17
                        )
                    ELSE 17
                    END
                )+
                (
                CASE 
                    WHEN  CLASSOLDMEN>0  THEN(
                        10/(SELECT a.MAXSTOP FROM((SELECT MAX(CLASSOLDMEN) AS MAXSTOP FROM chs_erp_evaluate)a))*CLASSOLDMEN+17
                    )
                    ELSE 17
                    END
                )
                '''
# insertSql
# evlInsertSql,
evlInsertSql = '''
            insert into 
                chs_erp_evaluate
                (
                    INSIDERID,
                    INSIDERCARDNO,
                    INSIDERNAME,
                    IDCARD,
                    MOBILE,
                    SEX,
                    MAILADDRESS,
                    INSCARDTYPEID,
                    BIRTHDATE,
                    NEWBIRTHDATE,
                    CREDATE,
                    LASTCONSUMDATE,
                    FREQUENCY,
                    MEANDAY,
                    INTEGRAL,
                    ADDINTEGRAL,
                    SUMREALMONEY,
                    SUMPROFIT,
                    STOREAMOUNT,
                    STOREPROFIT,
                    PLACEPOINTID,
                    UNITPRICE,
                    YEARFRE,
                    GOODSNUM,
                    CLASSOTHER,
                    CLASSCHILDREN,
                    CLASSOLDMEN
                )
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            on duplicate key update
                INSIDERID = values(INSIDERID),
                INSIDERCARDNO=values(INSIDERCARDNO),
                INSIDERNAME = values(INSIDERNAME),
                IDCARD = values(IDCARD),
                MOBILE = values(MOBILE),
                SEX = values(SEX),
                MAILADDRESS = values(MAILADDRESS),
                INSCARDTYPEID = values(INSCARDTYPEID),
                BIRTHDATE = values(BIRTHDATE),
                NEWBIRTHDATE = values(NEWBIRTHDATE),
                CREDATE = values(CREDATE),
                LASTCONSUMDATE = values(LASTCONSUMDATE),
                FREQUENCY = values(FREQUENCY),
                MEANDAY = values(MEANDAY),
                INTEGRAL = values(INTEGRAL),
                ADDINTEGRAL = values(ADDINTEGRAL),
                SUMREALMONEY = values(SUMREALMONEY),
                SUMPROFIT = values(SUMPROFIT),
                STOREAMOUNT = values(STOREAMOUNT),
                STOREPROFIT = values(STOREPROFIT),
                PLACEPOINTID = values(PLACEPOINTID),
                UNITPRICE = values(UNITPRICE),
                YEARFRE = values(YEARFRE),
                GOODSNUM = values(GOODSNUM),
                CLASSOTHER=values(CLASSOTHER),
                CLASSCHILDREN=values(CLASSCHILDREN),
                CLASSOLDMEN=values(CLASSOLDMEN)
            '''
# selectSql
# evlSelectSql
evlSelectSql = '''
            SELECT 
                a.INSIDERID,
                a.INSIDERCARDNO,
                a.INSIDERNAME,
                a.IDCARD,
                a.MOBILE,
                a.SEX,
                a.MAILADDRESS,
                a.INSCARDTYPEID,
                a.BIRTHDATE,
                a.NEWBIRTHDATE,
                a.CREDATE,
                b.MAXTIME,
                b.FREQUENCY,
                b.MEANDAY,
                a.INTEGRAL,
                a.ADDINTEGRAL,
                b.SUMREALMONEY,
                b.SUMPROFIT,
                c.STOREAMOUNT,
                c.PROFIT,
                a.PLACEPOINTID,
                b.UNITPRICE,
                b.YEARFRE,
                d.GOODSNUM,
                e.OTHER,
                e.CHILDREN,
                e.OLDMEN
            FROM 
                erp_member as a,chs_erp_amount_data as b ,chs_erp_store as c ,chs_erp_goods_num as d,chs_erp_goods_class as e
            where 
                a.INSIDERID=b.INSIDERID and a.PLACEPOINTID = c.PLACEPOINTID and USESTATUS=1 and a.INSIDERID = d.INSIDERID and a.INSIDERID=e.INSIDERID
            '''
# =========================================
