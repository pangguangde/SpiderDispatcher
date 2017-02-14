# coding:utf8

import json
import urllib
import urllib2

import datetime
import uuid

import logging
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from flask import request
from peewee import SqliteDatabase

from ScheduleInfo import ScheduleInfo
from settings import *
from util import send_email

__author__ = 'muyuguangchen'

app = Flask(__name__)
status_map = ['running', 'paused']
operation_map = [('pause', 'warning'), ('resume', 'success')]

# timed task scheduler
scheduler = BackgroundScheduler()

# ********************************* init logger *********************************
logger = logging.getLogger('SpiderDispatcher')
ch = logging.StreamHandler()
fmter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
ch.setFormatter(fmt=fmter)
logger.setLevel(logging.DEBUG)
logger.addHandler(hdlr=ch)


db = SqliteDatabase('schedule_info.db')


@app.route('/add_job/<spider_name>')
def add_job(spider_name):
    req = urllib2.Request('%s/schedule.json' % SCRAPYD_DOMAIN)
    data = urllib.urlencode({'project': PROJECT_NAME, 'spider': spider_name})
    # enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    resp = json.loads(response.read())
    if resp['status'] == 'ok':
        return 'success'
    else:
        return 'failure'


@app.route('/cancel/<job_id>')
def cancel_job(job_id):
    req = urllib2.Request('%s/cancel.json' % SCRAPYD_DOMAIN)
    data = urllib.urlencode({'project': PROJECT_NAME, 'job': job_id})
    # enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    resp = json.loads(response.read())
    if resp['status'] == 'ok':
        print resp
        return 'success'
    else:
        return 'failure'


@app.route('/list_jobs')
def list_jobs():
    response = urllib2.urlopen('%s/listjobs.json?project=%s' % (SCRAPYD_DOMAIN, PROJECT_NAME)).read()
    data = json.loads(response)

    data_running = data['running']
    data_running.sort(key=lambda d: d['start_time'], reverse=True)
    data['running'] = data_running

    data_finished = data['finished']
    data_finished.sort(key=lambda d: d['start_time'], reverse=True)
    data['finished'] = data_finished
    return render_template('list_jobs.html', data=data)


@app.route('/')
@app.route('/index')
def index():
    response = urllib2.urlopen('%s/listspiders.json?project=%s' % (SCRAPYD_DOMAIN, PROJECT_NAME)).read()
    data = json.loads(response)
    return render_template('index.html', data=data['spiders'],
                           cur_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00"))


@app.route('/del_schedule')
def del_schedule():
    try:
        sche_id = request.args['sche_id']
        scheduler.remove_job(sche_id)
        ScheduleInfo.delete().where(ScheduleInfo.id == sche_id).execute()
        return 'success'
    except:
        return 'failure'


@app.route('/list_schedule')
def list_schedule():
    schedules = ScheduleInfo.select()
    sche_list = []
    for sche in schedules:
        sche_list.append((sche.id, sche.spider_name, sche.min_interval, sche.first_run_time, sche.status, sche.created_time))

    return render_template('list_schedule.html', sche_list=sche_list, status_map=status_map,
                           operation_map=operation_map)


@app.route('/add_schedule')
def add_schedule():
    try:
        si = ScheduleInfo()
        si.spider_name = request.args['spider_name']
        si.min_interval = int(request.args['interval'])
        si.first_run_time = request.args['start_time']
        si.id = str(uuid.uuid1())
        scheduler.add_job(add_job, 'interval', minutes=si.min_interval, id=si.id, args=(si.spider_name,), next_run_time=si.first_run_time)
        try:
            si.save(force_insert=True)
        except:
            si.save()
        return 'success'
    except:
        return 'failure'


@app.route('/pause_schedule')
def pause_schedule():
    try:
        sche_id = request.args['sche_id']
        scheduler.pause_job(sche_id)
        ScheduleInfo.update(status=1).where(ScheduleInfo.id == sche_id).execute()
        return 'success'
    except:
        return 'failure'


@app.route('/resume_schedule')
def resume_schedule():
    try:
        sche_id = request.args['sche_id']
        scheduler.resume_job(sche_id)
        ScheduleInfo.update(status=0).where(ScheduleInfo.id == sche_id).execute()
        return 'success'
    except:
        return 'failure'


@app.route('/schedule_start/<msg>')
def schedule_start(msg):
    scheduler.add_job(job1, 'interval', seconds=10, id='test', args=(msg,), next_run_time='2016-12-29 09:50:20')
    return 'schedule started!'


@app.route('/schedule_stop')
def schedule_stop():
    scheduler.remove_job('test')
    return 'schedule stopped!'


def job1(a):
    logger.info(datetime.datetime.now(), a)


def scan_job_list():
    response = urllib2.urlopen('%s/listjobs.json?project=%s' % (SCRAPYD_DOMAIN, PROJECT_NAME)).read()
    data = json.loads(response)
    pending_len = len(data['pending'])
    running_len = len(data['running'])
    if pending_len >= 1 and running_len == 2:
        send_email('pangguangde@souche.com', 'che168车辆爬虫监控',
                   '<h1>scrapyd 爬虫运行阻塞或状态异常</h1>'
                   '<table border=1>'
                   '<tbody>'
                   '<tr>'
                   '<td>Pending</td>'
                   '<td>Running</td>'
                   '</tr>'
                   '<tr>'
                   '<td>%s</td>'
                   '<td>%s</td>'
                   '</tr>'
                   '</table>'
                   '<p>%s</p>' % (pending_len, running_len, datetime.datetime.now()))
    logger.info('writing job list scan result: {pending: %s, running: %s}' % (pending_len, running_len))


# it is also possible to enable the API directly
# scheduler.api_enabled = True

scheduler.start()
sche_infos = ScheduleInfo.select()
for sche_info in sche_infos:
    scheduler.add_job(add_job, 'interval', minutes=sche_info.min_interval, id=sche_info.id, args=(sche_info.spider_name,), next_run_time=sche_info.first_run_time)
    if sche_info.status == 1:
        scheduler.pause_job(sche_info.id)

app.run(host='0.0.0.0', port=4399, debug=IS_DEV)
