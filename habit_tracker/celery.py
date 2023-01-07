import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings.dev')

celery = Celery('habit_tracker')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()