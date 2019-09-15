from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('02-celery-project',
             broker='redis://:mincoroot_924@127.0.0.1:6379',
             backend='redis://:mincoroot_924@127.0.0.1:6379',
             include=['02-celery-project.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
