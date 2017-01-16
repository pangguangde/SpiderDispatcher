SpiderDispatcher
===
`SpiderDispatcher` 是一个轻量级的可视化爬虫管理系统，负责爬虫的调度和管理，`scrapyd` and `APScheduler` 框架设计，
简单易用，极低的系统资源占用率。目前只是一个初级的版本，鄙人还会继续优化的 ╮(╯▽╰)╭
<br></br>
`SpiderDispatcher` is a visualized lightweight spider manage system designed base on `scrapyd` and `APScheduler`, 
easy to install and use, low resource occupancy. It's an original version now, I'll optimizing it later ╮(╯▽╰)╭

REQUIREMENT
---

```
Python 2.7.x
MySQL >= 5.6
```

INSTALL
---

```
git clone git@gitlab.com:pangguangde/SpiderDispatcher.git
cd SpiderDispatcher
pip install -r requirements.txt
```


CONFIGURE
---
**Edit** `SpiderDispatcher/settings.py` according to your own situation.

check out database `test` in your MySQL, create it if not existed.

**notice** how to judge `IS_DEV` is important  ╮(╯▽╰)╭

RUN
---

```
cd $YOUR_SPIDER_PROJECT_DIR
scrapyd
cd SpiderDispatcher
python SpiderDispatcher.py
open url http://0.0.0.0:4399/
```

SHORTCUTS
---
**Index:**
![](shortcuts/index.png)

**List Jobs:**
![](shortcuts/job_list.png)

**List Schedule:**
![](shortcuts/list_schedule.png)

OTHER
=====
**Any questions or suggestions you can contact me via email** `muyuguangchen@gmail.com` **or just remind me in Issues, 
THX ╮(╯▽╰)╭**

<p style="font-size: 3em"><b>Enjoy your crawling!</b></p>



