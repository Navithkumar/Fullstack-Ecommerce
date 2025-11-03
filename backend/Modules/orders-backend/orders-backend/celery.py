import os 
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE','orders-backend.settings')
app = Celery('orders-backend')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

