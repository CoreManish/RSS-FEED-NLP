# celery_tasks.py
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from app.services import update_articles

# Create a Celery instance
celery = Celery(
    'celery_tasks',
    broker='redis://localhost:6379/0',  # Redis connection details, redis as task queue storage for celery broker
    backend='redis://localhost:6379/1',
)

# Setup task logger
logger = get_task_logger(__name__)

# Celery task
@celery.task
def update_articles_task():
    try:
        update_articles()
        logger.info('Articles updated successfully.')
    except Exception as e:
        logger.error(f'Error updating articles: {str(e)}')

celery.conf.beat_schedule = {
    'update-articles-task': {
        'task': 'celery_tasks.update_articles_task',
        'schedule': crontab(minute='*/2'), #run every 2 minutes
    },
}


#--------------------------------
# To use redis
  # `sudo apt install redis-server`
  # `sudo service redis-server start`
  # `redis-cli ping` verify Redis is Running
# install redis library `pip install redis`
# start celery worker
  # celery -A celery_tasks worker --loglevel=info
# start celery beat
  # celery -A celery_tasks beat --loglevel=info

#--------------------------------