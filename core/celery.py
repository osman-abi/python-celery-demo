from celery import Celery

from .celeryconfig import Config
from celery.schedules import crontab

# Configuration
app = Celery('core', include=['core'])

app.config_from_object(Config)
app.conf.beat_schedule = {
    "execute-every-minute": {
        "task": "tasks.test",
        # every day at midnight
        "schedule": crontab(minute=0, hour=0)
    }
}


###############################################################################
# Tasks
@app.task(name='tasks.test')
def test():
    print("hello world")
