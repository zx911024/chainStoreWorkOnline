# -*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-08-03  20:46
"""
from process.chsErpUpdateData import UpdateChsErpStore
from logConf.logger import get_logger
from threading import Timer

logger = get_logger()
upDataProcess = UpdateChsErpStore()


def updateChsData():
    '''
    定时任务，非阻塞（Timer）
    '''
    logger.info("更新店铺收益、销售总金额")
    upDataProcess.storeProcess()
    logger.info("等待12小时")
    t = Timer(43200, updateChsData)
    t.start()


if __name__ == "__main__":
    updateChsData()
