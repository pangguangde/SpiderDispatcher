# coding:utf8
import platform

__author__ = 'muyuguangchen'

# todo: please rewrite the sentence above according to your own situation
IS_DEV = True if platform.platform().find('Linux') == -1 else False

PROJECT_NAME = 'MySpiderProject'

if IS_DEV:
    SCRAPYD_DOMAIN = 'http://127.0.0.1:6800'

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWD = ''
    MYSQL_DB = 'test'  # please check out database 'test' in your MySQL, create one if not exist
    MYSQL_PORT = 3306
else:
    SCRAPYD_DOMAIN = 'http://127.0.0.1:6800'

    MYSQL_HOST = 'XXXXXXXXXXXX'
    MYSQL_USER = 'XXXXXXXXXXXX'
    MYSQL_PASSWD = '****************'
    MYSQL_DB = 'XXXXXXXXXXXX'
    MYSQL_PORT = 3306
