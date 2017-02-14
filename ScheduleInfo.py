# coding:utf8
import datetime
from peewee import *
from sqlobject.tests.test_auto import Person

__author__ = 'pangguangde'

db = SqliteDatabase('schedule_info.db')

class ScheduleInfo(Model):
	id = CharField(64, primary_key=True)
	spider_name = CharField(128, null=False)
	min_interval = IntegerField(null=False)
	first_run_time = DateTimeField(default=datetime.datetime.now())
	status = IntegerField(default=0)
	created_time = DateTimeField(default=datetime.datetime.now())

	# 所用数据库为db
	class Meta:
		database = db

db.create_table(ScheduleInfo, safe=True)
