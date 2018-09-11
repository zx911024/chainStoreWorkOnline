#-*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-08-24  09:49
"""
from common.dbase import dbase
from logConf.logger import get_logger
logger=get_logger()
from conf.evaluateScoreSql import identitySql,buyHistorySql,bheaviorScoreSql,costScoreSql,evlInsertSql,evlSelectSql
class EvaluateContent():
    def __init__(self):
        self.DBCON = dbase()
    def evaluate(self):
        logger.info("总表数据查询开始")
        data = self.DBCON.readDb(evlSelectSql)
        logger.info("查询结束")
        logger.info("插入数据开始")
        self.DBCON.writeDbs(evlInsertSql,data)
        logger.info("数据插入结束")
        logger.info("更新AGE、CREATINTERVAL、LASTINTERVAL")
        updateSql = ["UPDATE chs_erp_evaluate SET AGE = FLOOR(TIMESTAMPDIFF(SECOND,BIRTHDATE,NOW())/(3600*24*365));",
                     "UPDATE chs_erp_evaluate SET CREATINTERVAL = FLOOR(TIMESTAMPDIFF(SECOND,CREDATE,NOW())/(3600*24));",
                     "UPDATE chs_erp_evaluate SET LASTINTERVAL = FLOOR(TIMESTAMPDIFF(SECOND,LASTCONSUMDATE,NOW())/(3600*24));"
                    ]
        sumScoreSql = '''UPDATE chs_erp_evaluate SET MEMBERSCORE = HISTORYSCORE+IDENTITYSCORE+COSTSCORE+BEHAVIORSCORE'''
        classUpdateSql = ["UPDATE chs_erp_evaluate SET CLASSCHILDREN = (CASE WHEN CLASSCHILDREN is null then 0 else CLASSCHILDREN end )",
                          "UPDATE chs_erp_evaluate SET CLASSOTHER = (CASE WHEN CLASSOTHER is null then 0 else CLASSOTHER end )",
                          "UPDATE chs_erp_evaluate SET CLASSOLDMEN = (CASE WHEN CLASSOLDMEN is null then 0 else CLASSCHILDREN end )",
                          "UPDATE chs_erp_evaluate SET CLASSOTHER = GOODSNUM-CLASSOLDMEN-CLASSCHILDREN"
                          ]

        for sql in updateSql:
            logger.info("更新数据中")
            self.DBCON.updateDb(sql)
        logger.info("开始更新CLASSCHILD、CLASSOTHER、CLASSOLDMEN")
        for updateSql in classUpdateSql:
            logger.info("更新中")
            self.DBCON.updateDb(updateSql)
        logger.info("数据更新完毕")
        logger.info("更新各部分分数")
        logger.info("更新身份特质分数")
        self.DBCON.updateDb(identitySql)
        logger.info("更新购药历史分数")
        self.DBCON.updateDb(buyHistorySql)
        logger.info("更新消费分数")
        self.DBCON.updateDb(costScoreSql)
        logger.info("更新购药偏好分数")
        self.DBCON.updateDb(bheaviorScoreSql)
        logger.info("更新总分")
        self.DBCON.updateDb(sumScoreSql)
        logger.info("更新完成")

