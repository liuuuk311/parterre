from celery.schedules import crontab

from core.celery import app

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'update-every-artist': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
    },
}
