from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# 为 celery 项目设置 django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_01.settings')

app = Celery('project_01')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# 指定将 celery 的配置信息都设置在 django 的 settings.py 文件中, 关于 celery 的配置都要以 CELERY_ 形式配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.

# 配置 celery 自动查找 django 项目的每个模块下面的 tasks.py 文件中定义的异步任务
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
