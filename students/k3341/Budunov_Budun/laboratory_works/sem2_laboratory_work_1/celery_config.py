from celery import Celery

app = Celery(
    'task_manager',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['celery_tasks']
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)