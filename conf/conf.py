# -*- coding: utf-8 -*-

import os
import configparser as ConfigParser

cfg = ConfigParser.ConfigParser()
BASE_DIR = os.path.dirname(__file__)
cfg.read(os.path.join(BASE_DIR, 'config'))

# pgsql
db_name = cfg.get("mysql_test", "db_name")
db_user = cfg.get("mysql_test", "db_user")
db_pass = cfg.get("mysql_test", "db_pass")
db_ip = cfg.get("mysql_test", "db_ip")
# online
db_name_online = cfg.get("mysql_online", "db_name")
db_user_online = cfg.get("mysql_online", "db_user")
db_pass_online = cfg.get("mysql_online", "db_pass")
db_ip_online = cfg.get("mysql_online", "db_ip")
