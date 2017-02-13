# coding:utf8

import json
import urllib
import urllib2

import datetime
import uuid

import MySQLdb
import logging
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from flask import request

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

        conn, cur = connect_db()
        cur.execute("delete from schedule_list where id='%s'" % sche_id)
        conn.commit()
        cur.close()
        conn.close()
        return 'success'
    except:
        return 'failure'


@app.route('/list_schedule')
def list_schedule():
    conn, cur = connect_db()
    cur.execute("select * from schedule_list")
    result = cur.fetchall()
    sche_list = list(result)
    sche_list.sort(key=lambda d: d[3].strftime('%M%S'), reverse=True)
    cur.close()
    conn.close()

    return render_template('list_schedule.html', sche_list=sche_list, status_map=status_map,
                           operation_map=operation_map)


@app.route('/add_schedule')
def add_schedule():
    try:
        spider_name = request.args['spider_name']
        interval = int(request.args['interval'])
        start_time = request.args['start_time']
        sche_id = str(uuid.uuid1())
        scheduler.add_job(add_job, 'interval', minutes=interval, id=sche_id, args=(spider_name,),
                          next_run_time=start_time)
        conn, cur = connect_db()
        cur.execute(
            "insert into schedule_list(id, spider_name, min_interval, first_run_time, status) VALUES ('%s','%s','%s','%s','%s')" % (
            sche_id, spider_name, str(interval), start_time, '0'))
        conn.commit()
        cur.close()
        conn.close()
        return 'success'
    except:
        return 'failure'


@app.route('/pause_schedule')
def pause_schedule():
    try:
        sche_id = request.args['sche_id']
        scheduler.pause_job(sche_id)

        conn, cur = connect_db()
        cur.execute("update schedule_list set status=%s where id='%s'" % (1, sche_id))
        conn.commit()
        cur.close()
        conn.close()
        return 'success'
    except:
        return 'failure'


@app.route('/resume_schedule')
def resume_schedule():
    try:
        sche_id = request.args['sche_id']
        scheduler.resume_job(sche_id)

        conn, cur = connect_db()
        cur.execute("update schedule_list set status=%s where id='%s'" % (0, sche_id))
        conn.commit()
        cur.close()
        conn.close()
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


def connect_db():
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB,
                           charset="utf8")
    cur = conn.cursor()
    return conn, cur

def scan_job_list():
    response = urllib2.urlopen('%s/listjobs.json?project=NewsSpider' % SCRAPYD_DOMAIN).read()
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
conn, cur = connect_db()
cur.execute("CREATE TABLE if not EXISTS schedule_list("
            "`id` char(64) NOT NULL DEFAULT '',"
            "`spider_name` varchar(128) NOT NULL DEFAULT '',"
            "`min_interval` int(11) NOT NULL COMMENT 'measured in minutes',"
            "`first_run_time` datetime DEFAULT CURRENT_TIMESTAMP,"
            "`status` int(11) DEFAULT '0' COMMENT '0/1/2 means running/pause/finished',"
            "`created_time` datetime DEFAULT CURRENT_TIMESTAMP,"
            "PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8;")
conn.commit()
cur.execute("select * from schedule_list")
result = cur.fetchall()
cur.close()
conn.close()
for res in result:
    scheduler.add_job(add_job, 'interval', minutes=res[2], id=res[0], args=(res[1],), next_run_time=res[3])
    if res[4] == 1:
        scheduler.pause_job(res[0])

app.run(host='0.0.0.0', port=4399, debug=IS_DEV)
