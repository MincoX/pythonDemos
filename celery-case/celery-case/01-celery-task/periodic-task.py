from celery import Celery
from celery.schedules import crontab

import tasks

app = Celery(
    'celery_task',  # 为 celery 对象起一个名字(无实际作用)
    broker='redis://:mincoroot_924@127.0.0.1:6379',
    backend='redis://:mincoroot_924@127.0.0.1:6379',
)


# ##################################### 定义异步任务 #######################################
@app.task
def test(arg):
    print(arg)


# ##################################### 定义异步任务 #######################################

# ##################################### 函数调用方式, 添加定时任务 #######################################
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 每 10 秒启动一次定时任务
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # 每 30 秒执行一次
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # 每周一早上 7:30 执行, 精确的定时任务使用 crontab 模块进行添加, crontab 语法同 linux
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Tuesday!'),
    )


# ##################################### 函数方式, 添加定时任务 #######################################

# ##################################### 配置文件方式, 添加定时任务 #######################################
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',  # tasks.add 是异步任务, 引用 tasks 模块中的 add 任务
        'schedule': 30.0,
        'args': (16, 16)
    },
}
# ##################################### 配置文件方式, 添加定时任务 #######################################
app.conf.timezone = 'UTC'
