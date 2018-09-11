# -*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-08-21  15:27
"""
import datetime
from common.dbase import dbase
from logConf.logger import get_logger
from conf.chsErpUpdateSql import selectSqlOrder, insertSqlOrder, selectSqlAmount, insertSqlAmount
from conf.chsErpUpdateSql import selectSqlMember, insertSqlMember, selectSqlNum, insertSqlNum
from conf.chsErpUpdateSql import selectSqlClass, insertSqlClass, selectSqlStore, insertSqlStore, updateUseClass

logger = get_logger()


def MaxChsErpOrderDate():
    '''
    获取增量增加数据时间
    :return:MaxDate：时间
    '''
    selectSql = '''select max(CREDATE) from chs_erp_order'''
    DB = dbase()
    MaxDate = DB.readDb(selectSql)
    return MaxDate


class updateChsErpOrder():
    def __init__(self):
        self.DBASE = dbase()

    def updateData(self):
        '''
        更新数据，批量更新（若数据库中已经存在就更新，若存在则插入）
        '''
        logger.info("订单数据查询开始:ChsErpOrder")
        # 参数selectSqlOrder在配置文件中
        data = self.DBASE.readDb(selectSqlOrder)
        logger.info("订单查询结束")
        # 参数insertSqlOrder在配置文件中
        logger.info("开始插入订单信息数据:chs_erp_order -> data")
        self.DBASE.writeDbs(insertSqlOrder, data)
        logger.info("更新正式库")
        self.DBASE.writeDbsOnline(insertSqlOrder, data)
        logger.info("数据插入结束")

class updateChsErpAmountData():
    def __init__(self):
        self.DBASE = dbase()

    def updateData(self):
        '''
        更新数据，批量更新（若数据库中已经存在就更新，若存在则插入）
        '''
        logger.info("查询金额相关数据开始:ChsErpAmountData")
        data = self.DBASE.readDb(selectSqlAmount)
        logger.info("查询结束")
        logger.info("开始插入金额相关数据")
        self.DBASE.writeDbs(insertSqlAmount, data)
        logger.info("数据插入结束")
        logger.info("更新金额相关数据开始")
        updateSql = ["UPDATE chs_erp_amount_data set SUMPROFIT = SUMREALMONEY-SUMCOSTINGMONEY",
                     "UPDATE chs_erp_amount_data set UNITPRICE = ROUND(SUMREALMONEY/FREQUENCY,2)"]
        update2 = "UPDATE chs_erp_amount_data set MEANDAY = CEILING(TIMESTAMPDIFF(SECOND,MINTIME,UP_DATE)/(FREQUENCY*24*3600))"
        logger.info("更新SUMPROFIT、UNITPRICE")
        for sql in updateSql:
            self.DBASE.updateDb(sql)
        logger.info("更新MEANDAY")
        self.DBASE.updateDb(update2)
        logger.info("更新完毕")


class updateChsErpGoodsMember():
    def __init__(self):
        self.DBASE = dbase()

    def updateData(self, LASTORDERTIME):
        selectSql = selectSqlMember % LASTORDERTIME
        logger.info("GoodsMember数据查询开始")
        data = self.DBASE.readDb(selectSql)
        logger.info("数据查询结束")
        if data:
            logger.info("数据插入开始")
            self.DBASE.writeDbs(insertSqlMember, data)
            logger.info("数据插入结束")
        else:
            logger.info("数据为空")
        logger.info("更新USECLASSAGE")
        self.DBASE.updateDb(updateUseClass)
        logger.info("更新结束")


class updateChsErpGoodsNum():
    def __init__(self):
        self.DBASE = dbase()

    def updateData(self):
        logger.info("ChsErpGoodsNum数据查询开始")
        data = self.DBASE.readDb(selectSqlNum)
        logger.info("数据查询结束")
        logger.info("数据插入开始")
        self.DBASE.writeDbs(insertSqlNum, data)
        logger.info("数据插入结束")


class updateChsErpGoodsClass():
    def __init__(self):
        self.DBASE = dbase()

    def updateData(self):
        logger.info("ChsErpGoodsClass数据查询开始")
        data = self.DBASE.readDb(selectSqlClass)
        logger.info("数据查询结束")
        logger.info("数据插入开始")
        self.DBASE.writeDbs(insertSqlClass, data)
        logger.info("数据插入结束")


class UpdateChsErpStore():
    def __init__(self):
        self.DBDATA = dbase()

    def primeCost(self, rsaid):
        '''
        统计每个会员的订单的成本金额
        :param rsaid:总单ID
        :return:每笔订单的成本金额
        '''
        selectSql = "select sum(COSTINGMONEY) from erp_order_detail where RSAID = %s" % rsaid
        primeAmount = self.DBDATA.readDb(selectSql)
        return primeAmount

    def storeAmount(self, storeID):
        '''
        某门店销售总金额
        :param storeID:门店ID
        :return:总金额
        '''
        selectSqlReal = "select sum(REALMONEY) from erp_order WHERE PLACEPOINTID= %s" % storeID
        selectSqlProfit = "select RSAID from erp_order WHERE PLACEPOINTID= %s" % storeID
        try:
            sumAmount = self.DBDATA.readDb(selectSqlReal)[0][0]
        except:
            sumAmount = None

        rsaidAll = self.DBDATA.readDb(selectSqlProfit)
        primeAmount = 0
        for i in rsaidAll:
            amountTmp = self.primeCost(i)
            if amountTmp[0][0]:
                # 成本总金额
                primeAmount += amountTmp[0][0]
        if sumAmount > 0:
            profit = sumAmount - primeAmount
        else:
            profit = None
        return [sumAmount, profit]

    def storeProcess(self):
        '''
        计算表chs_erp_store:门店数据
        return:
        '''
        logger.info("查询所有门店信息：ChsErpStore")
        storeIDdata = self.DBDATA.readDb(selectSqlStore)
        allStoreData = []
        for index, i in enumerate(storeIDdata):
            storeInfo = []
            storeID = i[0]
            logger.info("查询第" + str(index) + "家门店的成本金额")
            costStore = self.storeAmount(storeID)
            logger.info("查询结束")
            storeInfo.extend(i)
            storeInfo.extend(costStore)
            allStoreData.append(storeInfo)
            if index % 1 == 0:
                self.DBDATA.writeDbs(insertSqlStore, allStoreData)
                allStoreData = []
# LASTORDERTIME='2018-08-28'
# upGoodsMember = updateChsErpGoodsMember()
# upGoodsMember.updateData(LASTORDERTIME)