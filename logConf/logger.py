# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author  jakey
# Date 2017-12-01 15:26
"""
日志加载模块
"""
from __future__ import print_function

import os
import sys
import logging
import logging.config
from logConf import log_conf


LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")

try:
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
except IOError as io_except:
    print("log目录文件初始化失败%s" % io_except)
    sys.exit(1)


def get_logger(log_name="data", log_path=LOG_PATH):
    """
    :param log_name: 只提供data(debug) 和 mail(Critical)
    :param log_path: 默认目录为wjy-log
    :return:
    """
    logging.config.dictConfig(log_conf.logging_conf(log_path))
    logger = logging.getLogger(log_name)
    return logger
