# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author  jakey
# Date 2017-12-01 18:00

import os
import sys
from datetime import date

def logging_conf(log_path):
    return {
        "mail": {
            "level": "ERROR",
            "propagate": False,
            "handlers": ["mail"]
        },
        "loggers": {
            "data": {
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["data", "console"]
            }
        },
        "disable_existing_loggers": False,
        "handlers": {
            "data": {
                "formatter": "simple",
                "backupCount": 10,
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": 10485760,
                "filename": os.path.join(log_path, "wjy-" + date.today().isoformat() + ".log")
            },
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
            "mail": {
                "toaddrs": ['124143758@qq.com','87199145@qq.com'],
                "mailhost": ["smtp.163.com",'25'],
                "fromaddr": "zhangxun0828@163.com",# 发送人
                # "level": "CRITICAL",
                "level": "ERROR",
                "credentials": ("zhangxun0828","zx911024"),
                "formatter": "mail",
                "class": "logging.handlers.SMTPHandler",
                "subject": "程序异常"
            }
        },
        "formatters": {
            "default": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "%(asctime)s - %(levelname)s - %(module)s.%(name)s : %(message)s"
            },
            "simple": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "%(asctime)s - %(levelname)s - %(module)s.%(name)s : %(message)s"
                # "format": "%(asctime)s - %(levelname)s - %(message)s"
            },
            "mail": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "%(asctime)s : %(message)s"
            }
        },
        "version": 1
    }
