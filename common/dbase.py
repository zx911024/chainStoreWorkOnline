# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 11:30:13 2017
@author: zhangxun
"""
import pymysql
import pandas as pd
from logConf.logger import get_logger
from conf.conf import *


logging = get_logger()


class dbase():
    def __init__(self):
        pass

    def connectSql(self):
        '''
        连接数据库
        :return:返回连接对象
        '''
        try:
            conn = pymysql.connect(host=db_ip, user=db_user, database=db_name, password=db_pass, port=3306)
            return conn
        except Exception as e:
            logging.error(e)
            return False

    def writeDbs(self, sql, values):
        """
        连接mysql数据库（写），并进行写的操作，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回true
        """
        try:
            conn = pymysql.connect(host=db_ip, user=db_user, database=db_name, password=db_pass, port=3306)
            cursor = conn.cursor()
        except Exception as e:
            logging.error('数据库连接失败:%s' % e)
            return False
        try:
            cursor.executemany(sql, values)
            conn.commit()  # 提交事务
        except Exception as e:
            conn.rollback()  # 如果出错，则事务回滚
            logging.error('数据写入失败:%s' % e)
            return False
        finally:
            cursor.close()
            conn.close()
        return True

    def writeDb(self, sql, values):
        """
        连接mysql数据库（写），并进行写的操作，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回true
        """
        try:
            conn = pymysql.connect(host=db_ip, user=db_user, database=db_name, password=db_pass, port=3306)
            cursor = conn.cursor()
        except Exception as e:
            logging.error('数据库连接失败:%s' % e)
            return False
        try:
            cursor.execute(sql, values)
            conn.commit()  # 提交事务
        except Exception as e:
            conn.rollback()  # 如果出错，则事务回滚
            logging.error('数据写入失败:%s' % e)
            return False
        finally:
            cursor.close()
            conn.close()
        return True

    def createDb(self, sql):
        """
        连接mysql数据库（从），并进行数据查询，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false
        """
        try:
            conn = pymysql.connect(database=db_name, user=db_user, password=db_pass, host=db_ip, port=3306)
            cursor = conn.cursor()
        except Exception as e:
            logging.error('数据库连接失败:%s' % e)
            return False
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logging.error('建表失败:%s' % e)
            return False
        finally:
            cursor.close()
            conn.close()
        return True

    def readDb(self, sql):
        """
        连接mysql数据库（从），并进行数据查询，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回查询到的数据，这个数据是经过转换的，转成字典格式，方便模板调用，其中字典的key是数据表里的字段名
        """
        try:
            conn = pymysql.connect(host=db_ip, user=db_user, database=db_name, password=db_pass, port=3306)
            cursor = conn.cursor()
        except Exception as e:
            logging.error('数据库连接失败:%s' % e)
            return False
        try:
            cursor.execute(sql)
            # data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
            #         cursor.fetchall()]
            data = cursor.fetchall()  # 转换数据，字典格式
        except Exception as  e:
            logging.error('数据执行失败:%s' % e)
            return False
        finally:
            cursor.close()
            conn.close()
        return data

    def readDbDict(self, sql):
        """
        连接mysql数据库（从），并进行数据查询，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回查询到的数据，这个数据是经过转换的，转成字典格式，方便模板调用，其中字典的key是数据表里的字段名
        """
        try:
            conn = pymysql.connect(host=db_ip, user=db_user, database=db_name, password=db_pass, port=3306)
            cursor = conn.cursor()
        except Exception as e:
            logging.error('数据库连接失败:%s' % e)
            return False
        try:
            cursor.execute(sql)
            data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                    cursor.fetchall()]
            # data = cursor.fetchall()  # 转换数据，字典格式
        except Exception as  e:
            logging.error('数据执行失败:%s' % e)
            return False
        finally:
            cursor.close()
            conn.close()
        return data

    def updateDb(self, sql):
        """
        连接mysql数据库（从），并进行数据查询，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false
        """
        try:
            conn = pymysql.connect(database=db_name, user=db_user, password=db_pass, host=db_ip, port=3306)
            cursor = conn.cursor()
        except Exception as e:
            logging.error('数据库连接失败:%s' % e)
            return False
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logging.error('数据更新失败:%s' % e)
            return False
        finally:
            cursor.close()
            conn.close()
        return True

    def writeDbsOnline(self, sql, values):
        """
        连接mysql数据库（写），并进行写的操作，如果连接失败，会把错误写入日志中，并返回false，如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回true
        """
        try:
            conn = pymysql.connect(host=db_ip_online, user=db_user_online, database=db_name_online,
                                   password=db_pass_online, port=3306)
            cursor = conn.cursor()
        except Exception as e:
            logging.error('数据库连接失败:%s' % e)
            return False
        try:
            cursor.executemany(sql, values)
            conn.commit()  # 提交事务
        except Exception as e:
            conn.rollback()  # 如果出错，则事务回滚
            logging.error('数据写入失败:%s' % e)
            return False
        finally:
            cursor.close()
            conn.close()
        return True
