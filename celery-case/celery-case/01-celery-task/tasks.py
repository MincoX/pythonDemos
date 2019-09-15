from celery import Celery

app = Celery(
    'tasks',
    broker='redis://:mincoroot_924@127.0.0.1:6379',
    backend='redis://:mincoroot_924@127.0.0.1:6379',
)


@app.task
def add(x, y):
    print("running...", x, y)
    return x + y
