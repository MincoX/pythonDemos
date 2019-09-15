from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

# __all__，用于模块导入时对通配符 * 的限制，如：from module import *,
# 只有 __all__ 中的成员才可以被 * 导入
__all__ = ['celery_app']
