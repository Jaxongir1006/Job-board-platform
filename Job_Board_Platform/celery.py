import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Job_Board_Platform.settings')

app = Celery('Job_Board_Platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
