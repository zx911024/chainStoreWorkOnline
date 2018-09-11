# -*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-08-23  10:39
"""
import datetime
from process.evaluateScore import EvaluateContent
from process.chsErpUpdateData import MaxChsErpOrderDate
from process.chsErpUpdateData import updateChsErpOrder, updateChsErpAmountData
from process.chsErpUpdateData import updateChsErpGoodsMember, updateChsErpGoodsClass, updateChsErpGoodsNum
from process.UnderLineToOnline import UnderLineToOnlineEvaluate
from threading import Timer
from logConf.logger import get_logger

logger = get_logger()

LASTORDERTIME_TMP = MaxChsErpOrderDate()
LASTORDERTIME = LASTORDERTIME_TMP
upOrder = updateChsErpOrder()
upAmount = updateChsErpAmountData()
upGoodsMember = updateChsErpGoodsMember()
upGoodsClass = updateChsErpGoodsClass()
upGoodsNum = updateChsErpGoodsNum()
localToOnline = UnderLineToOnlineEvaluate()
evaluateMem = EvaluateContent()
flag = 0

def updateChsData():
    '''
    定时任务，非阻塞（Timer）
    '''
    global flag
    if flag==0:
        logger.info("更新chs_erp_order")
        upOrder.updateData()
        logger.info("更新chs_erp_goods_member")
        logger.info(LASTORDERTIME)
        upGoodsMember.updateData(LASTORDERTIME)
        logger.info("更新chs_erp_amount_data")
        upAmount.updateData()
        logger.info("更新chs_erp_goods_num")
        upGoodsNum.updateData()
        logger.info("更新chs_erp_goods_class")
        upGoodsClass.updateData()
        logger.info("更新chs_erp_goods_evaluate")
        evaluateMem.evaluate()
        logger.info("上传chs_erp_order")
        localToOnline.updateOnline()
    else:
        flag=1
    # 获取现在时间
    now_time = datetime.datetime.now()
    # 获取明天时间
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # 获取明天3点时间
    next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 03:00:00",
                              "%Y-%m-%d %H:%M:%S")
    # 获取距离明天3点时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    logger.info("等待3点")
    logger.info(timer_start_time)
    t = Timer(timer_start_time, updateChsData)
    t.start()

if __name__ == "__main__":
    updateChsData()
