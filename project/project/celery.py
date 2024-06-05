import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_mondays_8am': {
        'task': 'news.tasks.new_weekly_posts',
        'schedule': crontab(day_of_week='wednesday', hour=11, minute=10),
    },
}
