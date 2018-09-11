#-*- coding:utf-8 -*-
"""
author:zhangxun
Created on 2018-09-07  11:38
"""
from process.UnderLineToOnline import UnderLineToOnlineEvaluate
from threading import Timer
from logConf.logger import get_logger

logger = get_logger()
localToOnline = UnderLineToOnlineEvaluate()


def updateChsData():
    '''
    定时任务，非阻塞（Timer）
    '''
    logger.info("上传chs_erp_order")
    localToOnline.updateOnline()
    logger.info("等待12小时")
    t = Timer(43200, updateChsData)
    t.start()


if __name__ == "__main__":
    updateChsData()
