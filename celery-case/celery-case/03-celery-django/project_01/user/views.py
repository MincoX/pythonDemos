from django.shortcuts import render, HttpResponse

from . import tasks


def index(request):
    res1 = tasks.add.delay(5, 20)
    res2 = tasks.mul.delay(10, 20)

    return HttpResponse(f'res1: --> {res1} + res2 --> {res2}')
