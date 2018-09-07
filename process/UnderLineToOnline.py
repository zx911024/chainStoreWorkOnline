#-*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-09-06  14:48
"""
from common.dbase import dbase
from conf.chsErpUpdateSql import selectSqlEvaluate, insertSqlEvaluate
from logConf.logger import get_logger

logger = get_logger()


class UnderLineToOnline():
    def __init__(self):
        self.DBCON = dbase()

    def updateOnline(self):
        logger.info("查询本地chs_erp_evaluate数据")
        data = self.DBCON.readDb(selectSqlEvaluate)
        logger.info("插入正式库")
        self.DBCON.writeDbsOnline(insertSqlEvaluate, data)
        logger.info("插入数据结束")
