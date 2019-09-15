from __future__ import absolute_import, unicode_literals
from celery import shared_task


# @shared_task 装饰器指明的这是一个全局的异步任务, 即所有的模块均可以调用这个异步任务
@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y
