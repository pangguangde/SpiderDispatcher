# coding:utf8
import platform

__author__ = 'muyuguangchen'

# todo: please rewrite the sentence above according to your own situation
IS_DEV = True if platform.platform().find('Linux') == -1 else False

PROJECT_NAME = 'default'

SCRAPYD_DOMAIN = 'http://127.0.0.1:6800'

MAIL_SENDER = "XXXXXXX@qq.com"
MAIL_PSWD = "*******"
MAIL_RECIEVER = "XXXXXXXX@qq.com"
