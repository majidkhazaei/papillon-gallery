from celery import Celery
from datetime import timedelta
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')
celery_app = Celery('A')
celery_app.config_from_object({
    'broker_url': 'amqp://',
    'result_backend': 'rpc://',
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'result_expires': timedelta(days=1),
    'worker_prefetch_multiplier': 1,
    'task_always_eager': False,
})
