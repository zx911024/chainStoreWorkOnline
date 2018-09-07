# -*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-08-23  10:39
"""
from process.chsErpUpdateData import MaxChsErpOrderDate
from process.chsErpUpdateData import updateChsErpOrder, updateChsErpAmountData
from process.chsErpUpdateData import updateChsErpGoodsMember, updateChsErpGoodsClass, updateChsErpGoodsNum
from threading import Timer
from logConf.logger import get_logger

logger = get_logger()

LASTORDERTIME = MaxChsErpOrderDate()
# LASTORDERTIME = '2018-09-07'
upAmount = updateChsErpAmountData()
upOrder = updateChsErpOrder()
upGoodsMember = updateChsErpGoodsMember()
upGoodsClass = updateChsErpGoodsClass()
upGoodsNum = updateChsErpGoodsNum()


def updateChsData():
    '''
    定时任务，非阻塞（Timer）
    '''
    logger.info("更新chs_erp_order")
    upOrder.updateData()
    logger.info("更新chs_erp_goods_member")
    upGoodsMember.updateData(LASTORDERTIME)
    logger.info("更新chs_erp_amount_data")
    upAmount.updateData()
    logger.info("更新chs_erp_goods_num")
    upGoodsNum.updateData()
    logger.info("更新chs_erp_goods_class")
    upGoodsClass.updateData()
    logger.info("等待12小时")
    t = Timer(43200, updateChsData)
    t.start()


if __name__ == "__main__":
    updateChsData()
