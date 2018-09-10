# -*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-08-23  10:39
"""
import datetime
from process.chsErpUpdateData import MaxChsErpOrderDate
from process.chsErpUpdateData import updateChsErpOrder, updateChsErpAmountData
from process.chsErpUpdateData import updateChsErpGoodsMember, updateChsErpGoodsClass, updateChsErpGoodsNum
from process.UnderLineToOnline import UnderLineToOnline
from threading import Timer
from logConf.logger import get_logger

logger = get_logger()

LASTORDERTIME = MaxChsErpOrderDate()
upOrder = updateChsErpOrder()
upAmount = updateChsErpAmountData()
upGoodsMember = updateChsErpGoodsMember()
upGoodsClass = updateChsErpGoodsClass()
upGoodsNum = updateChsErpGoodsNum()
localToOnline = UnderLineToOnline()


def func():
    print("haha")
    #如果需要循环调用，就要添加以下方法
    timer = Timer(86400, func)
    timer.start()

def updateChsData():
    '''
    定时任务，非阻塞（Timer）
    '''
    flag = 0
    if flag==1:
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
    next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 04:00:00",
                              "%Y-%m-%d %H:%M:%S")
    # 获取距离明天４点时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    logger.info("等待4点")
    logger.info(timer_start_time)
    t = Timer(timer_start_time, updateChsData)
    t.start()

if __name__ == "__main__":
    updateChsData()
