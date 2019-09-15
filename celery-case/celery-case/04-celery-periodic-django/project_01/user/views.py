from django.shortcuts import render, HttpResponse

from . import tasks


def index(request):
    res = tasks.add.delay(5, 20)

    return HttpResponse(f'task_id --> {res.id}')
